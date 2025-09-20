import datetime
from typing import List, Dict, Optional
from src.models import Task, TimeSlot
from src.scheduler.CalendarManager import CalendarManager
from src.scheduler.SlotScorer import SlotScorer


class GreedyScheduler:
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

        # Chuẩn bị dữ liệu cho ngày cần lên lịch
        pending_tasks = [task for task in self.tasks if task.scheduled_start is None]
        tasks_already_scheduled_today = [task for task in self.tasks if task.scheduled_start and task.scheduled_start.date() == target_date.date()]

        # Sắp xếp các task chờ xử lý theo độ ưu tiên và deadline
        pending_tasks.sort(key=lambda t: (-t.priority.value, t.due_date if t.due_date else datetime.datetime.max))

        # Cập nhật thông tin dự án cho SlotScorer
        self.slot_scorer.update_scheduled_tasks_for_projects(tasks_already_scheduled_today)

        # Lấy các khoảng liên tục còn trống trong ngày
        search_start = target_date
        search_end = target_date + datetime.timedelta(days=1)
        stride_minutes = 15  # default stride

        # Duyệt qua các task và tìm sub-interval tốt nhất
        for task in pending_tasks:
            available_intervals = self.calendar_manager.get_available_intervals(
                search_start, search_end, tasks_already_scheduled_today
            )
            best_sub_interval: Optional[TimeSlot] = None
            best_score: float = -1.0
            candidate_sub_intervals = []
            for interval in available_intervals:
                if interval.duration_minutes >= task.duration_minutes:
                    subs = self.calendar_manager.generate_sub_intervals(
                        interval, task.duration_minutes, stride_minutes
                    )
                    candidate_sub_intervals.extend(subs)
            if not candidate_sub_intervals:
                print(f"Không tìm thấy đủ chỗ trống cho task: {task.description} (cần {task.duration_minutes} phút).")
                continue
            for sub in candidate_sub_intervals:
                score = self.slot_scorer.score_slot(sub, task)
                if score.total > best_score:
                    best_score = score.total
                    best_sub_interval = sub
            if best_sub_interval:
                task.scheduled_start = best_sub_interval.start
                task.scheduled_end = best_sub_interval.end
                tasks_already_scheduled_today.append(task)
                self.scheduled_tasks.append(task)
                print(f"Đã lên lịch: {task.description} vào lúc {task.scheduled_start.strftime('%H:%M')} - {task.scheduled_end.strftime('%H:%M')} (Score: {best_score:.2f})")
            else:
                print(f"Không tìm thấy slot phù hợp cho task: {task.description}")
    
    def get_schedule_for_date(self, date: datetime.datetime) -> List[Task]:
        return sorted(
            [task for task in self.tasks if task.scheduled_start and task.scheduled_start.date() == date.date()],
            key=lambda t: t.scheduled_start
        )
