import subprocess
import sys

STEPS = [
    ["-m", "ingestion.gdelt_ingest"],
    ["-m", "Preprocessing.clean_and_dedup"],
    ["-m", "Preprocessing.filter_articles"],
    ["-m", "NLP.ner_companies"],
    ["-m", "mapping.map_entities"],
    ["-m", "Aggregation.add_sentiment"],
    ["-m", "Aggregation.add_confidence"],
    ["-m", "Aggregation.persist_aggregates"],
    ["-m", "UI.sector_heatmap"],
    ["-m", "UI.ticker_heatmap"],
    ["-m", "Aggregation.persist_snapshots"],
]

for step in STEPS:
    print(f"\n=== Running {' '.join(step)} ===")
    result = subprocess.run([sys.executable, *step])

    if result.returncode != 0:
        print("Pipeline failed")
        break
