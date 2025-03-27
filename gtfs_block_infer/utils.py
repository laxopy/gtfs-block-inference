import os
import zipfile
from gtfs_block_infer.logger import get_logger

logger = get_logger(__name__)

def extract_gtfs_zip(gtfs_folder="data/gtfs"):
    """
    Extracts the first GTFS zip file in the folder (if any),
    only if trips.txt doesn't already exist.
    """
    trips_path = os.path.join(gtfs_folder, "trips.txt")
    if os.path.exists(trips_path):
        logger.info(f"[green]GTFS already extracted at {gtfs_folder}[/green]")
        return

    zip_files = [f for f in os.listdir(gtfs_folder) if f.endswith(".zip")]
    if not zip_files:
        raise FileNotFoundError("No GTFS zip file found in data/gtfs/")

    zip_path = os.path.join(gtfs_folder, zip_files[0])
    logger.info(f"[bold cyan]Extracting GTFS ZIP:[/bold cyan] {zip_path}")
    
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(gtfs_folder)

    logger.info(f"[green]GTFS extracted to {gtfs_folder}[/green]")
