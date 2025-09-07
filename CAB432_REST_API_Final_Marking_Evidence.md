# Assignment 1 - REST API Project - Response to Criteria

## Overview

- **Name:** Srimanjary Paul  
- **Student number:** n10886524
- **Application name:** Video Transcoder API  
- **Two line description:** This app allows users to upload video files and trigger transcoding into H.264 (720p).  
  It implements JWT authentication with admin/user roles, versioned REST endpoints, and a simple web client at `/ui`.

---

## Core criteria

### Containerise the app

- **ECR Repository name:** srimanjary/cab432  
- **Video timestamp:** *see build log screenshot*  
- **Relevant files:**  
  - /Dockerfile  

### Deploy the container

- **EC2 instance ID:** *see EC2 screenshot*  
- **Video timestamp:** *see deployment screenshot*  
- **Relevant files:**  
  - Deployment logs (docker run, docker pull)  

### User login

- **One line description:** JWT login with roles (admin/user); admin-only metrics endpoint protected by role guard.  
- **Video timestamp:** *see curl proof screenshot*  
- **Relevant files:**  
  - /auth.py  

### REST API

- **One line description:** Versioned API under `/api/v1/*`, with correct methods, OpenAPI docs at `/docs`.  
- **Video timestamp:** *see swagger UI screenshot*  
- **Relevant files:**  
  - /main.py  
  - /routers/*  

### Data types

- **One line description:** Two data types: Media (video uploads) and Jobs (transcode tasks).  
- **Video timestamp:** *see UI video list screenshot*  
- **Relevant files:**  
  - /models.py  

#### First kind

- **One line description:** Media records for uploaded videos.  
- **Type:** Structured metadata + file storage  
- **Rationale:** Supports listing, ownership, and initiating transcodes.  
- **Video timestamp:** *see upload screenshot*  
- **Relevant files:**  
  - /models.py  

#### Second kind

- **One line description:** Job records for transcoding tasks.  
- **Type:** Structured (status, output, ffmpeg summary)  
- **Rationale:** Required for managing CPU-heavy transcodes asynchronously.  
- **Video timestamp:** *see transcode screenshot*  
- **Relevant files:**  
  - /models.py  
  - /transcode.py  

### CPU intensive task

- **One line description:** ffmpeg transcoding (H.264, 720p).  
- **Video timestamp:** *see ffmpeg job screenshot*  
- **Relevant files:**  
  - /transcode.py  

### CPU load testing

- **One line description:** Multiple transcodes push CPU usage >80% (observed 100%).  
- **Video timestamp:** *see Docker engine CPU screenshot*  
- **Relevant files:**  
  - /load_test.sh  

---

## Additional criteria

### Extensive REST API features

- **One line description:** Versioned API endpoints; pagination and sorting in list APIs.  
- **Video timestamp:** *see OpenAPI screenshot*  
- **Relevant files:**  
  - /routers/videos.py  

### External API(s)

- **One line description:** Integrated Data API to fetch related video titles and thumbnails alongside uploaded media.  
- **Video timestamp:** *see external API call screenshot*  
- **Relevant files:**  
  - /routers/external.py  
  - /schemas.py  

### Additional kinds of data

- **One line description:** Stores three data types — Media records, Job records, and External video metadata (title, thumbnail).  
- **Video timestamp:** *see video list with thumbnails screenshot*  
- **Relevant files:**  
  - /models.py  
  - /routers/videos.py  

### Custom processing

- **One line description:** Custom thumbnail extractor generates still-frame previews from uploaded videos during transcoding.  
- **Video timestamp:** *see transcoding with thumbnail screenshot*  
- **Relevant files:**  
  - /transcode.py  
  - /static/thumbnails/  

### Infrastructure as code

- **One line description:** Deployment automated with Docker Compose to provision API container and volume mounts in one command.  
- **Video timestamp:** *see docker-compose up screenshot*  
- **Relevant files:**  
  - /docker-compose.yml  

### Web client

- **One line description:** Web UI supports login, upload, listing, and transcode.  
- **Video timestamp:** *see UI screenshot*  
- **Relevant files:**  
  - /frontend/index.html  
  - /frontend/app.js  

### Upon request

- **One line description:** Not attempted  
- **Video timestamp:** —  
- **Relevant files:** —  

---

