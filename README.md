# Smart Door Security System with Face Recognition

> An IoT-based smart security system using Raspberry Pi 5, AWS Cloud AI, OpenCV, and real-time alerts.

**Authors:** Saharsh Saraf & Sahil Lahane | **Mentor:** Dr. Pooja Gundewar | MIT World Peace University, Pune

---

## Overview

A fully functional hybrid edge-cloud IoT security system that:
- Detects motion automatically using OpenCV background subtraction
- Captures visitor images using Raspberry Pi Camera Module
- Identifies known vs unknown faces using AWS Rekognition (deep learning)
- Sends real-time Telegram alerts with photo to owner's phone
- Logs every event to AWS DynamoDB
- Displays live visitor analytics on a Flask web dashboard

---

## Project Photos

### Hardware Setup
![Hardware Setup](images/hardware.jpg)

### System Running
![Terminal Output](images/terminal.jpg)

### Live Dashboard
![Dashboard](images/dashboard.jpg)

### AWS S3 Cloud Storage
![AWS S3](images/s3.png)

---

## System Architecture
Motion Detected (OpenCV)
↓
Raspberry Pi 5 — Image Capture (Pi Camera)
↓
OpenCV — Face Detection (Edge)
↓
AWS S3 — Image Upload (Cloud)
↓
AWS Rekognition — Face Recognition (Cloud AI)
↓
Known Face → Telegram Alert + Email + DynamoDB Log
Unknown Face → Photo Alert + Email + DynamoDB Log
↓
Flask Dashboard — Live Visitor Analytics

---

## Features

- Software-based motion detection — no PIR sensor needed
- Two-stage AI pipeline — edge detection + cloud recognition
- 100% face recognition accuracy using AWS Rekognition
- Real-time Telegram push notification with visitor photo
- Gmail backup email alert with image attachment
- AWS DynamoDB logging of every visitor event
- Live Flask dashboard accessible across the network
- Production-grade security — credentials in .env, IAM least privilege

---

## Hardware Requirements

| Component | Details |
|---|---|
| Raspberry Pi 5 | Main IoT edge processor |
| Raspberry Pi Camera Module | OV5647, 5MP, CSI interface |
| MicroSD Card | 16GB+ with Raspberry Pi OS |
| Internet Connection | WiFi or Ethernet |

---

## AWS Services Used

| Service | Purpose |
|---|---|
| AWS Rekognition | Deep learning face recognition |
| AWS S3 | Secure image storage |
| AWS DynamoDB | Visitor event logging |
| AWS IAM | Secure credential management |

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Primary language |
| OpenCV 4.10 | Motion detection + face detection |
| boto3 | AWS SDK |
| python-telegram-bot | Telegram alerts |
| Flask | Web dashboard |
| rpicam-apps | Pi Camera capture |

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/saharshsaraf03/smart-door-security-system.git
cd smart-door-security-system
```

### 2. Install dependencies
```bash
pip3 install -r requirements.txt
sudo apt install -y rpicam-apps python3-opencv
```

### 3. Configure credentials
```bash
cp .env.example .env
nano .env
```

### 4. Register known faces
```bash
python3 register_faces.py
```

### 5. Run the system
```bash
python3 main.py 2>&1
python3 dashboard/app.py
```

---

## Project Structure
smart-door/
├── main.py                 — Core pipeline
├── aws_helper.py           — AWS functions
├── telegram_helper.py      — Telegram alerts
├── email_helper.py         — Gmail alerts
├── register_faces.py       — Face registration
├── dashboard/
│   ├── app.py              — Flask server
│   └── templates/
│       └── index.html      — Dashboard UI
├── requirements.txt
├── .env.example
└── .gitignore

---

## Test Results

| Test Case | Result |
|---|---|
| Registered face recognition | PASS — 100% confidence |
| Unknown face detection | PASS — Photo alert fired |
| Telegram alert delivery | PASS — Under 6 seconds |
| Dashboard network access | PASS — Opened on laptop |
| DynamoDB logging | PASS — All events stored |

---

## Future Extensions

- Smart lock integration via GPIO relay
- Multi-door support with centralized dashboard
- Native mobile application
- Live video streaming
- Visitor analytics with graphs

---

## Authors

**Saharsh Saraf** — [GitHub](https://github.com/saharshsaraf03)

**Sahil Lahane**

**Mentor:** Dr. Pooja Gundewar

**Institution:** MIT World Peace University, Pune | ECE Department | 2026