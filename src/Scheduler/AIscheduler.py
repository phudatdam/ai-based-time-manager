import datetime
from typing import List, Dict, Optional, Tuple
from src.model import Task, TimeSlot
from src.Scheduler.scheduler import CalendarManager, SlotScore, SlotScorer

# --- AI Agent ---

class TodoListAIScheduler:
    def __init__(self, settings: Optional[Dict] = None):
        if settings is None:
            settings = {
                "work_start_hour": 9,
                "work_end_hour": 17,
                "min_buffer_minutes": 15,
                "slot_duration_minutes": 30, # Thời gian quét để tìm slot trống
                "group_by_project": True
            }
        self.settings = settings
        self.calendar_manager = CalendarManager(
            work_start_hour=settings.get("work_start_hour", 9),
            work_end_hour=settings.get("work_end_hour", 17),
            buffer_minutes=settings.get("min_buffer_minutes", 15)
        )
        self.slot_scorer = SlotScorer(settings)
        self.tasks: List[Task] = []
        self.scheduled_tasks: List[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def schedule_tasks(self, target_date: Optional[datetime.datetime] = None):
        if target_date is None:
            target_date = self.current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            self.current_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # 1. Chuẩn bị dữ liệu cho ngày cần lên lịch
        # Lấy các task chưa được lên lịch
        pending_tasks = [task for task in self.tasks if task.scheduled_start is None]
        # Lấy các task đã lên lịch trong ngày hôm nay (nếu có)
        tasks_already_scheduled_today = [task for task in self.tasks if task.scheduled_start and task.scheduled_start.date() == target_date.date()]

        # 2. Sắp xếp các task chờ xử lý theo độ ưu tiên và deadline
        pending_tasks.sort(key=lambda t: (t.priority.value, t.due_date if t.due_date else datetime.datetime.max), reverse=True)

        # 3. Cập nhật thông tin dự án cho SlotScorer
        self.slot_scorer.update_scheduled_tasks_for_projects(tasks_already_scheduled_today)

        # 4. Duyệt qua các task và tìm slot tốt nhất
        for task in pending_tasks:
            best_slot: Optional[TimeSlot] = None
            best_score: float = -1.0
            
            # Lấy các slot trống trong ngày
            search_start = target_date
            search_end = target_date + datetime.timedelta(days=1)
            available_slots = self.calendar_manager.get_available_slots(
                search_start, search_end, tasks_already_scheduled_today
            )

            # Lọc các slot đủ lớn cho task
            suitable_slots = [slot for slot in available_slots if slot.duration_minutes >= task.duration_minutes]
            
            if not suitable_slots:
                print(f"Không tìm thấy đủ chỗ trống cho task: {task.description} (cần {task.duration_minutes} phút).")
                continue

            # Tìm slot có điểm cao nhất
            for slot in suitable_slots:
                score = self.slot_scorer.score_slot(slot, task)
                if score.total > best_score:
                    best_score = score.total
                    best_slot = slot
            
            # Lên lịch task vào slot tốt nhất nếu tìm thấy
            if best_slot:
                task.scheduled_start = best_slot.start
                task.scheduled_end = best_slot.start + datetime.timedelta(minutes=task.duration_minutes)
                tasks_already_scheduled_today.append(task) # Thêm task vừa lên lịch vào danh sách hôm nay
                self.scheduled_tasks.append(task)
                print(f"Đã lên lịch: {task.description} vào lúc {task.scheduled_start.strftime('%H:%M')} - {task.scheduled_end.strftime('%H:%M')} (Score: {best_score:.2f})")
            else:
                print(f"Không tìm thấy slot phù hợp cho task: {task.description}")
        
        # Cập nhật lại danh sách tasks chính
        self.tasks = [t for t in self.tasks if t.scheduled_start is not None] + pending_tasks # Kết hợp task đã có và task mới lên lịch

    def get_schedule_for_date(self, date: datetime.datetime) -> List[Task]:
        return sorted(
            [task for task in self.tasks if task.scheduled_start and task.scheduled_start.date() == date.date()],
            key=lambda t: t.scheduled_start
        )
