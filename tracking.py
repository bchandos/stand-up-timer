from datetime import date, datetime
from dateutil.parser import parse

def track_standing(standing: bool):
    with open('tracking.txt', 'a') as f:
        f.write(f'STANDING {"START" if standing else "END"},{datetime.now()}\n')

def get_todays_standing_time() -> int:
    with open('tracking.txt', 'r') as f:
        activities = f.readlines()
    t = date.today()
    cummulative_time = 0
    last_start = None
    for activity in activities:
        try:
            action, time = activity.split(',')
        except ValueError:
            continue
        if parse(time).date() == t:
            if action == 'STANDING START':
                last_start = parse(time)
            elif action == 'STANDING END' and last_start:
                time_diff = parse(time) - last_start
                cummulative_time += time_diff.seconds
                last_start = None
    if last_start:
        time_diff = datetime.now() - last_start
        cummulative_time += time_diff.seconds
    
    return cummulative_time
