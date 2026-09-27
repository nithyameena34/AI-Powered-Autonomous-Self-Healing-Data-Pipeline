import pandas as pd
import time
import sys
import os

# Add project root folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

# Import logger
from logs.logger import log_message

# Log start
log_message("Streaming started")

# Load dataset
df = pd.read_csv("../dataset/transactions.csv")

print("Starting Real-Time Data Stream...\n")

try:
    # Stream records one by one
    for index, row in df.iterrows():

        print("Streaming Record:")
        print(row.to_dict())

        print("-" * 40)

        # Log transaction
        transaction_id = row.get(
            "TransactionID",
            f"ROW_{index}"
        )

        log_message(
            f"Processed Transaction: {transaction_id}"
        )

        # Wait 2 seconds
        time.sleep(2)

    print("\nStreaming Finished Successfully")

    log_message("Streaming completed successfully")

except KeyboardInterrupt:

    print("\nStreaming stopped by user")

    log_message("Streaming stopped by user")

except Exception as e:

    print(f"\nError: {e}")

    log_message(f"Streaming error: {e}")