# Placeholder for process_camera.py
import cv2
import os
import csv
from processing.roi_config import ROI_CONFIG
from processing.zones import extract_roi
from processing.tracker import CarTracker

def process_video(camera, input_path, output_dir="video_after_process", csv_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(csv_dir, exist_ok=True)

    # فتح الفيديو
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # فيديو معالج
    out_path = os.path.join(output_dir, f"{camera}_processed.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    # tracker
    tracker = CarTracker()

    # CSV
    csv_path = os.path.join(csv_dir, f"{camera}.csv")
    csv_file = open(csv_path, "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["CarID", "EnterFrame", "ExitFrame", "WaitingTimeFrames"])

    # تخزين دخول السيارات
    car_times = {}

    # ROI
    roi = ROI_CONFIG[camera]

    frame_id = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_id += 1

        roi_frame, (x1, y1, x2, y2) = extract_roi(frame, roi)

        outputs = tracker.process_frame(frame)  # تعديل حسب tracker
        # outputs = list of [x1, y1, x2, y2, track_id]

        for out_box in outputs:
            tid = int(out_box[4])
            # رسم الصندوق على الفيديو
            cv2.rectangle(frame, (out_box[0], out_box[1]), (out_box[2], out_box[3]), (0,255,0), 2)
            cv2.putText(frame, f"ID:{tid}", (out_box[0], out_box[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            # حساب زمن الانتظار
            if tid not in car_times:
                car_times[tid] = frame_id  # وقت الدخول
            else:
                pass  # يمكن تحديث وقت الخروج عند الخروج لاحقًا

        out.write(frame)

    # كتابة CSV
    for tid, enter_frame in car_times.items():
        exit_frame = frame_id
        waiting_time = exit_frame - enter_frame
        csv_writer.writerow([tid, enter_frame, exit_frame, waiting_time])

    csv_file.close()
    cap.release()
    out.release()
    print(f"✅ Done processing {camera}. Video saved to {out_path}, CSV saved to {csv_path}")