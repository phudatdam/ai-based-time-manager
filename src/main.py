# gọi file chính để chạy scripts
import argparse
import os
import datetime
from src.Scheduler.AIscheduler import TodoListAIScheduler
from src.model import Task, TimeSlot, Priority
from src.Scheduler.scheduler import SlotScore, SlotScorer

def main(args):
    #os.makedirs(args.output_dir, exist_ok=True)

    print('Args:')
    for k, v in sorted(vars(args).items()):
        print('\t{}: {}'.format(k, v))
    
    #--- xử lí input ---
    scheduler_settings = {
        "work_start_hour": args.work_start_hour,
        "work_end_hour": args.work_end_hour,
        "min_buffer_minutes": args.min_buffer_minutes,
        "slot_duration_minutes": args.slot_duration_minutes,
        "group_by_project": args.group_by_project
    }
    
    #--- chạy schedule ---
    scheduler = TodoListAIScheduler(settings=scheduler_settings)
    
    
    # Thêm các công việc
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    task1 = Task(id=1, description="Hoàn thành báo cáo dự án A", duration_minutes=120, priority=Priority.HIGH, due_date=today + datetime.timedelta(days=1),project_id="ProjectA")
    task2 = Task(id=2, description="Chuẩn bị slide thuyết trình", duration_minutes=90, priority=Priority.CRITICAL, due_date=today + datetime.timedelta(days=2), preferred_time="morning")
    task3 = Task(id=3, description="Kiểm tra email và trả lời", duration_minutes=45, priority=Priority.MEDIUM, energy_level="medium")
    task4 = Task(id=4, description="Nghiên cứu tính năng mới", duration_minutes=60, priority=Priority.MEDIUM, due_date=today + datetime.timedelta(days=3), project_id="ProjectB")
    task5 = Task(id=5, description="Đi gặp khách hàng", duration_minutes=180, priority=Priority.HIGH, due_date=today + datetime.timedelta(hours=5), preferred_time="afternoon", project_id="ClientX") # Giả định là task ngoài giờ làm việc cần xử lý
    task6 = Task(id=6, description="Dọn dẹp bàn làm việc", duration_minutes=15, priority=Priority.LOW)
    task7 = Task(id=7, description="Họp nhóm hàng tuần", duration_minutes=60, priority=Priority.HIGH, due_date=today + datetime.timedelta(days=2), scheduled_start=today.replace(hour=10, minute=0), scheduled_end=today.replace(hour=11, minute=0)) # Task đã có lịch

    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_task(task3)
    scheduler.add_task(task4)
    scheduler.add_task(task5)
    scheduler.add_task(task6)
    scheduler.add_task(task7) # Thêm task đã có lịch
    
    #--- print output ---
    # Lên lịch cho ngày hôm nay
    scheduler.schedule_tasks(target_date=today)

    print("\n--- Lịch trình cho ngày hôm nay ---")
    schedule = scheduler.get_schedule_for_date(today)
    if schedule:
        for task in schedule:
            print(f"- {task.scheduled_start.strftime('%H:%M')} - {task.scheduled_end.strftime('%H:%M')}: {task.description} (Ưu tiên: {task.priority.name})")
    else:
        print("Không có công việc nào được lên lịch.")

    # In ra trạng thái cuối cùng của tất cả các task
    print("\n--- Trạng thái cuối cùng của các task ---")
    for task in scheduler.tasks:
        status = f"lúc {task.scheduled_start.strftime('%Y-%m-%d %H:%M')} - {task.scheduled_end.strftime('%H:%M')}" if task.scheduled_start else "Chưa lên lịch"
        print(f"- {task.description}: {status}")    

def parse_args(raw_args=None):
    parser = argparse.ArgumentParser(description='Time-manager')
    parser.add_argument('--work_start_hour', type=int, default=9)
    parser.add_argument('--work_end_hour', type=int, default=17)
    parser.add_argument('--min_buffer_minutes', type=int, default=15)
    parser.add_argument('--slot_duration_minutes', type=int, default=30)
    parser.add_argument('--group_by_project', type=bool, default=True)
    
    
    args = parser.parse_args(raw_args)
    return args
    

if __name__ == "__main__":
    args = parse_args()
    main(args)    
