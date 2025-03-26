# GTFS Block Inference

This project infers `block_id`s in a GTFS feed using historical trip observations, based on real-world vehicle behavior. It is particularly useful when your GTFS feed does not include block assignments, and you want to improve trip chaining logic, vehicle assignment tracking, or real-time rider info systems.

---

## 🚀 Features

- ✅ Vehicle-based block inference using historical observations
- ✅ Automatically selects best reference day per `service_id`
- ✅ Validates trip chains for time consistency (no overlaps)
- ✅ Skips uncertain or ambiguous trip assignments
- ✅ Appends inferred `block_id` to `trips.txt` in GTFS format

---

## 📁 Project Structure

```
gtfs-block-inference/
├── gtfs_block_infer/       # Core logic modules
├── scripts/                # Pipeline entry point
├── data/                   # (Ignored) Input GTFS + history
├── output/                 # Generated updated GTFS files
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🧱 Requirements

- Python 3.8+
- GTFS files: at least `trips.txt` and `stop_times.txt`
- A historical CSV with these columns:
  - `tripId`
  - `vehicleIds` (can be multiple, comma-separated)
  - `serviceId`
  - `serviceDate`

---

## 🧪 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/gtfs-block-inference.git
cd gtfs-block-inference
```

### 2. Create and activate a virtual environment

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📦 Input Data

Organize your files like this:

```
data/
├── gtfs/
│   ├── trips.txt
│   └── stop_times.txt
└── history/
    └── history.csv
```

Make sure your `history.csv` has the required columns as listed above.

---

## ▶️ Run the Pipeline

```bash
python scripts/run_pipeline.py
```

This will:
1. Load GTFS and historical data
2. Infer valid blocks from real vehicle behavior
3. Select the best date per `service_id`
4. Assign `block_id`s to GTFS `trips.txt`
5. Output a modified `trips_with_blocks.txt` to `output/`

---

## 🧹 Output

```
output/
└── trips_with_blocks.txt  # GTFS-compatible file with block_id column
```

You can now merge this updated file back into your GTFS feed.

---

## 🔐 Git Safety

This project is designed **not to track any private or sensitive data**:

- `data/` is listed in `.gitignore`
- No historical data or GTFS samples are included in the repo

---

## 📬 Feedback & Contributions

Issues, ideas, or pull requests are welcome! Feel free to fork this project and adapt it to your transit agency’s needs.

---

## 📄 License

MIT — use it freely, modify as you wish.