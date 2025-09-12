CUDA_VISIBLE_DEVICES=1 python3 -m src.main\
        --work_start_hour 8 \
        --work_end_hour 23 \
        --min_buffer_minutes 15 \
        --slot_duration_minutes 30 \
        --group_by_project True
