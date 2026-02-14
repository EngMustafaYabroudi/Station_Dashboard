from .zones import WaitingZone

# def bbox_center(box):
#     x1, y1, x2, y2 = map(int, box)
#     return int((x1+x2)/2), int((y1+y2)/2)

# class CarTrackerManager:
#     def __init__(self, zone, logger, color_extractor):
#         self.zone = zone
#         self.logger = logger
#         self.color_extractor = color_extractor
#         self.cars = {}
#         self.completed_waits = []

#     def update(self, car_id, bbox, frame, time_sec):
#         cx, cy = bbox_center(bbox)
#         inside = self.zone.contains(cx, cy)

#         if car_id not in self.cars:
#             self.cars[car_id] = {
#                 "color": self.color_extractor.extract(frame, bbox),
#                 "enter_time": None,
#                 "inside": False
#             }

#         car = self.cars[car_id]

#         # 🚗 دخول السيارة
#         if inside and not car["inside"]:
#             car["enter_time"] = time_sec
#             car["inside"] = True

#         # 🚗 خروج السيارة → سجل CSV
#         elif not inside and car["inside"]:
#             exit_time = time_sec
#             wait = exit_time - car["enter_time"]
#             self.completed_waits.append(wait)

#             self.logger.log_detail({
#                 "car_id": car_id,
#                 "color": car["color"],
#                 "enter_time_sec": round(car["enter_time"], 2),
#                 "exit_time_sec": round(exit_time, 2),
#                 "waiting_time_sec": round(wait, 2)
#             })

#             car["inside"] = False
#             car["enter_time"] = None

#     def handle_lost(self, active_ids, time_sec):
#         # إذا اختفت السيارة فجأة خارج ROI
#         for cid, car in self.cars.items():
#             if car["inside"] and cid not in active_ids:
#                 self.update(cid, (0,0,0,0), None, time_sec)  # استخدم update لمحاكاة خروج

#     def get_wait_time(self, car_id, time_sec):
#         car = self.cars.get(car_id)
#         if not car or car["enter_time"] is None:
#             return None
#         if car["inside"]:
#             return time_sec - car["enter_time"]
#         return None

#     def finalize(self, duration):
#         avg = sum(self.completed_waits)/len(self.completed_waits) if self.completed_waits else 0
#         self.logger.log_summary({
#             "cars_served": len(self.completed_waits),
#             "average_wait_time_sec": round(avg,2)
#         })
# from .zones import WaitingZone

# def bbox_center(box):
#     x1, y1, x2, y2 = map(int, box)
#     return int((x1 + x2) / 2), int((y1 + y2) / 2)

# class CarTrackerManager:
#     def __init__(self, zone, logger, color_extractor):
#         self.zone = zone
#         self.logger = logger
#         self.color_extractor = color_extractor
#         self.cars = {}  # All tracked cars
#         self.completed_waits = []  # Store wait times

#     def update(self, car_id, bbox, frame, time_sec):
#         """
#         Update the car's state:
#         - Entering ROI → start timer
#         - Leaving ROI → log CSV
#         """
#         cx, cy = bbox_center(bbox)
#         inside = self.zone.contains(cx, cy)

#         # New car
#         if car_id not in self.cars:
#             self.cars[car_id] = {
#                 "color": self.color_extractor.extract(frame, bbox),
#                 "enter_time": None,
#                 "inside": False
#             }

#         car = self.cars[car_id]

#         # 🚗 Car enters the ROI
#         if inside and not car["inside"]:
#             car["enter_time"] = time_sec
#             car["inside"] = True

#         # 🚗 Car exits ROI → log CSV
#         elif not inside and car["inside"]:
#             exit_time = time_sec
#             wait = exit_time - car["enter_time"]
#             self.completed_waits.append(wait)

#             self.logger.log_detail({
#                 "car_id": car_id,
#                 "color": car["color"],
#                 "enter_time_sec": round(car["enter_time"], 2),
#                 "exit_time_sec": round(exit_time, 2),
#                 "waiting_time_sec": round(wait, 2)
#             })

#             car["inside"] = False
#             car["enter_time"] = None

