import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode(), hashed_password)
