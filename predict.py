from pathlib import Path
import pandas as pd
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from logs.logger import log_message

try:
    log_message("Failure Prediction Started")

    anomaly_file = BASE_DIR / "dataset" / "anomaly_results.csv"
    healed_file  = BASE_DIR / "dataset" / "healed_transactions.csv"
    output_file  = BASE_DIR / "dataset" / "failure_prediction.csv"

    anomaly_df = pd.read_csv(anomaly_file)
    healed_df  = pd.read_csv(healed_file)

    print("\n" + "=" * 60)

    # ── Step 1: Core Counts ──
    total_records     = len(anomaly_df)
    anomalies         = len(anomaly_df[anomaly_df["Anomaly"] == "Anomaly"])
    normal_records    = len(anomaly_df[anomaly_df["Anomaly"] == "Normal"])
    confirmed_fraud   = len(healed_df[healed_df["HealingStatus"] == "Quarantined"])
    healed_records    = len(healed_df[healed_df["HealingStatus"] == "Healed"])
    anomaly_rate      = round((anomalies / total_records) * 100, 4)
    fraud_rate        = round((confirmed_fraud / total_records) * 100, 4)
    healing_rate      = round((healed_records / anomalies) * 100, 2) if anomalies > 0 else 0

    print(f"\nPipeline Summary:")
    print(f"  Total Records       : {total_records}")
    print(f"  Normal Records      : {normal_records}")
    print(f"  Anomalies Detected  : {anomalies}")
    print(f"  Confirmed Fraud     : {confirmed_fraud}")
    print(f"  Healed Records      : {healed_records}")
    print(f"  Anomaly Rate        : {anomaly_rate:.4f}%")
    print(f"  Fraud Rate          : {fraud_rate:.4f}%")
    print(f"  Healing Rate        : {healing_rate:.2f}%")

    log_message(f"Total Records: {total_records}")
    log_message(f"Anomalies: {anomalies}, Anomaly Rate: {anomaly_rate:.4f}%")
    log_message(f"Confirmed Fraud: {confirmed_fraud}, Fraud Rate: {fraud_rate:.4f}%")
    log_message(f"Healing Rate: {healing_rate:.2f}%")

    print("\n" + "=" * 60)

    # ── Step 2: Risk Classification ──
    # Based on anomaly rate thresholds
    if anomaly_rate < 0.1:
        risk  = "LOW"
        score = round(100 - (anomaly_rate * 10), 2)

    elif anomaly_rate < 0.5:
        risk  = "MEDIUM"
        score = round(100 - (anomaly_rate * 20), 2)

    else:
        risk  = "HIGH"
        score = round(max(0, 100 - (anomaly_rate * 30)), 2)

    # Health score from healed data
    health_score = round(
        ((total_records - anomalies) / total_records) * 100, 2
    )

    print(f"\nRisk Assessment:")
    print(f"  Failure Risk  : {risk}")
    print(f"  Risk Score    : {score}")
    print(f"  Health Score  : {health_score}%")

    log_message(f"Failure Risk: {risk}")
    log_message(f"Risk Score: {score}")
    log_message(f"Health Score: {health_score}%")

    print("\n" + "=" * 60)

    # ── Step 3: Fraud Detection Performance ──
    # How well did Isolation Forest catch real fraud?
    real_fraud_total  = len(anomaly_df[anomaly_df["Class"] == 1])
    real_fraud_caught = confirmed_fraud
    detection_rate    = round(
        (real_fraud_caught / real_fraud_total) * 100, 2
    ) if real_fraud_total > 0 else 0

    false_positives = anomalies - confirmed_fraud
    fp_rate         = round(
        (false_positives / normal_records) * 100, 4
    ) if normal_records > 0 else 0

    print(f"\nFraud Detection Performance:")
    print(f"  Real Fraud in Dataset   : {real_fraud_total}")
    print(f"  Fraud Caught            : {real_fraud_caught}")
    print(f"  Detection Rate          : {detection_rate:.2f}%")
    print(f"  False Positives         : {false_positives}")
    print(f"  False Positive Rate     : {fp_rate:.4f}%")

    log_message(f"Detection Rate: {detection_rate:.2f}%")
    log_message(f"False Positives: {false_positives}, FP Rate: {fp_rate:.4f}%")

    print("\n" + "=" * 60)

    # ── Step 4: Save Results ──
    result = pd.DataFrame([{
        "TotalRecords"      : total_records,
        "NormalRecords"     : normal_records,
        "Anomalies"         : anomalies,
        "ConfirmedFraud"    : confirmed_fraud,
        "HealedRecords"     : healed_records,
        "AnomalyRate"       : anomaly_rate,
        "FraudRate"         : fraud_rate,
        "HealingRate"       : healing_rate,
        "FailureRisk"       : risk,
        "RiskScore"         : score,
        "HealthScore"       : health_score,
        "DetectionRate"     : detection_rate,
        "FalsePositives"    : false_positives,
        "FalsePositiveRate" : fp_rate
    }])

    result.to_csv(output_file, index=False)

    print(f"\nFailure Risk    : {risk}")
    print(f"Health Score    : {health_score}%")
    print(f"Detection Rate  : {detection_rate:.2f}%")
    print(f"\nPrediction Saved Successfully")

    log_message("failure_prediction.csv created")
    log_message("Failure Prediction Completed")

except Exception as e:
    print(f"\nERROR: {e}")
    log_message(f"Failure Prediction Failed: {e}")