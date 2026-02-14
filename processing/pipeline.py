# import cv2
# from ultralytics import YOLO
# from .zones import WaitingZone
# from .color import CarColorExtractor
# from .tracker import CarTrackerManager
# from .logger import CSVLogger

# def process_video(
#     video_path,
#     output_video,
#     details_csv,
#     summary_csv,
#     service_zone=(0.498687, 0.644583, 0.994500, 0.700833),
#     model_path="models/MU_Station-Car-Detection_V2.pt",
#     conf_th=0.25,
#     tracker_cfg="bytetrack.yaml"
# ):
#     cap = cv2.VideoCapture(video_path)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     writer = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

#     zone = WaitingZone(service_zone, w, h)
#     logger = CSVLogger(details_csv, summary_csv)
#     color_extractor = CarColorExtractor()
#     tracker = CarTrackerManager(zone, logger, color_extractor)

#     model = YOLO(model_path)
#     frame_idx = 0

#     for r in model.track(source=video_path, stream=True, persist=True, tracker=tracker_cfg, conf=conf_th):
#         frame = r.orig_img
#         time_sec = frame_idx / fps
#         active_ids = set()

#         # رسم ROI فقط
#         x1, y1, x2, y2 = zone.roi
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

#         # التتبع فقط للـ boxes الموجودة
#         if r.boxes.id is not None:
#             for box, tid in zip(r.boxes.xyxy, r.boxes.id):
#                 tid = int(tid)
#                 active_ids.add(tid)
#                 box = box.tolist()
#                 tracker.update(tid, box, frame, time_sec)

#                 wait = tracker.get_wait_time(tid, time_sec)
#                 wait_txt = f"WAIT: {wait:.1f}s" if wait else ""

#                 # رسم صندوق السيارة
#                 cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 0, 0), 2)
#                 cv2.putText(frame, f"ID {tid} | {tracker.cars[tid]['color']}",
#                             (int(box[0]), int(box[1]-25)),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
#                 if wait_txt:
#                     cv2.putText(frame, wait_txt, (int(box[0]), int(box[1]-5)),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

#         tracker.handle_lost(active_ids, time_sec)
#         writer.write(frame)
#         frame_idx += 1

#     cap.release()
#     writer.release()
#     tracker.finalize(frame_idx / fps)

#     return details_csv, summary_csv, output_video
import cv2
from ultralytics import YOLO
from .zones import WaitingZone
from .color import CarColorExtractor
from .tracker import CarTrackerManager
from .logger import CSVLogger

def process_video(
    video_path,
    output_video,
    details_csv,
    summary_csv,
    service_zone=(0.498687, 0.644583, 0.994500, 0.700833),
    model_path="models/MU_Station-Car-Detection_V2.pt",
    conf_th=0.25,
    tracker_cfg="bytetrack.yaml"
):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    zone = WaitingZone(service_zone, w, h)
    logger = CSVLogger(details_csv, summary_csv)
    color_extractor = CarColorExtractor()
    tracker = CarTrackerManager(zone, logger, color_extractor)

    model = YOLO(model_path)
    frame_idx = 0

    for r in model.track(source=video_path, stream=True, persist=True,
                         tracker=tracker_cfg, conf=conf_th):
        frame = r.orig_img.copy()
        time_sec = frame_idx / fps
        active_ids = set()

        # رسم الـROI على الفيديو
        x1, y1, x2, y2 = zone.roi
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if r.boxes.id is not None:
            for box, tid in zip(r.boxes.xyxy, r.boxes.id):
                tid = int(tid)
                cx, cy = int((box[0]+box[2])/2), int((box[1]+box[3])/2)

                # 🚗 فقط السيارات داخل الـROI
                if zone.contains(cx, cy):
                    active_ids.add(tid)
                    box = box.tolist()
                    tracker.update(tid, box, frame, time_sec)
                    wait = tracker.get_wait_time(tid, time_sec)

                    # رسم الـbbox والـtext
                    cv2.rectangle(frame, (int(box[0]), int(box[1])),
                                  (int(box[2]), int(box[3])), (255, 0, 0), 2)
                    text = f"ID {tid} | {tracker.cars[tid]['color']}"
                    if wait:
                        text += f" | WAIT {wait:.1f}s"
                    cv2.putText(frame, text, (int(box[0]), int(box[1]-10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        tracker.handle_lost(active_ids, time_sec)
        writer.write(frame)
        frame_idx += 1

    cap.release()
    writer.release()
    tracker.finalize(frame_idx / fps)
    return details_csv, summary_csv, output_video