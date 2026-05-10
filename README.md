\# 🔐 Cloud-Integrated Smart Door Security System with Face Recognition



!\[Python](https://img.shields.io/badge/Python-3.10-blue)

!\[AWS](https://img.shields.io/badge/AWS-Rekognition%20%7C%20S3%20%7C%20DynamoDB-orange)

!\[Raspberry Pi](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205-red)

!\[OpenCV](https://img.shields.io/badge/OpenCV-4.10-green)

!\[Flask](https://img.shields.io/badge/Flask-3.1-lightgrey)



An IoT-based smart door security system that uses \*\*edge computing\*\* on Raspberry Pi 5 and \*\*AWS cloud AI\*\* to automatically detect visitors, recognize faces, send real-time alerts, and log all activity to a live web dashboard.



\---



\## 🎯 Features



\- \*\*Software-based motion detection\*\* using OpenCV background subtraction (no PIR sensor needed)

\- \*\*Two-stage AI pipeline\*\* — edge face detection + cloud face recognition

\- \*\*AWS Rekognition\*\* deep learning face identification (100% accuracy on registered faces)

\- \*\*Real-time Telegram alerts\*\* with visitor photo sent to owner's phone within seconds

\- \*\*Gmail backup alerts\*\* with captured image attachment

\- \*\*AWS DynamoDB\*\* logging of every visitor event with timestamp

\- \*\*Live Flask dashboard\*\* accessible across the network showing visitor analytics

\- \*\*AWS S3\*\* secure cloud storage for all visitor images

\- \*\*Production-grade security\*\* — credentials in .env, IAM least privilege, HTTPS/TLS



\---



\## 🏗 System Architecture

PIR Sensor / OpenCV Motion Detection

↓

Raspberry Pi 5 (Edge)

↓

Pi Camera Module (Capture)

↓

OpenCV — Face Detection (Edge AI)

↓

AWS S3 — Image Upload

↓

AWS Rekognition — Face Recognition

↓

┌─────────────────────┐

│    KNOWN FACE       │    UNKNOWN FACE

│  ✅ Authorized      │  🚨 Unauthorized

│  Telegram + Email   │  Photo Alert + Email

└─────────────────────┘

↓

AWS DynamoDB — Event Log

↓

Flask Dashboard — Analytics



\---



\## 🛠 Hardware Requirements



| Component | Details |

|---|---|

| Raspberry Pi 5 | Main IoT edge processor |

| Raspberry Pi Camera Module | OV5647, 5MP, CSI interface |

| MicroSD Card | 16GB+ with Raspberry Pi OS |

| Internet Connection | WiFi or Ethernet |



\---



\## ☁️ AWS Services Used



| Service | Purpose | Free Tier |

|---|---|---|

| AWS Rekognition | Deep learning face recognition | 5,000 images/month |

| AWS S3 | Secure image storage | 5GB storage |

| AWS DynamoDB | Visitor event logging | 25GB storage |



\---



\## 🚀 Installation \& Setup



\### 1. Clone the Repository

```bash

git clone https://github.com/yourusername/smart-door-security-system.git

cd smart-door-security-system

```



\### 2. Install Dependencies

```bash

pip3 install -r requirements.txt

```



\### 3. Install Raspberry Pi Camera Tools

```bash

sudo apt install -y rpicam-apps python3-opencv

```



\### 4. Configure AWS

\- Create an AWS IAM user with S3, Rekognition, and DynamoDB permissions

\- Create an S3 bucket with `/known-faces/` and `/visitors/` folders

\- Create a DynamoDB table named `DoorVisitorLog` with partition key `timestamp`



\### 5. Set Up Credentials

```bash

cp .env.example .env

nano .env

```

Fill in all your credentials in the `.env` file.



\### 6. Set Up Telegram Bot

\- Message @BotFather on Telegram

\- Create a new bot and get your Bot Token

\- Message @userinfobot to get your Chat ID



\### 7. Register Known Faces

```bash

python3 register\_faces.py

```

Follow the prompts to register authorized persons.



\---



\## ▶️ Running the System



\*\*Start the main security system:\*\*

```bash

python3 main.py 2>\&1

```



\*\*Start the dashboard (in a new terminal):\*\*

```bash

python3 dashboard/app.py

```



\*\*Access the dashboard:\*\*

http://\[Raspberry-Pi-IP]:5000



\*\*Run both permanently in background:\*\*

```bash

screen -S dashboard -dm python3 dashboard/app.py

screen -S mainsystem -dm python3 main.py 2>\&1

```



\---



\## 📁 Project Structure

smart-door/

├── main.py                  # Core pipeline — motion → capture → recognize → alert

├── aws\_helper.py            # AWS S3, Rekognition, DynamoDB functions

├── telegram\_helper.py       # Telegram Bot alert functions

├── email\_helper.py          # Gmail SMTP alert functions

├── register\_faces.py        # One-time face registration script

├── haarcascade\_frontalface\_default.xml  # OpenCV face detection model

├── dashboard/

│   ├── app.py               # Flask dashboard server

│   └── templates/

│       └── index.html       # Dashboard UI

├── requirements.txt         # Python dependencies

├── .env.example             # Credentials template

└── .gitignore               # Git ignore rules



\---



\## 🔐 Security



\- All credentials stored in `.env` file — never committed to GitHub

\- AWS IAM user with minimum required permissions only

\- Private S3 bucket — images not publicly accessible by default

\- HTTPS/TLS encryption on all AWS API calls

\- Gmail App Password used — real password never in code



\---



\## 📊 Demo Results



| Test Case | Result | Confidence |

|---|---|---|

| Registered face recognition | ✅ PASS | 100% |

| Unknown face detection | ✅ PASS | N/A |

| Telegram alert delivery | ✅ PASS | < 6 seconds |

| Dashboard visibility | ✅ PASS | Network-wide |

| DynamoDB logging | ✅ PASS | All events |



\---



\## 🔮 Future Extensions



\- Smart lock integration via GPIO relay

\- Multi-door support with centralized dashboard

\- Native mobile application

\- Live video streaming (RTSP)

\- Visitor analytics with graphs and heatmaps

\- Mask detection AI layer



\---



\## 👨‍💻 Authors



\- \*\*Saharsh Saraf\*\* — \[GitHub](https://github.com/saharshsaraf)

\- \*\*Sahil Laganea\*\*



\*\*Mentor:\*\* Dr. Pooja Gundewar



\*\*Institution:\*\* MIT World Peace University, Pune | Department of ECE | 2026



\---



\## 📄 License



This project is for educational purposes as part of an IoT course project at MIT World Peace University, Pune.

