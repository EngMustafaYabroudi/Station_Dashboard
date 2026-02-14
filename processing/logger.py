import csv
import os

class CSVLogger:
    def __init__(self, details_csv, summary_csv):
        self.details_csv = details_csv
        self.summary_csv = summary_csv
        self.detail_fields = ["car_id", "color", "enter_time_sec", "exit_time_sec", "waiting_time_sec"]

        # إذا الملف موجود لا تكتب الهيدر، إذا مش موجود اكتب الهيدر
        if not os.path.exists(details_csv):
            with open(details_csv, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.detail_fields)
                writer.writeheader()

        # لا تمسح summary عند كل فيديو
        if not os.path.exists(summary_csv):
            with open(summary_csv, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["cars_served", "average_wait_time_sec"])
                writer.writeheader()

    def log_detail(self, row):
        with open(self.details_csv, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.detail_fields)
            writer.writerow(row)

    def log_summary(self, row):
        # نضيف الصف الجديد بدل أن نحذف القديم
        with open(self.summary_csv, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            writer.writerow(row)