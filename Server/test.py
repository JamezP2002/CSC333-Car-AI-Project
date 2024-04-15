from datetime import datetime
import pytz

# Specify the Eastern Time Zone
eastern = pytz.timezone('America/New_York')

# Get the current time in Eastern Time Zone
now = datetime.now(eastern).strftime("%Y-%m-%d %H:%M:%S")

print(now)