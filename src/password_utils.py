import os
import hashlib
import base64
import streamlit as st
from dotenv import load_dotenv

# Constants for PBKDF2
SALT_LENGTH = 32
ITERATIONS = 100000
KEY_LENGTH = 32

load_dotenv()
PASSWORD = os.getenv('hashed_password')

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(SALT_LENGTH)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, ITERATIONS, dklen=KEY_LENGTH)
    return salt + key

def verify_password(stored_password, provided_password):
    salt = stored_password[:SALT_LENGTH]
    stored_key = stored_password[SALT_LENGTH:]
    provided_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, ITERATIONS, dklen=KEY_LENGTH)
    return stored_key == provided_key

def check_password():
    def password_entered():
        stored_password = base64.b64decode(PASSWORD)
        if verify_password(stored_password, st.session_state["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        password_placeholder = st.empty()
        password_placeholder.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    
    elif not st.session_state["password_correct"]:
        password_placeholder = st.empty()
        password_placeholder.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    
    # Password correct.
    else:
        return True

def clear_session_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("Session state cleared!")

def logout_button():
    if st.sidebar.button("Logout"):
        clear_session_state()
        st.switch_page('pages/1_requirements.py')