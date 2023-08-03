import os
import pandas as pd
import logging

def extract_numeric_price(price_str):
    # Extract numeric values from the price string using regular expressions
    numeric_value = pd.to_numeric(price_str.str.replace(r'[\D]', ''), errors='coerce')
    return numeric_value

def calculate_percentage_drop(old_price, new_price):
    if old_price == 0:
        return float('inf')  # Set percentage drop to infinity if the old price is zero
    return ((old_price - new_price) / old_price) * 100

def main():
    log_file_directory = r"C:\Users\nisch\updt price_extract"
    log_file_path = r"C:\Users\nisch\updt price_extract/log_file.txt"

    # Create the log file directory if it doesn't exist
    os.makedirs(log_file_directory, exist_ok=True)
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format="%(message)s")
    
    # File paths for the CSV files
    file1 = "Last_ran_data.csv"
    file2 = "present_ran_data.csv"

    # Read the CSV files into pandas DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Extract numeric values from the 'Price' columns
    df1['Price'] = extract_numeric_price(df1['Price'])
    df2['Price'] = extract_numeric_price(df2['Price'])

    # Merge the DataFrames based on the 'Links' and 'Brands' columns
    merged_df = pd.merge(df1, df2, on=['Links', 'Brands'], suffixes=('_old', '_new'))

    # Calculate the percentage drop and log the results
    for _, row in merged_df.iterrows():
        link_brand = f"{row['Links']},{row['Brands']}"
        percentage_drop = calculate_percentage_drop(row['Price_old'], row['Price_new'])
        logging.info(f"{link_brand},{percentage_drop:.2f}%")

if __name__ == "__main__":
    main()
