import pandas as pd
import os

def save_to_csv(filename, data):
    """Append a dictionary as a row to a CSV file."""
    df = pd.DataFrame([data])
    if not os.path.exists(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)

def load_from_csv(filename):
    """Load a CSV file into a pandas DataFrame."""
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame()