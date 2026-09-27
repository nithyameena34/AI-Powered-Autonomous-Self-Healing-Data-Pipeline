from pathlib import Path
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from logs.logger import log_message

try:
    log_message("Anomaly Detection Process Started")

    input_file  = BASE_DIR / "dataset" / "clean_transactions.csv"
    output_file = BASE_DIR / "dataset" / "anomaly_results.csv"

    df = pd.read_csv(input_file)

    print("\nDataset Loaded Successfully")
    print(f"Shape: {df.shape}")
    log_message(f"Dataset Loaded. Records: {len(df)}, Columns: {len(df.columns)}")

    print("\n" + "=" * 60)

    # ── Step 1: Auto-Detect Feature Columns ──
    # Exclude known non-feature columns automatically
    exclude_cols = [
        "Class", "Anomaly", "HealingStatus",
        "Label", "Target", "label", "target",
        "class", "anomaly", "id", "ID", "Id"
    ]

    # Use only numeric columns, excluding labels
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    feature_cols = [col for col in numeric_cols if col not in exclude_cols]

    print(f"\nAuto-Detected Feature Columns ({len(feature_cols)}):")
    print(feature_cols)
    log_message(f"Auto-detected {len(feature_cols)} feature columns: {feature_cols}")

    print("\n" + "=" * 60)

    # ── Step 2: Auto-Scale All Features ──
    features = df[feature_cols].copy()
    scaler   = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    print("\nAll Features Scaled Successfully")
    log_message("All features normalized using StandardScaler")

    print("\n" + "=" * 60)

    # ── Step 3: Auto-Detect Contamination ──
    # Check if a label column exists to calculate real contamination
    label_col = None
    for col in ["Class", "class", "Label", "label", "Target", "target"]:
        if col in df.columns:
            label_col = col
            break

    if label_col:
        real_fraud_rate = round(
            df[label_col].astype(int).sum() / len(df), 6
        )
        # Clamp between 0.001 and 0.1 for Isolation Forest
        contamination = max(0.001, min(real_fraud_rate, 0.1))
        print(f"\nLabel Column Found: '{label_col}'")
        print(f"Real Fraud Rate   : {real_fraud_rate:.6f}")
        print(f"Contamination Set : {contamination:.6f}")
        log_message(f"Label column '{label_col}' found. Contamination: {contamination:.6f}")
    else:
        contamination = 0.02
        print(f"\nNo Label Column Found — Using Default Contamination: {contamination}")
        log_message(f"No label column found. Default contamination: {contamination}")

    print("\n" + "=" * 60)

    # ── Step 4: Train Isolation Forest ──
    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100
    )

    print("\nTraining Isolation Forest Model...")
    log_message("Isolation Forest Training Started")

    df["Anomaly"] = model.fit_predict(features_scaled)
    df["Anomaly"] = df["Anomaly"].map({1: "Normal", -1: "Anomaly"})

    log_message("Isolation Forest Training Completed")

    print("\nAnomaly Detection Completed")

    print("\n" + "=" * 60)

    # ── Step 5: Count Results ──
    anomaly_counts = df["Anomaly"].value_counts()
    print("\nAnomaly Count:")
    print(anomaly_counts)

    normal_count  = anomaly_counts.get("Normal", 0)
    anomaly_count = anomaly_counts.get("Anomaly", 0)

    log_message(f"Normal Records: {normal_count}")
    log_message(f"Anomalies Detected: {anomaly_count}")

    print("\n" + "=" * 60)

    # ── Step 6: Evaluate if Label Column Exists ──
    if label_col:
        print(f"\nModel Evaluation Against '{label_col}' Labels:")

        y_true = df[label_col].astype(int).map({0: "Normal", 1: "Anomaly"})
        y_pred = df["Anomaly"]

        cm = confusion_matrix(y_true, y_pred, labels=["Normal", "Anomaly"])

        print(f"\nConfusion Matrix:")
        print(f"  True Normal   (TN): {cm[0][0]}")
        print(f"  False Anomaly (FP): {cm[0][1]}")
        print(f"  Missed Fraud  (FN): {cm[1][0]}")
        print(f"  Caught Fraud  (TP): {cm[1][1]}")

        print("\nClassification Report:")
        print(classification_report(
            y_true, y_pred,
            target_names=["Normal", "Anomaly"]
        ))

        caught       = cm[1][1]
        total_fraud  = cm[1][0] + cm[1][1]
        detection_rate = (
            (caught / total_fraud) * 100
        ) if total_fraud > 0 else 0

        print(f"Fraud Detection Rate : {detection_rate:.2f}%")
        print(f"Fraud Caught         : {caught} / {total_fraud}")

        log_message(f"Detection Rate: {detection_rate:.2f}%")
        log_message(f"Caught {caught} out of {total_fraud} real fraud cases")

    else:
        print("\nNo Label Column — Skipping Evaluation")
        log_message("No label column — evaluation skipped")

    print("\n" + "=" * 60)

    # ── Step 7: Save Results ──
    df.to_csv(output_file, index=False)

    print("\nResults Saved Successfully")
    log_message("anomaly_results.csv created successfully")

    print("\nSample Detected Anomalies:\n")
    print(df[df["Anomaly"] == "Anomaly"].head(10))

    log_message("Anomaly Detection Process Completed Successfully")

except Exception as e:
    print(f"\nERROR: {e}")
    log_message(f"Anomaly Detection Failed: {str(e)}")