#     def handle_lost(self, active_ids, time_sec):
#         """
#         Handle cars that disappeared outside the ROI:
#         - Assume they exited and log their data
#         """
#         for cid, car in self.cars.items():
#             if car["inside"] and cid not in active_ids:
#                 # Simulate exit at current frame
#                 self.update(cid, (0, 0, 0, 0), None, time_sec)

#     def get_wait_time(self, car_id, time_sec):
#         """
#         Get the current wait time for overlay display
#         """
#         car = self.cars.get(car_id)
#         if not car or car["enter_time"] is None:
#             return None
#         if car["inside"]:
#             return time_sec - car["enter_time"]
#         return None

#     def finalize(self, duration):
#         """
#         At the end of the video: log summary
#         - Total cars served
#         - Average wait time
#         Also logs cars still inside ROI at the end
#         """
#         # Log remaining cars still in the ROI
#         for cid, car in self.cars.items():
#             if car["inside"] and car["enter_time"] is not None:
#                 exit_time = duration
#                 wait = exit_time - car["enter_time"]
#                 self.completed_waits.append(wait)
#                 self.logger.log_detail({
#                     "car_id": cid,
#                     "color": car["color"],
#                     "enter_time_sec": round(car["enter_time"], 2),
#                     "exit_time_sec": round(exit_time, 2),
#                     "waiting_time_sec": round(wait, 2)
#                 })
#                 car["inside"] = False
#                 car["enter_time"] = None

#         # Log summary
#         avg = sum(self.completed_waits) / len(self.completed_waits) if self.completed_waits else 0
#         self.logger.log_summary({
#             "cars_served": len(self.completed_waits),
#             "average_wait_time_sec": round(avg, 2)
#         })

from .zones import WaitingZone

def bbox_center(box):
    x1, y1, x2, y2 = map(int, box)
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

class CarTrackerManager:
    def __init__(self, zone, logger, color_extractor):
        self.zone = zone
        self.logger = logger
        self.color_extractor = color_extractor
        self.cars = {}  # active cars in ROI
        self.completed_waits = []

    def update(self, car_id, bbox, frame, time_sec):
        cx, cy = bbox_center(bbox)
        inside = self.zone.contains(cx, cy)

        if car_id not in self.cars:
            self.cars[car_id] = {
                "color": self.color_extractor.extract(frame, bbox) if frame is not None else "Unknown",
                "enter_time": None,
                "inside": False
            }

        car = self.cars[car_id]

        # Car enters ROI
        if inside and not car["inside"]:
            car["enter_time"] = time_sec
            car["inside"] = True

        # Car exits ROI → log CSV
        elif not inside and car["inside"]:
            self._log_car_exit(car_id, time_sec)

    def _log_car_exit(self, car_id, exit_time):
        car = self.cars[car_id]
        wait = exit_time - car["enter_time"]
        self.completed_waits.append(wait)

        self.logger.log_detail({
            "car_id": car_id,
            "color": car["color"],
            "enter_time_sec": round(car["enter_time"], 2),
            "exit_time_sec": round(exit_time, 2),
            "waiting_time_sec": round(wait, 2)
        })

        car["inside"] = False
        car["enter_time"] = None

    def get_wait_time(self, car_id, time_sec):
        """Return current wait time for car if inside ROI, else None."""
        car = self.cars.get(car_id)
        if not car or car["enter_time"] is None:
            return None
        if car["inside"]:
            return time_sec - car["enter_time"]
        return None

    def handle_lost(self, active_ids, time_sec):
        # Simulate exit for lost cars
        for cid, car in self.cars.items():
            if car["inside"] and cid not in active_ids:
                self._log_car_exit(cid, time_sec)

    def finalize(self, duration):
        # Log any car still inside ROI at the end
        for cid, car in self.cars.items():
            if car["inside"]:
                self._log_car_exit(cid, duration)

        # Summary
        avg = sum(self.completed_waits)/len(self.completed_waits) if self.completed_waits else 0
        self.logger.log_summary({
            "cars_served": len(self.completed_waits),
            "average_wait_time_sec": round(avg, 2)
        })