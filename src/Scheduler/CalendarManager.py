import datetime
from typing import List
from src.models import Task, TimeSlot


class CalendarManager:
    def __init__(self, work_start_hour: int = 9, work_end_hour: int = 17, buffer_minutes: int = 15):
        self.work_start_hour = work_start_hour
        self.work_end_hour = work_end_hour
        self.buffer_minutes = buffer_minutes
        self.current_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    def get_available_slots(self, start_time: datetime.datetime, end_time: datetime.datetime,
                            tasks_scheduled_today: List[Task]) -> List[TimeSlot]:
        """
        Tìm các khoảng thời gian trống trong một khoảng thời gian cho trước,
        loại trừ các khoảng đã có task.
        """
        all_slots = self.generate_potential_slots(start_time, end_time)
        available_slots = []
        
        # Sắp xếp các task đã lên lịch theo thời gian bắt đầu để dễ xử lý
        tasks_scheduled_today.sort(key=lambda t: t.scheduled_start)

        current_cursor = start_time
        task_idx = 0

        for slot in all_slots:
            # Bỏ qua các slot đã bị chiếm dụng bởi task đã lên lịch
            while task_idx < len(tasks_scheduled_today) and \
                  tasks_scheduled_today[task_idx].scheduled_start and \
                  tasks_scheduled_today[task_idx].scheduled_end and \
                  tasks_scheduled_today[task_idx].scheduled_start < slot.end and \
                  tasks_scheduled_today[task_idx].scheduled_end > slot.start:
                task_idx += 1
            
            # Kiểm tra xem slot có hoàn toàn nằm trong khoảng thời gian làm việc không
            slot_start_in_work_hours = self.work_start_hour <= slot.start.hour < self.work_end_hour
            slot_end_in_work_hours = self.work_start_hour <= slot.end.hour < self.work_end_hour

            # Chỉ xem xét các slot nằm hoàn toàn trong giờ làm việc (hoặc một phần)
            if slot_start_in_work_hours or slot_end_in_work_hours:
                # Tinh chỉnh slot nếu nó chỉ một phần nằm trong giờ làm việc
                actual_start = max(slot.start, start_time.replace(hour=self.work_start_hour, minute=0, second=0))
                actual_end = min(slot.end, start_time.replace(hour=self.work_end_hour, minute=0, second=0))

                if actual_start < actual_end: # Đảm bảo có khoảng thời gian hợp lệ
                    adjusted_slot = TimeSlot(actual_start, actual_end)
                    
                    # Kiểm tra lại xem slot này có còn bị chiếm dụng không sau khi điều chỉnh
                    is_occupied = False
                    for t in tasks_scheduled_today:
                        if t.scheduled_start and t.scheduled_end:
                            if max(adjusted_slot.start, t.scheduled_start) < min(adjusted_slot.end, t.scheduled_end):
                                is_occupied = True
                                break
                    
                    if not is_occupied and adjusted_slot.duration_minutes >= self.buffer_minutes:
                         available_slots.append(adjusted_slot)
        
        return available_slots

    def generate_potential_slots(self, start_time: datetime.datetime, end_time: datetime.datetime, slot_duration_minutes: int = 60) -> List[TimeSlot]:
        """
        Tạo ra các khoảng thời gian tiềm năng trong một phạm vi cho trước.
        """
        slots = []
        current_time = start_time
        while current_time < end_time:
            next_time = current_time + datetime.timedelta(minutes=slot_duration_minutes)
            if next_time > end_time:
                next_time = end_time
            
            if current_time < next_time: # Đảm bảo có khoảng thời gian hợp lệ
                slots.append(TimeSlot(current_time, next_time))
            current_time = next_time
        return slots
