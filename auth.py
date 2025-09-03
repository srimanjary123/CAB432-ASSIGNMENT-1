import os, time, jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALG = "HS256"

# username -> {password, role}
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "srimanjary":  {"password": "srimanjary123",  "role": "user"},
}

security = HTTPBearer()

def create_token(username: str, role: str):
    now = int(time.time())
    payload = {"sub": username, "role": role, "iat": now, "exp": now + 3600}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def require_auth(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        return {"username": payload["sub"], "role": payload["role"]}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def require_admin(user = Depends(require_auth)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    return user

def verify_login(username: str, password: str):
    u = USERS.get(username)
    if not u or u["password"] != password:
        raise HTTPException(status_code=401, detail="Bad credentials")
    return {"username": username, "role": u["role"]}

