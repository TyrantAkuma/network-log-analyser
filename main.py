from src.loader import load
from src.analyser import run
from src.report import print_report

if __name__ == "__main__":
    print("Step 1: Loading dataset into MySQL...")
    load()

    print("Step 2: Running anomaly detection...")
    results = run()

    print("Step 3: Generating report...")
    print_report(results)
