#!/usr/bin/env python3
from datetime import datetime

# Get current time
current_time = datetime.now()

# Format time for filename (avoiding special characters that might cause issues)
filename_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
filename = f"time_{filename_time}.txt"

# Format time for content
time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")

# Write to file
try:
    with open(filename, 'w') as file:
        file.write(time_string)
    print(f"Time written to {filename}")
except Exception as e:
    print(f"Error writing to file: {e}")
