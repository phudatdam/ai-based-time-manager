export PYTHONIOENCODING=utf-8
python3 -c "
import datetime
today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
print(f'1,Hoàn thành báo cáo dự án A,120,HIGH,{(today + datetime.timedelta(days=1)).isoformat()},,,ProjectA,,')
print(f'2,Chuẩn bị slide thuyết trình,90,CRITICAL,{(today + datetime.timedelta(days=2)).isoformat()},morning,,,,')
print(f'3,Kiểm tra email và trả lời,45,MEDIUM,,,,,,')
print(f'4,Nghiên cứu tính năng mới,60,MEDIUM,{(today + datetime.timedelta(days=3)).isoformat()},,,ProjectB,,')
print(f'5,Đi gặp khách hàng,180,HIGH,{(today + datetime.timedelta(hours=5)).isoformat()},afternoon,,ClientX,,')
print(f'6,Dọn dẹp bàn làm việc,15,LOW,,,,,,')
print(f'7,Họp nhóm hàng tuần,60,HIGH,{(today + datetime.timedelta(days=2)).isoformat()},,,,{today.replace(hour=10,minute=0).isoformat()},{today.replace(hour=11,minute=0).isoformat()}')
print('done')
" | python3 -m src.cli --work_start_hour 8 --work_end_hour 23 --min_buffer_minutes 15 --slot_duration_minutes 30 --group_by_project True