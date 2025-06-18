import pandas as pd
import os
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

BASE_DIR = os.path.dirname(__file__)
calendar_path = os.path.join(BASE_DIR, "sample_calendar_week.csv")
calendar_df = pd.read_csv(calendar_path)

# Function to find available time slots in the calendar
def find_time_slots(event_name: str, duration_minutes: int, description: str = None) -> dict:
    """Finds time slots in the weekly calendar where the event can be scheduled.

    Args:
        event_name (str): Name of the event to schedule.
        duration_minutes (int): Duration of the event in minutes.
        description (str, optional): Optional description of the event.

    Returns:
        dict: status and result or error message.
    """
    if not description:
        description = f"Auto-generated description for {event_name}."

    # Define working hours for each day (8 AM to 10 PM)
    working_start = datetime.time(8, 0)
    working_end = datetime.time(22, 0)
    slot_suggestions = []

    for day in calendar_df['day'].unique():
        day_events = calendar_df[calendar_df['day'] == day]
        # Sort by start_time
        day_events_sorted = day_events.sort_values(by="start_time")

        # Convert event start/end times to datetime.time
        busy_times = []
        for _, row in day_events_sorted.iterrows():
            st = datetime.datetime.strptime(row['start_time'], "%H:%M").time()
            et = datetime.datetime.strptime(row['end_time'], "%H:%M").time()
            busy_times.append((st, et))

        # Look for free slots between 8:00 and 22:00
        current_time = working_start
        for st, et in busy_times:
            slot_start = datetime.datetime.combine(datetime.date.today(), current_time)
            slot_end = datetime.datetime.combine(datetime.date.today(), st)
            slot_duration = (slot_end - slot_start).total_seconds() / 60

            if slot_duration >= duration_minutes:
                slot_suggestions.append({
                    "day": day,
                    "start_time": current_time.strftime("%H:%M"),
                    "end_time": st.strftime("%H:%M"),
                    "available_duration": int(slot_duration),
                    "note": f"Available for {event_name} - {description}"
                })

            current_time = et

        # After last event until working_end
        slot_start = datetime.datetime.combine(datetime.date.today(), current_time)
        slot_end = datetime.datetime.combine(datetime.date.today(), working_end)
        slot_duration = (slot_end - slot_start).total_seconds() / 60

        if slot_duration >= duration_minutes:
            slot_suggestions.append({
                "day": day,
                "start_time": current_time.strftime("%H:%M"),
                "end_time": working_end.strftime("%H:%M"),
                "available_duration": int(slot_duration),
                "note": f"Available for {event_name} - {description}"
            })

    return {
        "status": "success" if slot_suggestions else "error",
        "slots": slot_suggestions if slot_suggestions else [],
        "error_message": None if slot_suggestions else "No suitable time slots found for the event."
    }

# Define the agent
schedule_agent = Agent(
    name="calendar_scheduler",
    model="gemini-2.0-flash",
    description="Agent to find free time slots in the weekly calendar for scheduling new events.",
    instruction="You help users find the best times to add a new event to their weekly schedule.",
    tools=[find_time_slots],
)
