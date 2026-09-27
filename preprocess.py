from pathlib import Path
import pandas as pd
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from logs.logger import log_message

try:
    log_message("ETL Process Started")

    input_file = BASE_DIR / "dataset" / "transactions.csv"
    output_file = BASE_DIR / "dataset" / "clean_transactions.csv"

    df = pd.read_csv(input_file)

    print("\nORIGINAL DATASET\n")
    print(df.head())
    print(f"\nShape: {df.shape}")

    log_message(f"Dataset loaded. Records: {len(df)}, Columns: {len(df.columns)}")

    print("\n" + "=" * 60)

    # ── Step 1: Remove Duplicates ──
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    duplicates_removed = before - after

    print(f"\nDuplicates Removed: {duplicates_removed}")
    log_message(f"Duplicates removed: {duplicates_removed}")

    print("\n" + "=" * 60)

    # ── Step 2: Handle Missing Values ──
    print("\nMissing Values Before:")
    print(df.isnull().sum())

    # Fill missing numeric columns with column mean
    feature_cols = [f"V{i}" for i in range(1, 29)] + ["Time", "Amount"]

    for col in feature_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())

    # Drop rows where Class is missing (we need the label)
    before_class = len(df)
    df = df.dropna(subset=["Class"])
    dropped_class = before_class - len(df)

    print("\nMissing Values After:")
    print(df.isnull().sum())

    log_message(f"Missing values handled. Rows dropped due to missing Class: {dropped_class}")

    print("\n" + "=" * 60)

    # ── Step 3: Fix Data Types ──
    df["Class"] = df["Class"].astype(int)
    df["Amount"] = df["Amount"].astype(float)
    df["Time"] = df["Time"].astype(float)

    print("\nData Types Fixed")
    log_message("Data types normalized")

    print("\n" + "=" * 60)

    # ── Step 4: Fix Negative Amount ──
    negative_amounts = (df["Amount"] < 0).sum()
    df["Amount"] = df["Amount"].abs()

    print(f"\nNegative Amount Records Fixed: {negative_amounts}")
    log_message(f"Negative Amount values fixed: {negative_amounts}")

    print("\n" + "=" * 60)

    # ── Step 5: Class Distribution ──
    fraud_count = (df["Class"] == 1).sum()
    normal_count = (df["Class"] == 0).sum()
    fraud_pct = (fraud_count / len(df)) * 100

    print(f"\nClass Distribution:")
    print(f"  Normal Transactions : {normal_count}")
    print(f"  Fraudulent          : {fraud_count}")
    print(f"  Fraud Rate          : {fraud_pct:.4f}%")

    log_message(
        f"Class Distribution — Normal: {normal_count}, Fraud: {fraud_count}, Fraud Rate: {fraud_pct:.4f}%"
    )

    print("\n" + "=" * 60)

    # ── Step 6: Data Quality Score ──
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    quality_score = ((total_cells - missing_cells) / total_cells) * 100

    print(f"\nData Quality Score: {quality_score:.2f}%")
    log_message(f"Data Quality Score: {quality_score:.2f}%")

    print("\n" + "=" * 60)

    # ── Step 7: Save Clean Dataset ──
    df.to_csv(output_file, index=False)

    print("\nClean Dataset Saved Successfully")
    print(f"\nFinal Shape: {df.shape}")
    print("\nFinal Dataset Preview:\n")
    print(df.head())

    log_message(f"clean_transactions.csv created. Final records: {len(df)}")
    log_message("ETL Process Completed Successfully")

except Exception as e:
    print(f"\nERROR: {e}")
    log_message(f"ETL Process Failed: {str(e)}")