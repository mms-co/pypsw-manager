# Py-Psw Manager
A lightweight, secure desktop built with Python and an HTML/CSS/JavaScript frontend, powered by `pywebview`. Passwords are encrypted using AES-128 and stored in the home directory. 

---
## Security Architecture
- **Master Password**: First prompted at the top of the application, this is processed in-memory and **never** stored in-disk.
- **Master Key**: Derived by first hashing the master password, then encoding the hash in base 64.
- **Encryption**: Involves taking the password and encrypting it using Fernet (AES-128, CBC mode, PCKCS7 padding, SHA-256 hashed signing) via the master key, the ciphertext is then encoded in base 64 for storage.
- **Storage**: Data is safely written in a structure JSON vault located in a folder inside the user's directory, passwords have an associated entry identifier decided by the user.

## Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

## Installation
```bash
git clone https://github.com/mms-co/pypsw-manager
cd pypsw-manager
pip install -r requirements.txt
```

## Usage
```bash
cd src/backend
python app.py
```

## License
Distributed under the MIT License. See `LICENSE` for more information.