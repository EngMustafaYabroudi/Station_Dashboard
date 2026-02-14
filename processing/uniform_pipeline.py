import cv2
from ultralytics import YOLO
import pandas as pd
import os

# -----------------------------
# كلاس لتحويل ROI النسبي للبكسل والتحقق
# -----------------------------
class WaitingZone:
    def __init__(self, roi, frame_w, frame_h):
        # roi: (cx, cy, w, h) نسبي
        cx, cy, w, h = roi
        self.roi = (
            int((cx - w/2) * frame_w),
            int((cy - h/2) * frame_h),
            int((cx + w/2) * frame_w),
            int((cy + h/2) * frame_h)
        )

    def contains(self, x, y):
        x1, y1, x2, y2 = self.roi
        return x1 <= x <= x2 and y1 <= y <= y2

# -----------------------------
# الدالة المعدلة لمعالجة الفيديو
# -----------------------------
def process_uniform_video(
    video_path,
    output_video,
    summary_csv,
    rois,  # قائمة من WaitingZone objects
    model_path="models/MU_Station-Uniform_V0.pt",
    conf_th=0.25,
    tracker_cfg="bytetrack.yaml"
):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = cv2.VideoWriter(
        output_video,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (frame_w, frame_h)
    )

    model = YOLO(model_path)

    unique_person_ids = set()
    unique_uniform_ids = set()
    frame_idx = 0

    for r in model.track(
        source=video_path,
        stream=True,
        persist=True,
        tracker=tracker_cfg,
        conf=conf_th
    ):
        frame = r.orig_img.copy()

        # رسم كل منطقة ROI
        for zone in rois:
            x1, y1, x2, y2 = zone.roi
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # التحقق من كل اكتشاف إذا كان داخل أي ROI
        if r.boxes.id is not None:
            for box, tid, cls in zip(r.boxes.xyxy, r.boxes.id, r.boxes.cls):
                tid = int(tid)
                cls = int(cls)
                class_name = model.names[cls]

                box = box.tolist()
                cx = (box[0] + box[2]) / 2
                cy = (box[1] + box[3]) / 2

                if not any(zone.contains(cx, cy) for zone in rois):
                    continue

                if class_name == "person":
                    unique_person_ids.add(tid)
                elif class_name == "uniform":
                    unique_uniform_ids.add(tid)

                color = (255, 0, 0) if class_name == "person" else (0, 0, 255)
                cv2.rectangle(frame, (int(box[0]), int(box[1])),
                              (int(box[2]), int(box[3])), color, 2)
                cv2.putText(frame, f"{class_name} ID {tid}",
                            (int(box[0]), int(box[1]-10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        writer.write(frame)
        frame_idx += 1

    cap.release()
    writer.release()

    # حفظ ملخص العد
    summary_df = pd.DataFrame([{
        "total_person": len(unique_person_ids),
        "total_uniform": len(unique_uniform_ids),
        "compliance_rate": round(
            (len(unique_uniform_ids)/len(unique_person_ids))*100, 2
        ) if unique_person_ids else 0
    }])
    # -----------------------------
    # Final Counts
    # -----------------------------
    total_person = len(unique_person_ids) + len(unique_uniform_ids)
    total_uniform = len(unique_uniform_ids)

    # حساب نسبة الالتزام
    compliance_rate = round((total_uniform / total_person) * 100, 2) if total_person > 0 else 0

    summary_df = pd.DataFrame([{
        "total_person": total_person,
        "total_uniform": total_uniform,
        "compliance_rate": compliance_rate
    }])

  

    os.makedirs(os.path.dirname(summary_csv), exist_ok=True)
    summary_df.to_csv(summary_csv, index=False)

    return summary_csv, output_video