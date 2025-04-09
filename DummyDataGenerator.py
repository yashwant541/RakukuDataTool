import os
import pandas as pd
from faker import Faker
import random

def read_sample(file_path, num_rows=10):
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path, nrows=num_rows)
    elif file_extension.lower() == '.txt':
        df = pd.read_csv(file_path, sep='\t', nrows=num_rows)
    else:
        df = pd.read_csv(file_path, nrows=num_rows)

    return df

def analyze_data(df):
    # Extract field names, data types, and unique values
    field_info = df.dtypes.reset_index()
    field_info.columns = ['Field', 'Data Type']

    unique_values = df.apply(lambda col: col.unique()).reset_index()
    unique_values.columns = ['Field', 'Unique Values']

    field_info = pd.merge(field_info, unique_values, on='Field', how='left')

    return field_info

def generate_dummy_data(field_info, num_rows=100, with_duplicates=False, with_errors=False, with_blank_fields=False):
    fake = Faker()

    # Generate empty dataframe with the same columns as the original data
    dummy_data = pd.DataFrame(columns=field_info['Field'])

    # Generate dummy data based on data types, field lengths, and specific values
    for index, row in field_info.iterrows():
        field_name = row['Field']
        data_type = row['Data Type']
        unique_values = row['Unique Values']

        if 'int' in str(data_type):
            # Generate whole numbers for integer fields with the same precision
            dummy_data[field_name] = [random.randint(1, 100) for _ in range(num_rows)]
        elif 'float' in str(data_type):
            # Generate decimal values for float fields with the same precision
            dummy_data[field_name] = [round(random.uniform(1, 100), 2) for _ in range(num_rows)]
        elif 'object' in str(data_type):
            # Generate object data with the same unique values
            dummy_data[field_name] = [random.choice(unique_values) for _ in range(num_rows)]
        elif 'datetime' in str(data_type):
            dummy_data[field_name] = [fake.date_this_decade() for _ in range(num_rows)]
        elif 'bool' in str(data_type):
            dummy_data[field_name] = [random.choice([True, False]) for _ in range(num_rows)]

    # Add duplicates, data type errors, blank fields based on user options
    if with_duplicates:
        dummy_data = pd.concat([dummy_data, dummy_data.sample(frac=0.2)])
    if with_errors:
        # Introduce data type errors, e.g., changing int to string in some rows
        for index, row in field_info.iterrows():
            if 'int' in str(row['Data Type']):
                dummy_data[row['Field']].iloc[:num_rows//2] = [fake.word() for _ in range(num_rows//2)]
    if with_blank_fields:
        # Introduce blank or null fields
        for index, row in field_info.iterrows():
            dummy_data[row['Field']].iloc[:num_rows//3] = None

    return dummy_data

def main(folder_path, options=None, num_rows=100):
    # Get the list of files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        
        # Skip non-data files
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() not in ['.xls', '.xlsx', '.txt', '.csv']:
            continue

        sample_data = read_sample(file_path)
        field_info = analyze_data(sample_data)

        with_duplicates = '1' in options
        with_errors = '2' in options
        with_blank_fields = '4' in options

        # Assume no blanks, no errors, and no duplicates if options input is blank
        if not options:
            with_duplicates = with_errors = with_blank_fields = False

        # Ask the user for the required number of rows
        # num_rows = int(input("Enter the number of rows for dummy data: "))

        # dummy_data = generate_dummy_data(field_info, num_rows=num_rows, with_duplicates=with_duplicates, with_errors=with_errors, with_blank_fields=with_blank_fields)

        # # Save the generated dummy data to a new CSV file in the same folder
        # output_file_path = os.path.join(folder_path, f"{os.path.splitext(file_name)[0]}_dummy.csv")
        # dummy_data.to_csv(output_file_path, index=False)
        dummy_data = generate_dummy_data(field_info, num_rows=num_rows, with_duplicates=with_duplicates, with_errors=with_errors, with_blank_fields=with_blank_fields)

        # Save the generated dummy data to a new CSV file in the same folder
        output_file_path = os.path.join(folder_path, f"{os.path.splitext(file_name)[0]}_dummy.csv")
        dummy_data.to_csv(output_file_path, index=False)