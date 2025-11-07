import datetime
from src.scheduler import AIScheduler
from src.utils import parse_args, parse_tasks


def run_cli():
    # Parse scheduling settings from CLI args
    scheduler_settings = parse_args()
    scheduler = AIScheduler(settings=scheduler_settings)

    # Input tasks interactively or from file
    print("Enter tasks:")
    tasks = []
    while True:
        line = input().strip()
        if line.lower() == "done":
            break
        elif line.lower().startswith("file "):
            filename = line[5:].strip()
            tasks = parse_tasks(filename)
            print(f"Loaded {len(tasks)} tasks from {filename}")
            break
        elif line:
            task = parse_tasks(line)
            if isinstance(task, list):
                tasks.extend(task)
            elif task:
                tasks.append(task)

    for task in tasks:
        scheduler.add_task(task)
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    scheduler.schedule_tasks(target_date=today)

    print("\n--- Lịch trình cho ngày hôm nay ---")
    schedule = scheduler.get_schedule_for_date(today)
    if schedule:
        for task in schedule:
            print(f"- {task.scheduled_start.strftime('%H:%M')} - {task.scheduled_end.strftime('%H:%M')}: {task.description} (Ưu tiên: {task.priority.name})")
    else:
        print("Không có công việc nào được lên lịch.")

    print("\n--- Trạng thái cuối cùng của các task ---")
    for task in scheduler.tasks:
        status = f"lúc {task.scheduled_start.strftime('%Y-%m-%d %H:%M')} - {task.scheduled_end.strftime('%H:%M')}" if task.scheduled_start else "Chưa lên lịch"
        print(f"- {task.description}: {status}")

if __name__ == "__main__":
    run_cli()
