import hashlib

string = "rrw9xc"
hashed = hashlib.sha256(bytes(string, 'utf-8')).hexdigest()
print(hashed)