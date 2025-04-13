🔒 Project Overview
A secure web application built with Streamlit that allows users to:

Encrypt sensitive data with a passkey

Store encrypted data in memory

Retrieve data only with the correct passkey

Features brute-force protection with login after 3 failed attempts

🚀 Features
Military-Grade Encryption: Uses Fernet (AES-128) encryption

Passkey Protection: Data can only be decrypted with the original passkey

Session Management: Tracks active sessions and failed attempts

Clean UI: User-friendly interface with visual feedback

No Database Needed: Stores everything in memory (session)

🛠️ Installation
Clone the repository:

bash
Copy
git clone https://github.com/muhammadHamzaIsmaeel/Secure-Data-Encryption-System.git
cd secure-data-encryption
Install requirements:

bash
Copy
pip install -r requirements.txt
Run the app:

bash
Copy
streamlit run app.py
📖 How It Works
Storing Data
Go to "Store Data" page

Enter:

A unique ID for your data

The sensitive data you want to encrypt

A strong passkey (remember this!)

Click "Encrypt & Save"

Your data is now securely encrypted and stored

Retrieving Data
Go to "Retrieve Data" page

Enter:

The exact same unique ID

The exact same passkey

Click "Decrypt"

If correct, your original data will appear

Security Features
After 3 wrong passkey attempts, the system locks

You'll need to login with the master password to continue

All passkeys are hashed before storage

🔐 Default Credentials
Master Password: admin123 (Change this in production!)

📝 Code Structure
Copy
app.py                # Main application file
requirements.txt      # Python dependencies
README.md            # This documentation
💡 Why This Project?
Learn about real-world encryption implementation

Understand session-based security

See how to build secure web apps with Python

Great template for building your own secure apps

🚨 Important Notes
This is for educational purposes only - Not for production use without modifications

Data is stored in memory - Will be lost when the app restarts

Change the master password before using for anything serious

👨‍💻 Author
Muhammad Hamza
GitHub Profile

📜 License
MIT License - Feel free to use and modify