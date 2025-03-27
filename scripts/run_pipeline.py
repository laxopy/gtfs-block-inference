import os
import shutil
import pandas as pd

from gtfs_block_infer import block_inference, block_selector, block_applier
from gtfs_block_infer.utils import extract_gtfs_zip


def load_latest_history_csv(history_folder="data/history"):
    csv_files = [f for f in os.listdir(history_folder) if f.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError("No historical CSV file found in data/history/")
    csv_files.sort()  # optional: load latest by filename
    return os.path.join(history_folder, csv_files[-1])


def prepare_gtfs_inputs(gtfs_folder="data/gtfs"):
    extract_gtfs_zip(gtfs_folder)
    trips = pd.read_csv(os.path.join(gtfs_folder, "trips.txt"), dtype=str)
    stop_times = pd.read_csv(os.path.join(gtfs_folder, "stop_times.txt"), dtype=str)
    stop_times["departure_time"] = pd.to_timedelta(stop_times["departure_time"].fillna("00:00:00"))
    stop_times["arrival_time"] = pd.to_timedelta(stop_times["arrival_time"].fillna("00:00:00"))
    return trips, stop_times


def save_modified_gtfs(trips_df, original_gtfs_dir, output_dir="output/gtfs_with_blocks"):
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(original_gtfs_dir):
        if file != "trips.txt" and file.endswith(".txt"):
            shutil.copyfile(
                os.path.join(original_gtfs_dir, file),
                os.path.join(output_dir, file)
            )

    trips_df.to_csv(os.path.join(output_dir, "trips.txt"), index=False)

    zip_path = shutil.make_archive(output_dir, "zip", output_dir)
    print(f"[✓] New GTFS with blocks created at: {zip_path}")


def main():
    gtfs_path = "data/gtfs"
    history_path = load_latest_history_csv()

    trips_df, stop_times_df = prepare_gtfs_inputs(gtfs_path)
    history_df = pd.read_csv(history_path, dtype=str)

    inferred_blocks = block_inference.infer_blocks(history_df, stop_times_df)
    best_blocks = block_selector.select_best_blocks(inferred_blocks)
    updated_trips_df = block_applier.apply_blocks_to_gtfs(trips_df, best_blocks)

    save_modified_gtfs(updated_trips_df, original_gtfs_dir=gtfs_path)


if __name__ == "__main__":
    main()
