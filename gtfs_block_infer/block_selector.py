
from collections import defaultdict
from gtfs_block_infer.logger import get_logger

logger = get_logger(__name__)

def select_best_blocks(inferred_blocks):
    logger.info("[bold cyan]Selecting best service date per service_id...[/bold cyan]")
    
    blocks_by_service = defaultdict(list)

    for (service_id, service_date), blocks in inferred_blocks.items():
        trip_ids = set()
        for block in blocks:
            for trip in block["trips"]:
                trip_ids.add(trip["trip_id"])
        blocks_by_service[service_id].append({
            "date": service_date,
            "trip_ids": trip_ids,
            "blocks": blocks
        })

    best_blocks = {}

    for service_id, block_sets in blocks_by_service.items():
        logger.info(f"[yellow]Evaluating service_id={service_id}[/yellow]")
        sorted_sets = sorted(block_sets, key=lambda b: (len(b["trip_ids"]), b["date"]), reverse=True)
        best = sorted_sets[0]
        logger.info(f"[green]Selected date {best['date']} with {len(best['trip_ids'])} trips[/green]")
        best_blocks[service_id] = {
            "service_date": best["date"],
            "blocks": best["blocks"]
        }

    return best_blocks
