import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import time

# --- Setup ---
# Generate and store a persistent Fernet key
if 'fernet_key' not in st.session_state:
    st.session_state.fernet_key = Fernet.generate_key()
cipher = Fernet(st.session_state.fernet_key)

# Initialize session state
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'login_time' not in st.session_state:
    st.session_state.login_time = None

MASTER_PASSWORD = "admin123"  # In production, use proper authentication
MAX_ATTEMPTS = 3

# --- Functions ---
def hash_passkey(passkey):
    """Hashes the passkey using SHA256 with salt"""
    salt = "secure_salt_value"
    return hashlib.sha256((passkey + salt).encode()).hexdigest()

def encrypt_data(text):
    """Encrypts the data using Fernet cipher"""
    try:
        encrypted_bytes = cipher.encrypt(text.encode())
        return encrypted_bytes.decode('latin-1')
    except Exception as e:
        st.error(f"Encryption error: {e}")
        return None

def decrypt_data(encrypted_text):
    """Decrypts the data"""
    try:
        encrypted_bytes = encrypted_text.encode('latin-1')
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        return decrypted_bytes.decode()
    except Exception as e:
        st.error(f"Decryption error: {e}")
        return None

# --- UI Components ---
def show_login_success():
    """Shows login success animation"""
    success_placeholder = st.empty()
    with success_placeholder:
        st.success("✅ Login successful!")
        st.balloons()
        time.sleep(1.5)
    success_placeholder.empty()

def login_page():
    """Enhanced login page with better UI"""
    st.subheader("🔑 Login Required")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3064/3064155.png", width=100)
    
    with col2:
        st.markdown("""
        <style>
            .login-box {
                padding: 20px;
                border-radius: 10px;
                background-color: #f0f2f6;
            }
        </style>
        <div class="login-box">
            <h3>Please authenticate to continue</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        login_pass = st.text_input("Master Password:", type="password", help="Enter the master password to unlock the system")
        login_button = st.form_submit_button("Unlock System")
        
        if login_button:
            if login_pass == MASTER_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.failed_attempts = 0
                st.session_state.login_time = time.time()
                show_login_success()
                st.rerun()
            else:
                st.error("❌ Incorrect password! Please try again")
                st.session_state.failed_attempts += 1

# --- Main UI ---
st.set_page_config(page_title="Secure Data System", page_icon="🔒", layout="centered")

# Custom CSS for better styling
st.markdown("""
<style>
    .stTextInput input, .stTextArea textarea {
        border-radius: 8px !important;
    }
    .stButton button {
        border-radius: 8px !important;
        background-color: #4CAF50 !important;
        color: white !important;
    }
    .stAlert {
        border-radius: 10px !important;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔒 Secure Data Encryption System")

# Sidebar Navigation with icons
menu_options = {
    "Home": "🏠",
    "Store Data": "📂", 
    "Retrieve Data": "🔍",
    "Login": "🔑"
}

with st.sidebar:
    st.header("Navigation")
    choice = st.radio("", list(menu_options.keys()), 
               format_func=lambda x: f"{menu_options[x]} {x}",
               label_visibility="collapsed")
    
    if st.session_state.logged_in and st.session_state.login_time:
        st.markdown(f"🕒 Session active for {int(time.time() - st.session_state.login_time)} seconds")

# Home Page
if choice == "Home":
    st.subheader("🏠 Welcome!")
    st.write("""
    Use this app to securely store and retrieve sensitive data using military-grade encryption.
    
    **Features:**
    - 🔐 AES-256 encryption
    - 🔑 Passkey protection
    - 🛡️ Brute-force protection
    """)
    
    if st.checkbox("Show system status"):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Stored Items", len(st.session_state.stored_data))
        with col2:
            st.metric("Failed Attempts", st.session_state.failed_attempts)

# Store Data
elif choice == "Store Data":
    st.subheader("📂 Store New Data")
    
    with st.form("store_form"):
        unique_id = st.text_input("Unique ID*", help="A unique identifier for your data")
        user_data = st.text_area("Data to Encrypt*", height=150)
        passkey = st.text_input("Passkey*", type="password", help="Create a strong passkey you'll remember")
        
        if st.form_submit_button("🔒 Encrypt & Save"):
            if not all([user_data, passkey, unique_id]):
                st.error("Please fill all required fields (*)")
            elif unique_id in st.session_state.stored_data:
                st.error("This ID already exists! Please choose another.")
            else:
                encrypted_text = encrypt_data(user_data)
                if encrypted_text:
                    st.session_state.stored_data[unique_id] = {
                        "encrypted_text": encrypted_text,
                        "hashed_passkey": hash_passkey(passkey)
                    }
                    st.success("Data encrypted and stored securely!")
                    with st.expander("View encrypted data"):
                        st.code(encrypted_text)

# Retrieve Data
elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    
    # Check if user is locked out
    if st.session_state.failed_attempts >= MAX_ATTEMPTS and not st.session_state.logged_in:
        st.warning("🔒 Too many failed attempts. Please login to continue.")
        st.session_state.choice = "Login"
        st.rerun()
    
    with st.form("retrieve_form"):
        unique_id = st.text_input("Unique ID*")
        passkey = st.text_input("Passkey*", type="password")
        
        if st.form_submit_button("🔓 Decrypt"):
            if not all([unique_id, passkey]):
                st.error("Please fill all required fields (*)")
            elif unique_id not in st.session_state.stored_data:
                st.warning("No data found with this ID")
            else:
                data = st.session_state.stored_data[unique_id]
                if hash_passkey(passkey) == data["hashed_passkey"]:
                    decrypted_text = decrypt_data(data["encrypted_text"])
                    if decrypted_text is not None:
                        st.success("✅ Decryption successful!")
                        st.text_area("Decrypted Data", value=decrypted_text, height=200)
                        st.session_state.failed_attempts = 0
                    else:
                        st.error("Technical error during decryption")
                else:
                    st.session_state.failed_attempts += 1
                    remaining = MAX_ATTEMPTS - st.session_state.failed_attempts
                    st.error(f"❌ Wrong passkey! {remaining} attempts remaining")
                    if st.session_state.failed_attempts >= MAX_ATTEMPTS:
                        st.warning("🔒 Account locked due to too many failed attempts.")
                        st.session_state.logged_in = False
                        time.sleep(1)
                        st.rerun()

# Login Page
elif choice == "Login":
    login_page()

# Footer
st.markdown("---")
st.markdown("""
<style>
.footer {
    font-size: 0.8rem;
    color: #6c757d;
    text-align: center;
}
</style>
<div class="footer">
    Secure Data Encryption System • Project by Muhammad Hamza
</div>
""", unsafe_allow_html=True)