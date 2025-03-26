
import pandas as pd
from gtfs_block_infer.logger import get_logger
from gtfs_block_infer.config import UNASSIGNED_BLOCK_ID

logger = get_logger(__name__)

def apply_blocks_to_gtfs(trips_df, best_blocks_by_service):
    logger.info("[bold cyan]Applying inferred block_ids to GTFS trips...[/bold cyan]")

    trips_df = trips_df.copy()
    trips_df["block_id"] = UNASSIGNED_BLOCK_ID

    block_counter = 1
    trip_to_block = {}

    for service_id, info in best_blocks_by_service.items():
        blocks = info["blocks"]
        logger.info(f"[yellow]Assigning blocks for service_id={service_id}[/yellow]")
        for block in blocks:
            block_id = f"block_{block_counter:05d}"
            block_counter += 1
            for trip in block["trips"]:
                trip_id = trip["trip_id"]
                trip_to_block[trip_id] = block_id

    assigned_count = 0
    for idx, row in trips_df.iterrows():
        trip_id = row["trip_id"]
        if trip_id in trip_to_block:
            trips_df.at[idx, "block_id"] = trip_to_block[trip_id]
            assigned_count += 1

    logger.info(f"[green]Assigned block_id to {assigned_count} trips[/green]")
    return trips_df
