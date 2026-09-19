import os
from cryptography.fernet import Fernet
import json
import hashlib
import base64


STORAGE = "encrypted_vault.enc"
FOLDER = "/py-password-gen/"
HOME = os.path.expanduser("~")

class APIBridge:
	def __init__(self):
		# Set main path
		self.path = HOME + FOLDER
	def save(self, master_key, entry, password):
		check_files()
		ENC_FILE = self.path + STORAGE
		code = {"success": False, "rewrite": False}
		# Set up AES encryption with hashed master password
		key = process_key(master_key.encode("utf-8"))
		f = Fernet(key)
		enc = f.encrypt(password.encode("utf-8"))
		# Get all passwords
		content = {}
		with open(ENC_FILE, "r") as file:
			content = json.loads(file.read())
			file.close()
		if entry in content.keys():
			code["rewrite"] = True
		# Insert/replace the encrypted and encoded password
		content[entry] = base64.b64encode(enc).decode("utf-8")
		# Write back to file
		with open(ENC_FILE, "w") as file:
			file.write(json.dumps(content))
			file.close()
		code["success"] = True
		return code
	def get(self, master_key, entry):
		check_files()
		ENC_FILE = self.path + STORAGE
		code = {"success": False, "value": ""}
		# Set up AES encryption with hashed master password
		key = process_key(master_key.encode("utf-8"))
		f = Fernet(key)
		# Get all passwords
		enc_vault = {}
		with open(ENC_FILE, "r") as file:
			enc_vault = json.loads(file.read())
			file.close()
		# Make sure the entry exists
		if entry not in enc_vault.keys():
			return code
		# Decode and decrypt the respective password
		enc = base64.b64decode(enc_vault[entry].encode("utf-8"))
		raw = f.decrypt(enc)
		code["value"] = raw.decode("utf-8")
		code["success"] = True
		return code

# Hash and encode the key
def process_key(master_key):
	key_hash = hashlib.sha256(master_key).digest()
	key = base64.b64encode(key_hash)
	return key

# Make sure the file exists, it must have a JSON component inside
def check_files():
	# 1. Check if dedicated folder exists
	folder = FOLDER[1:-1]
	if folder not in os.listdir(path=HOME):
		# Make the folder if it doesn't exist
		os.mkdir(HOME + FOLDER[:-1])
	path = HOME + FOLDER[:-1]
	# 2. Check if file exists
	if STORAGE not in os.listdir(path=path):
		# Make the file if it doesn't exist 
		with open(HOME + FOLDER + STORAGE, "w") as file:
			file.write("{}")
			file.close()
	else:
		# 3. Check if the file format follows JSON
		content = ''
		with open(HOME + FOLDER + STORAGE, "r") as file:
			content = file.read()
			file.close()
		try:
			json.loads(content)
		except json.decoder.JSONDecodeError:
			raise LookupError("Storage file is in an incorrect format")
		finally:
			# Overwrite if the file isn't in JSON
			with open(HOME + FOLDER + STORAGE, "w") as file:
				file.write("{}")
				file.close()
