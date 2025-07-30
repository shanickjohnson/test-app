import streamlit as st

def set_bg_color():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-color: #FF0000;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_color()

# --- Your app's content below ---
st.title("This app has a new background! 🎨")