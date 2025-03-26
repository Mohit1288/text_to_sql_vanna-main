import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

def preprocess_and_import_data(CSV_FILE_PATH, MYSQL_CONFIG):
    """
    This function reads data from a CSV file, preprocesses it (handling missing values, 
    converting dates, normalizing data), and then imports the data into a MySQL database.
    """
    # === Read CSV File ===
    df = pd.read_csv(CSV_FILE_PATH, dtype=str, skip_blank_lines=False)

    # Replace NaN values (from blank rows/cells) with None so that they become SQL NULLs
    df = df.where(pd.notnull(df), None)

    # === Preprocess Data ===
    # Handle missing values - Fill NaN values with appropriate values (could be median, mean, etc.)
    df.fillna({
        'is_canceled': '0',  # Fill 'is_canceled' with '0' if missing
        'country': 'Unknown',  # Fill 'country' with 'Unknown' if missing
        'meal': 'Undefined',  # Fill 'meal' with 'Undefined' if missing
        'market_segment': 'Unknown',  # Fill 'market_segment' with 'Unknown' if missing
        'distribution_channel': 'Unknown',  # Fill 'distribution_channel' with 'Unknown' if missing
        'reserved_room_type': 'Undefined',  # Fill 'reserved_room_type' with 'Undefined' if missing
        'assigned_room_type': 'Undefined',  # Fill 'assigned_room_type' with 'Undefined' if missing
        'deposit_type': 'No Deposit',  # Fill 'deposit_type' with 'No Deposit' if missing
        'agent': 'Unknown',  # Fill 'agent' with 'Unknown' if missing
        'company': 'Unknown',  # Fill 'company' with 'Unknown' if missing
        'customer_type': 'Unknown',  # Fill 'customer_type' with 'Unknown' if missing
        'reservation_status': 'Unknown',  # Fill 'reservation_status' with 'Unknown' if missing
    }, inplace=True)

    # Convert relevant columns to the appropriate data types
    df['lead_time'] = pd.to_numeric(df['lead_time'], errors='coerce')  # Convert 'lead_time' to numeric
    df['adults'] = pd.to_numeric(df['adults'], errors='coerce')  # Convert 'adults' to numeric
    df['children'] = pd.to_numeric(df['children'], errors='coerce')  # Convert 'children' to numeric
    df['babies'] = pd.to_numeric(df['babies'], errors='coerce')  # Convert 'babies' to numeric
    df['previous_cancellations'] = pd.to_numeric(df['previous_cancellations'], errors='coerce')  # Convert 'previous_cancellations' to numeric
    df['previous_bookings_not_canceled'] = pd.to_numeric(df['previous_bookings_not_canceled'], errors='coerce')  # Convert 'previous_bookings_not_canceled' to numeric
    df['days_in_waiting_list'] = pd.to_numeric(df['days_in_waiting_list'], errors='coerce')  # Convert 'days_in_waiting_list' to numeric
    df['adr'] = pd.to_numeric(df['adr'], errors='coerce')  # Convert 'adr' to numeric
    df['required_car_parking_spaces'] = pd.to_numeric(df['required_car_parking_spaces'], errors='coerce')  # Convert 'required_car_parking_spaces' to numeric
    df['total_of_special_requests'] = pd.to_numeric(df['total_of_special_requests'], errors='coerce')  # Convert 'total_of_special_requests' to numeric

    # Convert 'arrival_date_year', 'arrival_date_month', 'arrival_date_week_number', 'arrival_date_day_of_month' to datetime
    df['arrival_date'] = pd.to_datetime(df['arrival_date_year'].astype(str) + '-' +
                                         df['arrival_date_month'].astype(str) + '-' +
                                         df['arrival_date_day_of_month'].astype(str), errors='coerce')

    # Convert 'reservation_status_date' to datetime
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce')

    # Extract year, month, and day from 'arrival_date'
    df['arrival_year'] = df['arrival_date'].dt.year
    df['arrival_month'] = df['arrival_date'].dt.month
    df['arrival_day'] = df['arrival_date'].dt.day

    # Remove rows where 'adr' or 'lead_time' is negative or invalid
    df = df[df['adr'] >= 0]
    df = df[df['lead_time'] >= 0]

    # Normalize the 'adr' column (Min-Max scaling)
    df['adr_normalized'] = (df['adr'] - df['adr'].min()) / (df['adr'].max() - df['adr'].min())

    # Remove duplicates
    df = df.drop_duplicates()

    # === Extract Table Name from CSV File Name ===
    # This will use the filename (without extension) as the table name.
    table_name = os.path.splitext(os.path.basename(CSV_FILE_PATH))[0]

    # === Connect to MySQL ===
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    # === Create Table ===
    # Drop the table if it exists, then create a new one with each column defined as TEXT.
    columns = df.columns.tolist()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

    create_table_query = f"CREATE TABLE {table_name} ("
    for col in columns:
        create_table_query += f"{col} TEXT, "
    # Remove trailing comma and space, then close the statement
    create_table_query = create_table_query.rstrip(', ') + ');'
    cursor.execute(create_table_query)

    # === Prepare Insert Query ===
    # Create a parameterized query to insert each row.
    placeholders = ", ".join(["%s"] * len(columns))
    column_names = ", ".join([f"{col}" for col in columns])
    insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders});"

    # Convert DataFrame rows into a list of tuples
    data = df.values.tolist()

    # Insert all rows into the table.
    cursor.executemany(insert_query, data)
    conn.commit()

    print(f"Data from {CSV_FILE_PATH} uploaded successfully to table '{table_name}'.")

    # === Clean Up ===
    cursor.close()
    conn.close()

# Example Usage:

# Define your MySQL database configuration
load_dotenv()
MYSQL_CONFIG = {
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
}

# Define the path to your CSV file
CSV_FILE_PATH = 'data/hotel_bookings.csv'  # Update with the correct path to your CSV file

# Call the function to preprocess and import the data
preprocess_and_import_data(CSV_FILE_PATH, MYSQL_CONFIG)
