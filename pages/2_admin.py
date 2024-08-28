import streamlit as st
import hashlib
import os
import base64

# Constants for PBKDF2
SALT_LENGTH = 32
ITERATIONS = 100000
KEY_LENGTH = 32

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
        stored_password = base64.b64decode(st.secrets["hashed_password"])
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

def main():

    if check_password():
        logout_button()
        
        # Your main app goes here
        st.title("Admin Area")

        tab1, tab2, tab3 = st.tabs(['Upload New Version', 'Compare Versions', 'Configure Version'])

        with tab1:
            st.subheader("Upload New Version")

        with tab2:
            st.subheader("Compare Versions")

        with tab3:
            st.subheader("Configure Version")

    else:
        with st.container():  
            st.warning("Please enter the password to access the app.")
            st.markdown("""
                        DEMO PURPOSE ONLY - NOT FOR PRODUCTION USE

To enter the admin area, use the password: "Password123!"

WARNING: This is a demonstration password. In a real application, never reveal 
passwords. For actual deployment:
1. Use a strong, unique password
2. Implement two-factor authentication (2FA)
3. Store passwords securely (hashed and salted)
4. Regularly update and rotate passwords

Remember: Security is crucial. This demo setup is not suitable for any real-world application.
                        """)

if __name__ == "__main__":
    main()