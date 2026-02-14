import os
import zipfile

# الهيكلية
structure = {
    "video_after_process": [],
    "models": [],
    "utils": ["roi_config.py", "helpers.py"],
    "processing": ["tracker.py", "process_camera.py"],
    "pages": ["home.py", "camera_analysis.py", "statistics.py"],
    "outputs": [],
    "requirements.txt": None,
    "app.py": None
}

# إنشاء الملفات والمجلدات بأمان
for key, value in structure.items():
    if isinstance(value, list):
        # إنشاء المجلد الرئيسي أولًا
        os.makedirs(key, exist_ok=True)
        for item in value:
            filepath = os.path.join(key, item)
            with open(filepath, "w") as f:
                f.write(f"# Placeholder for {item}\n")
    else:
        # ملف عادي في الجذر
        with open(key, "w") as f:
            f.write(f"# Placeholder for {key}\n")

# ضغط المشروع بالكامل
zip_filename = "gasstation_project.zip"
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".zip"):
                continue
            filepath = os.path.join(root, file)
            arcname = os.path.relpath(filepath, ".")
            zipf.write(filepath, arcname)

print(f"✅ المشروع جاهز ومضغوط: {zip_filename}")