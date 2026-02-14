import streamlit as st
import os
import pandas as pd
from processing.pipeline import process_video
from processing.roi_config import ROI_DICT

st.set_page_config(page_title="Fuel Service", layout="wide")
st.title("⛽ Fuel Service Analysis")

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

    # تثبيت اسم الفيديو مرة واحدة
    if "video_base" not in st.session_state:
        st.session_state.video_base = os.path.splitext(uploaded_file.name)[0]

    base_name = st.session_state.video_base
    video_path = os.path.join("video_after_process", uploaded_file.name)

    if not os.path.exists(video_path):
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"{uploaded_file.name} uploaded for {camera}")
    else:
        st.info("Video already uploaded")

    # ROI حسب الكاميرا
    roi = ROI_DICT.get(camera, (0.5, 0.5, 1.0, 1.0))

    # مسارات المخرجات الموحدة لكل كاميرا + فيديو
    details_csv = os.path.join("outputs", f"{camera}_details.csv")
    summary_csv = os.path.join("outputs", f"{camera}_summary.csv")
    output_video = os.path.join("video_after_process", f"{base_name}_processed.mp4")

    # -----------------------------
    # معالجة الفيديو مباشرة عند رفعه
    # -----------------------------
    with st.spinner("⏳ Processing video… please wait"):
        process_video(
            video_path=video_path,
            output_video=output_video,
            details_csv=details_csv,
            summary_csv=summary_csv,
            service_zone=roi
        )
    st.success("✅ Processing finished!")

    # -----------------------------
    # قراءة CSV وعرضه
    # -----------------------------
    if os.path.exists(details_csv):
        st.subheader("📄 Details Table")
        df = pd.read_csv(details_csv)
        st.dataframe(df)
    else:
        st.warning("Details CSV not found")

    # -----------------------------
    # تحميل الفيديو المعالج
    # -----------------------------
    if os.path.exists(output_video):
        with open(output_video, "rb") as f:
            st.download_button(
                "Download Processed Video",
                data=f,
                file_name=f"{base_name}_processed.mp4",
                mime="video/mp4"
            )