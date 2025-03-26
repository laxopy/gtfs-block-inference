
import pandas as pd
from collections import defaultdict
from datetime import timedelta
from gtfs_block_infer.logger import get_logger
from gtfs_block_infer.config import MIN_TRIPS_IN_BLOCK

logger = get_logger(__name__)

def parse_time_from_gtfs(stop_times_df):
    trip_times = stop_times_df.groupby("trip_id").agg({
        "departure_time": "min",
        "arrival_time": "max"
    }).reset_index()
    trip_times.rename(columns={"departure_time": "start_time", "arrival_time": "end_time"}, inplace=True)
    return trip_times

def validate_block(trips_in_block):
    sorted_trips = sorted(trips_in_block, key=lambda x: x['start_time'])
    for i in range(1, len(sorted_trips)):
        if sorted_trips[i]['start_time'] < sorted_trips[i-1]['end_time']:
            return False
    return True

def resolve_multi_vehicle_assignment(trip_id, candidates, trip_times):
    best_vehicle = None
    best_fit_score = float('inf')
    
    for vehicle_id in candidates:
        vehicle_trips = trip_times.get(vehicle_id, [])
        for i, trip in enumerate(vehicle_trips):
            if trip['trip_id'] == trip_id:
                prev_end = vehicle_trips[i-1]['end_time'] if i > 0 else None
                next_start = vehicle_trips[i+1]['start_time'] if i < len(vehicle_trips) - 1 else None
                this_start = trip['start_time']
                this_end = trip['end_time']
                
                gaps = []
                if prev_end: gaps.append(abs((this_start - prev_end).total_seconds()))
                if next_start: gaps.append(abs((next_start - this_end).total_seconds()))
                
                fit_score = sum(gaps) if gaps else 0
                if fit_score < best_fit_score:
                    best_fit_score = fit_score
                    best_vehicle = vehicle_id

    logger.info(f"Trip {trip_id} assigned to vehicle {best_vehicle} (best fit among {candidates})")
    return best_vehicle

def infer_blocks(history_df, stop_times_df):
    logger.info("[bold cyan]Starting block inference...[/bold cyan]")

    trip_times_df = parse_time_from_gtfs(stop_times_df)
    history_df = history_df.copy()
    
    history_df = history_df.merge(trip_times_df, how="left", left_on="tripId", right_on="trip_id")

    grouped = history_df.groupby(["serviceId", "serviceDate"])
    all_blocks = {}

    for (service_id, service_date), group in grouped:
        logger.info(f"[yellow]Analyzing service_id={service_id} on date={service_date}[/yellow]")

        vehicle_blocks = defaultdict(list)
        unresolved = []

        for _, row in group.iterrows():
            trip_id = row['tripId']
            vehicle_ids = str(row['vehicleIds']).split(",") if pd.notnull(row['vehicleIds']) else []

            if len(vehicle_ids) == 1:
                vehicle_blocks[vehicle_ids[0]].append({
                    "trip_id": trip_id,
                    "start_time": row['start_time'],
                    "end_time": row['end_time']
                })
            elif len(vehicle_ids) > 1:
                unresolved.append((trip_id, vehicle_ids, row['start_time'], row['end_time']))
        
        for trip_id, vehicle_ids, start_time, end_time in unresolved:
            trip_times_by_vehicle = {
                v: sorted(vehicle_blocks[v], key=lambda x: x['start_time']) for v in vehicle_ids if v in vehicle_blocks
            }
            best_vehicle = resolve_multi_vehicle_assignment(trip_id, vehicle_ids, trip_times_by_vehicle)
            if best_vehicle:
                vehicle_blocks[best_vehicle].append({
                    "trip_id": trip_id,
                    "start_time": start_time,
                    "end_time": end_time
                })

        valid_blocks = []
        for vehicle_id, trips in vehicle_blocks.items():
            sorted_trips = sorted(trips, key=lambda x: x['start_time'])
            if validate_block(sorted_trips):
                if len(sorted_trips) >= MIN_TRIPS_IN_BLOCK:
                    logger.info(f"[green]Valid block: vehicle_id={vehicle_id}, {len(sorted_trips)} trips[/green]")
                    valid_blocks.append({
                        "vehicle_id": vehicle_id,
                        "trips": sorted_trips
                    })
                else:
                    logger.warning(f"Block too short: vehicle_id={vehicle_id}, only {len(sorted_trips)} trips")
            else:
                logger.warning(f"[red]Time overlap in block for vehicle_id={vehicle_id}[/red]")

        all_blocks[(service_id, service_date)] = valid_blocks
        logger.info(f"Total valid blocks for {service_id} on {service_date}: {len(valid_blocks)}")

    return all_blocks
