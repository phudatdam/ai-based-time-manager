export PYTHONIOENCODING=utf-8
python3 -m src.cli \
        --work_start_hour 8 \
        --work_end_hour 23 \
        --min_buffer_minutes 15 \
        --slot_duration_minutes 30 \
        --group_by_project True <<EOF
1,Hoàn thành báo cáo dự án A,120,HIGH,2025-09-15T00:00:00,, ,ProjectA,,
2,Chuẩn bị slide thuyết trình,90,CRITICAL,2025-09-16T00:00:00,morning,, ,,,
3,Kiểm tra email và trả lời,45,MEDIUM,,,,,,
4,Nghiên cứu tính năng mới,60,MEDIUM,2025-09-17T00:00:00,, ,ProjectB,,
5,Đi gặp khách hàng,180,HIGH,2025-09-14T05:00:00,afternoon,,ClientX,,
6,Dọn dẹp bàn làm việc,15,LOW,,,,,,
7,Họp nhóm hàng tuần,60,HIGH,2025-09-16T00:00:00,,, , ,2025-09-14T10:00:00,2025-09-14T11:00:00
done
EOF

