import subprocess
import sys

print("Starting AI Self-Healing Pipeline...\n")

steps = [
    ("STEP 1: ETL", "etl/preprocess.py"),

    ("STEP 2: Anomaly Detection",
     "anomaly_detection/detect.py"),

    ("STEP 3: Self-Healing",
     "self_healing/heal.py"),

    ("STEP 4: Database",
     "database/db.py"),

    ("STEP 5: Failure Prediction",
     "failure_prediction/predict.py"),

]

for label, script in steps:

    print("=" * 60)
    print(label)
    print("=" * 60)

    try:
        subprocess.run(
            [sys.executable, script],
            check=True
        )

        print(f"\n{label} Completed Successfully\n")

    except subprocess.CalledProcessError:

        print(f"\nERROR in {label}")
        print("Pipeline Stopped.\n")

        sys.exit(1)

print("=" * 60)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)