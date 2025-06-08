import pandas as pd

def convert_csv_to_json(input_file, output_file):
    df = pd.read_csv(input_file)  # comma is the default delimiter
    df.to_json(output_file, orient="records", indent=2)
    print(f"JSON saved to {output_file}")

convert_csv_to_json(
    input(f'Path to CSV input, pls: '),
    "output.json"
)
