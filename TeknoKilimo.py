import sqlite3
import random
import time
import pandas as pd

# Database setup
conn = sqlite3.connect('tekno_kilimo.db')
c = conn.cursor()

# Create tables
c.execute('''
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    sensor_type TEXT,
    value REAL
)
''')

# Simulate IoT sensor data
sensor_types = ['temperature', 'humidity', 'soil_moisture', 'ph_level']

def simulate_sensor_data():
    data = []
    for sensor in sensor_types:
        value = random.uniform(10, 30) if sensor == 'temperature' else random.uniform(0, 100)
        data.append((sensor, value))
    return data

def insert_sensor_data(data):
    with conn:
        c.executemany('INSERT INTO sensor_data (sensor_type, value) VALUES (?, ?)', data)

# Data Processing and Analysis
def get_average_sensor_values():
    query = '''
    SELECT sensor_type, AVG(value) as avg_value
    FROM sensor_data
    GROUP BY sensor_type
    '''
    df = pd.read_sql_query(query, conn)
    return df

def get_sensor_trends():
    query = '''
    SELECT timestamp, sensor_type, value
    FROM sensor_data
    ORDER BY timestamp DESC
    LIMIT 100
    '''
    df = pd.read_sql_query(query, conn)
    return df.pivot(index='timestamp', columns='sensor_type', values='value')

# Simulate and insert data every minute (for demonstration purposes)
def main():
    for _ in range(5):  # Simulate 5 cycles of data collection
        data = simulate_sensor_data()
        insert_sensor_data(data)
        time.sleep(1)  # Wait for 1 second before next data collection cycle

    # Perform data analysis
    avg_values = get_average_sensor_values()
    trends = get_sensor_trends()

    print("Average Sensor Values:")
    print(avg_values)
    print("\nSensor Trends:")
    print(trends)

if __name__ == '__main__':
    main()

# Close the connection
conn.close()
