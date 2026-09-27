from pathlib import Path
import pandas as pd
import numpy as np
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from logs.logger import log_message

try:
    log_message("Self-Healing Process Started")

    input_file  = BASE_DIR / "dataset" / "anomaly_results.csv"
    output_file = BASE_DIR / "dataset" / "healed_transactions.csv"

    df = pd.read_csv(input_file)

    print("Loading anomaly results...")
    print(f"Total Records: {len(df)}")
    log_message(f"Anomaly Results Loaded. Records: {len(df)}")

    print("\n" + "=" * 60)

    normal_records  = df[df["Anomaly"] == "Normal"].copy()
    anomaly_records = df[df["Anomaly"] == "Anomaly"].copy()

    print(f"\nNormal Records  : {len(normal_records)}")
    print(f"Anomalies Found : {len(anomaly_records)}")

    log_message(f"Normal Records: {len(normal_records)}")
    log_message(f"Anomalies Found: {len(anomaly_records)}")

    print("\n" + "=" * 60)

    # ── Step 1: Heal Amount ──
    # Replace anomalous Amount with median of normal records
    median_amount = normal_records["Amount"].median()
    print(f"\nMedian Amount (from normal records): {median_amount:.2f}")
    log_message(f"Median Amount used for healing: {median_amount:.2f}")

    anomaly_records["Amount"] = anomaly_records["Amount"].apply(
        lambda x: median_amount if x <= 0 or x > 10000 else x
    )

    log_message("Amount healed — extreme values replaced with median")

    print("\n" + "=" * 60)

    # ── Step 2: Heal V1-V28 ──
    # Replace extreme outliers (beyond 3 std dev) with column median
    feature_cols = [f"V{i}" for i in range(1, 29)]

    healed_feature_count = 0

    for col in feature_cols:
        col_median = normal_records[col].median()
        col_std    = normal_records[col].std()
        upper      = col_median + 3 * col_std
        lower      = col_median - 3 * col_std

        extreme_mask = (
            (anomaly_records[col] > upper) |
            (anomaly_records[col] < lower)
        )

        healed_feature_count += extreme_mask.sum()

        anomaly_records[col] = anomaly_records[col].where(
            ~extreme_mask, col_median
        )

    print(f"\nFeature Values Healed (V1-V28): {healed_feature_count} extreme values replaced")
    log_message(f"V1-V28 healing: {healed_feature_count} extreme values replaced with column medians")

    print("\n" + "=" * 60)

    # ── Step 3: Add Healing Metadata ──
    anomaly_records["HealingStatus"] = "Healed"
    normal_records["HealingStatus"]  = "Original"

    log_message("HealingStatus column added")

    print("\n" + "=" * 60)

    # ── Step 4: Quarantine High-Risk Records ──
    # Flag records where Class == 1 (confirmed real fraud) as Quarantined
    quarantined = anomaly_records[anomaly_records["Class"] == 1].copy()
    quarantined["HealingStatus"] = "Quarantined"

    anomaly_records.loc[
        anomaly_records["Class"] == 1, "HealingStatus"
    ] = "Quarantined"

    print(f"\nQuarantined (Confirmed Fraud): {len(quarantined)}")
    log_message(f"Quarantined confirmed fraud records: {len(quarantined)}")

    print("\n" + "=" * 60)

    # ── Step 5: Combine and Save ──
    healed_df = pd.concat(
        [normal_records, anomaly_records],
        ignore_index=True
    )

    healed_df.to_csv(output_file, index=False)

    print(f"\nHealing Summary:")
    print(f"  Total Records       : {len(healed_df)}")
    print(f"  Original (Normal)   : {len(normal_records)}")
    print(f"  Healed (Anomaly)    : {len(anomaly_records) - len(quarantined)}")
    print(f"  Quarantined (Fraud) : {len(quarantined)}")

    log_message(f"Final Records: {len(healed_df)}")
    log_message(f"Healed: {len(anomaly_records) - len(quarantined)}, Quarantined: {len(quarantined)}")
    log_message("healed_transactions.csv created successfully")
    log_message("Self-Healing Process Completed Successfully")

    print("\nHealing Completed Successfully")

    print("\nSample Healed Records:\n")
    print(
        healed_df[healed_df["HealingStatus"] == "Healed"][[
            "Time", "Amount", "Class", "Anomaly", "HealingStatus"
        ]].head(10)
    )

except Exception as e:
    print(f"\nERROR: {e}")
    log_message(f"Self-Healing Failed: {str(e)}")