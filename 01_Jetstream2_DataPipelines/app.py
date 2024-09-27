import streamlit as st
import cv2
import os
import tempfile

def process_video(video_file, output_dir):
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(video_file.read())
    
    vcap = cv2.VideoCapture(tfile.name)
    frame_count = 0
    while True:
        ret, frame = vcap.read()
        if not ret:
            break
        output_path = os.path.join(output_dir, f'frame_{frame_count:04d}.jpg')
        cv2.imwrite(output_path, frame)
        frame_count += 1
    vcap.release()
    os.unlink(tfile.name)
    return frame_count

st.title('Video Frame Extractor')

uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'mov', 'avi'])

if uploaded_file is not None:
    output_dir = st.text_input('Output directory', '/app/data')
    if st.button('Process Video'):
        with st.spinner('Processing video...'):
            frame_count = process_video(uploaded_file, output_dir)
        st.success(f'Video processed! Extracted {frame_count} frames to {output_dir}')

st.write("Processed frames will be available in Label Studio for annotation.")
