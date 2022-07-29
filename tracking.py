from datetime import datetime

def track_standing():
    with open('tracking.txt', 'a') as f:
        f.write(f'STANDING, {datetime.now()}\n')

def track_sitting():
    with open('tracking.txt', 'a') as f:
        f.write(f'SITTING, {datetime.now()}\n')