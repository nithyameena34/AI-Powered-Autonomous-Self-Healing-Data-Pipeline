import pandas as pd
import sqlite3
from pathlib import Path

# Project Root
ROOT = Path(__file__).resolve().parent.parent.parent

# Dataset Paths
DATASET = ROOT / "dataset"

ANOMALY_FILE    = DATASET / "anomaly_results.csv"
HEALED_FILE     = DATASET / "healed_transactions.csv"
PREDICTION_FILE = DATASET / "failure_prediction.csv"
CLEAN_FILE      = DATASET / "clean_transactions.csv"

# Database Path
DB_FILE = ROOT / "database" / "pipeline.db"

# Log File
LOG_FILE = ROOT / "logs" / "pipeline.log"


# ----------------------------
# Load Anomaly Data
# ----------------------------

def load_anomaly_data():
    try:
        return pd.read_csv(ANOMALY_FILE)
    except Exception:
        return pd.DataFrame()


# ----------------------------
# Load Healed Data
# ----------------------------

def load_healed_data():
    try:
        return pd.read_csv(HEALED_FILE)
    except Exception:
        return pd.DataFrame()


# ----------------------------
# Load Prediction Data
# ----------------------------

def load_prediction_data():
    try:
        df = pd.read_csv(PREDICTION_FILE)
        if df.empty:
            return {}
        row = df.iloc[0]
        return {
            "TotalRecords"      : int(row.get("TotalRecords", 0)),
            "NormalRecords"     : int(row.get("NormalRecords", 0)),
            "Anomalies"         : int(row.get("Anomalies", 0)),
            "ConfirmedFraud"    : int(row.get("ConfirmedFraud", 0)),
            "HealedRecords"     : int(row.get("HealedRecords", 0)),
            "AnomalyRate"       : float(row.get("AnomalyRate", 0)),
            "FraudRate"         : float(row.get("FraudRate", 0)),
            "HealingRate"       : float(row.get("HealingRate", 0)),
            "FailureRisk"       : str(row.get("FailureRisk", "LOW")),
            "RiskScore"         : float(row.get("RiskScore", 100)),
            "HealthScore"       : float(row.get("HealthScore", 100)),
            "DetectionRate"     : float(row.get("DetectionRate", 0)),
            "FalsePositives"    : int(row.get("FalsePositives", 0)),
            "FalsePositiveRate" : float(row.get("FalsePositiveRate", 0)),
        }
    except Exception:
        return {}


# ----------------------------
# Load Clean Data
# ----------------------------

def load_clean_data():
    try:
        return pd.read_csv(CLEAN_FILE)
    except Exception:
        return pd.DataFrame()


# ----------------------------
# Load Database Records
# ----------------------------

def load_database_records():
    try:
        conn = sqlite3.connect(DB_FILE)
        df   = pd.read_sql("SELECT * FROM transactions", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


# ----------------------------
# Load Healing Summary from DB
# ----------------------------

def load_healing_summary():
    try:
        conn = sqlite3.connect(DB_FILE)
        df   = pd.read_sql("SELECT * FROM healing_summary", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


# ----------------------------
# Load Fraud Summary from DB
# ----------------------------

def load_fraud_summary():
    try:
        conn = sqlite3.connect(DB_FILE)
        df   = pd.read_sql("SELECT * FROM fraud_summary", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


# ----------------------------
# Load Anomaly Results from DB
# ----------------------------

def load_anomaly_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        df   = pd.read_sql("SELECT * FROM anomaly_results", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


# ----------------------------
# Read Logs
# ----------------------------

def load_logs():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = f.readlines()
        return logs[-50:]
    except Exception:
        return ["No logs available."]


# ----------------------------
# Check Pipeline Files Exist
# ----------------------------

def check_pipeline_status():
    return {
        "ETL"               : CLEAN_FILE.exists(),
        "Anomaly Detection" : ANOMALY_FILE.exists(),
        "Self Healing"      : HEALED_FILE.exists(),
        "Database"          : DB_FILE.exists(),
        "Failure Prediction": PREDICTION_FILE.exists(),
    }