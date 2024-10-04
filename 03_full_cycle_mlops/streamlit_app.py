import streamlit as st
import zipfile
import os

def main():
    st.title("House Image Upload")
    uploaded_file = st.file_uploader("Choose a ZIP file", type="zip")
    if uploaded_file is not None:
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            zip_ref.extractall("uploaded_images")
        st.success("Images uploaded successfully!")

if __name__ == "__main__":
    main()