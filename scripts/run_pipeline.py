from gtfs_block_infer import block_inference, block_selector, block_applier
import pandas as pd

def main():
    trips_df = pd.read_csv("data/gtfs/trips.txt", dtype=str)
    stop_times_df = pd.read_csv("data/gtfs/stop_times.txt", dtype=str)
    history_df = pd.read_csv("data/history/history.csv", dtype=str)

    stop_times_df["departure_time"] = pd.to_timedelta(stop_times_df["departure_time"].fillna("00:00:00"))
    stop_times_df["arrival_time"] = pd.to_timedelta(stop_times_df["arrival_time"].fillna("00:00:00"))

    inferred_blocks = block_inference.infer_blocks(history_df, stop_times_df)
    best_blocks = block_selector.select_best_blocks(inferred_blocks)
    updated_trips_df = block_applier.apply_blocks_to_gtfs(trips_df, best_blocks)

    updated_trips_df.to_csv("output/trips_with_blocks.txt", index=False)

if __name__ == "__main__":
    main()
