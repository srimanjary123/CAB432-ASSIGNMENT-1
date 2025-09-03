from pydantic import BaseModel
from typing import Optional, List

class LoginReq(BaseModel):
    username: str
    password: str

class LoginResp(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: str

class UploadResp(BaseModel):
    video_id: str

class JobReq(BaseModel):
    video_id: str

class JobResp(BaseModel):
    id: str
    status: str
    detail: str

class VideoOut(BaseModel):
    id: str
    owner: str
    filename: str
    size_bytes: int

