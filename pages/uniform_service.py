import streamlit as st
import os
import pandas as pd
from processing.uniform_pipeline import process_uniform_video, WaitingZone
from processing.roi_config import UNIFORM_ROI_DICT
import cv2
st.set_page_config(page_title="Uniform Service", layout="wide")
st.title("👕 Uniform Service Analysis")

# -----------------------------
# اختيار الكاميرا
# -----------------------------
camera = st.selectbox("Select Camera", ["Camera2", "Camera13", "Camera17"])

# -----------------------------
# رفع الفيديو
# -----------------------------
uploaded_file = st.file_uploader(f"Upload video for {camera}", type=["mp4"])

if uploaded_file:
    os.makedirs("video_after_process", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # الاحتفاظ باسم الفيديو الأساسي
    if "uniform_video_base" not in st.session_state:
        st.session_state.uniform_video_base = os.path.splitext(uploaded_file.name)[0]

    base_name = st.session_state.uniform_video_base
    video_path = os.path.join("video_after_process", uploaded_file.name)

    if not os.path.exists(video_path):
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"{uploaded_file.name} uploaded for {camera}")
    else:
        st.info("Video already uploaded")

    # -----------------------------
    # إعداد ROIs للكاميرا
    # -----------------------------
    rois_relative = UNIFORM_ROI_DICT.get(camera, [])
    
    # نحتاج لمعرفة أبعاد الفيديو لعمل WaitingZone
    cap = cv2.VideoCapture(video_path)
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    rois = [WaitingZone(r, frame_w, frame_h) for r in rois_relative]

    # -----------------------------
    # مسارات الملفات
    # -----------------------------
    summary_csv = os.path.join("outputs", f"{camera}_uniform_summary.csv")
    output_video = os.path.join("video_after_process", f"{base_name}_uniform_processed.mp4")

    # -----------------------------
    # معالجة الفيديو
    # -----------------------------
    with st.spinner("⏳ Processing uniform detection… please wait"):
        process_uniform_video(
            video_path=video_path,
            output_video=output_video,
            summary_csv=summary_csv,
            rois=rois
        )
    st.success("✅ Uniform processing finished!")

    # -----------------------------
    # عرض الفيديو المعالج
    # -----------------------------
    st.subheader("🎥 Processed Video")
    video_file = open(output_video, "rb").read()

    st.download_button(
        "Download Processed Video",
        data=video_file,
        file_name=f"{base_name}_uniform_processed.mp4",
        mime="video/mp4"
    )

    # -----------------------------
    # عرض جدول التحليلات
    # -----------------------------
    if os.path.exists(summary_csv):
        st.subheader("📊 Uniform Summary")
        df_summary = pd.read_csv(summary_csv)
        st.dataframe(df_summary)

        # عرض الرسوم البيانية
        st.subheader("📈 Visualization")
        col1, col2 = st.columns(2)
        col1.metric("Total Persons", int(df_summary['total_person'][0]))
        col2.metric("Total Uniforms", int(df_summary['total_uniform'][0]))
        st.progress(min(int(df_summary['compliance_rate'][0]), 100))

    else:
        st.warning("Summary CSV not found")