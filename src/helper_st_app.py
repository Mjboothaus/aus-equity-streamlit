import streamlit as st


def create_app_header(app_title):
    st.set_page_config(
        page_title=app_title,
        layout="wide",
        menu_items={
            "About":
            "Created with love & care at DataBooth - www.databooth.com.au"
        },
    )
    st.header(app_title)