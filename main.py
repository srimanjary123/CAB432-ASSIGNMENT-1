import os, shutil, uuid, datetime as dt
from pathlib import Path
from typing import List
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, desc
from models import init_db, SessionLocal, Video, Job
from auth import verify_login, create_token, require_auth, require_admin
from schemas import LoginReq, LoginResp, UploadResp, JobReq, JobResp, VideoOut
from ffmpeg_utils import ensure_dirs, transcode

APP_NAME = "Video Transcoder API"
app = FastAPI(title=APP_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

ensure_dirs()
init_db()

app.mount("/ui", StaticFiles(directory="static", html=True), name="ui")

@app.get("/health")
def health():
    return {"ok": True, "time": dt.datetime.utcnow().isoformat()}

@app.post("/api/v1/auth/login", response_model=LoginResp)
def login(body: LoginReq):
    user = verify_login(body.username, body.password)
    token = create_token(user["username"], user["role"])
    return {"access_token": token, "username": user["username"], "role": user["role"]}

@app.post("/api/v1/media/upload", response_model=UploadResp)
def upload(file: UploadFile = File(...), user=Depends(require_auth)):
    uploads = Path("/data/uploads")
    vid_id = str(uuid.uuid4())
    safe_name = f"{vid_id}_{file.filename}"
    dest = uploads / safe_name
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    size = dest.stat().st_size

    db = SessionLocal()
    try:
        v = Video(id=vid_id, owner=user["username"], filename=file.filename,
                  stored_path=str(dest), size_bytes=size)
        db.add(v); db.commit()
        return {"video_id": vid_id}
    finally:
        db.close()

@app.get("/api/v1/media", response_model=List[VideoOut])
def list_media(
    owner: str | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    sort: str = Query("created_at_desc"),
    user=Depends(require_auth),
):
    db = SessionLocal()
    try:
        q = select(Video)
        if owner: q = q.where(Video.owner == owner)
        if sort == "created_at_desc": q = q.order_by(desc(Video.created_at))
        offs = (page-1)*per_page
        rows = db.execute(q.offset(offs).limit(per_page)).scalars().all()
        return [VideoOut(id=r.id, owner=r.owner, filename=r.filename, size_bytes=r.size_bytes) for r in rows]
    finally:
        db.close()

@app.post("/api/v1/transcode", response_model=JobResp)
def start_transcode(body: JobReq, user=Depends(require_auth)):
    db = SessionLocal()
    try:
        v = db.get(Video, body.video_id)
        if not v:
            raise HTTPException(404, "Video not found")

        # copy fields BEFORE closing the session
        video_id = v.id
        input_path = v.stored_path
        input_name_stem = Path(v.filename).stem

        outdir = os.path.join("/data/outputs", video_id, dt.datetime.utcnow().strftime("%Y%m%d%H%M%S"))
        job = Job(video_id=video_id, owner=user["username"], status="running", output_dir=outdir)
        db.add(job); db.commit(); db.refresh(job)
        job_id = job.id
    finally:
        db.close()

    # CPU-intensive work
    try:
        log = transcode(input_path, outdir, input_name_stem)
        status, detail = "completed", log
    except Exception as e:
        status, detail = "failed", str(e)

    db = SessionLocal()
    try:
        j = db.get(Job, job_id)
        j.status = status
        j.detail = detail[-4000:]
        j.finished_at = dt.datetime.utcnow()
        db.commit()
        return {"id": j.id, "status": j.status, "detail": j.detail}
    finally:
        db.close()

@app.get("/api/v1/jobs/{job_id}", response_model=JobResp)
def get_job(job_id: str, user=Depends(require_auth)):
    db = SessionLocal()
    try:
        j = db.get(Job, job_id)
        if not j: raise HTTPException(404, "Job not found")
        return {"id": j.id, "status": j.status, "detail": j.detail}
    finally:
        db.close()

