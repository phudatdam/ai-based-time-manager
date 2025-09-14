import argparse
import datetime
from src.models import Task, Priority


def parse_args(raw_args=None):
    parser = argparse.ArgumentParser(description='Time-manager')
    parser.add_argument('--work_start_hour', type=int, default=9)
    parser.add_argument('--work_end_hour', type=int, default=17)
    parser.add_argument('--min_buffer_minutes', type=int, default=15)
    parser.add_argument('--slot_duration_minutes', type=int, default=30)
    parser.add_argument('--group_by_project', type=bool, default=True)
    args = parser.parse_args(raw_args)
    return {
        "work_start_hour": getattr(args, "work_start_hour", 9),
        "work_end_hour": getattr(args, "work_end_hour", 17),
        "min_buffer_minutes": getattr(args, "min_buffer_minutes", 15),
        "slot_duration_minutes": getattr(args, "slot_duration_minutes", 30),
        "group_by_project": getattr(args, "group_by_project", True)
    }

def parse_tasks(input_data):
    """
    Parse tasks from a string (single line) or from a file.
    Format: id,description,duration,priority,due_date,preferred_time,energy_level,project_id,scheduled_start,scheduled_end
    Only id, description, duration, priority are required. Others are optional.
    """
    tasks = []
    if isinstance(input_data, str) and input_data.endswith('.txt'):
        with open(input_data, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    elif isinstance(input_data, str):
        lines = [input_data]
    else:
        return []
    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        if len(parts) < 4:
            continue
        try:
            id = int(parts[0])
            description = parts[1]
            duration_minutes = int(parts[2])
            priority = Priority[parts[3].upper()]
            due_date = None
            preferred_time = None
            energy_level = None
            project_id = None
            scheduled_start = None
            scheduled_end = None
            if len(parts) > 4 and parts[4]:
                due_date = datetime.datetime.fromisoformat(parts[4])
            if len(parts) > 5 and parts[5]:
                preferred_time = parts[5]
            if len(parts) > 6 and parts[6]:
                energy_level = parts[6]
            if len(parts) > 7 and parts[7]:
                project_id = parts[7]
            if len(parts) > 8 and parts[8]:
                scheduled_start = datetime.datetime.fromisoformat(parts[8])
            if len(parts) > 9 and parts[9]:
                scheduled_end = datetime.datetime.fromisoformat(parts[9])
            task = Task(
                id=id,
                description=description,
                duration_minutes=duration_minutes,
                priority=priority,
                due_date=due_date,
                preferred_time=preferred_time,
                energy_level=energy_level,
                project_id=project_id,
                scheduled_start=scheduled_start,
                scheduled_end=scheduled_end
            )
            tasks.append(task)
        except Exception:
            continue
    return tasks if len(tasks) > 1 else (tasks[0] if tasks else None)
