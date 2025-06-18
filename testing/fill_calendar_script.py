import pandas as pd
from datetime import datetime, timedelta
import random
import os

# Define sample days and sample events
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
sample_event_names = [
    'Team Meeting', 'Gym Workout', 'Study Session', 'Coffee with Sarah',
    'Doctor Appointment', 'Project Brainstorm', 'Lunch Break', 'Coding Sprint',
    'Grocery Shopping', 'Evening Walk'
]
descriptions = [
    'Bring notebook', 'Discuss timeline', 'Cardio day', 'Catch up with Sarah',
    'Don’t forget reports', 'Ideation for new features', 'Quick lunch', 
    'Backend implementation', 'Buy veggies and fruits', 'Walk around the block'
]

# Generate sample data
events = []
for day in days:
    num_events = random.randint(2, 4)  # 2 to 4 events per day
    start_hour = 8
    for _ in range(num_events):
        event_name = random.choice(sample_event_names)
        start_time_hour = random.randint(start_hour, 18)
        start_time_minute = random.choice([0, 15, 30, 45])
        duration = random.choice([30, 45, 60, 90])
        end_time = datetime(2000, 1, 1, start_time_hour, start_time_minute) + timedelta(minutes=duration)
        if end_time.hour >= 22:  # prevent late night events
            continue
        event = {
            "day": day,
            "event_name": event_name,
            "start_time": f"{start_time_hour:02}:{start_time_minute:02}",
            "end_time": end_time.strftime("%H:%M"),
            "duration_minutes": duration,
            "description": random.choice(descriptions)
        }
        events.append(event)

# Create dataframe
df = pd.DataFrame(events)

# Save CSV
output_path = "sample_calendar_week.csv"
df.to_csv(output_path, index=False)