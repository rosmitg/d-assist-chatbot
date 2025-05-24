# auth.py

def check_credentials(username, password):
    if username == "admin" and password == "admin":
        return "admin"
    elif username == "staff" and password == "staff":
        return "staff"
    return None
