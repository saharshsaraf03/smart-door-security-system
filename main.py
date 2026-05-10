import cv2
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from aws_helper import upload_to_s3, recognize_face, log_to_dynamodb
from telegram_helper import send_telegram_message, send_telegram_photo
from email_helper import send_email_alert

load_dotenv()

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def capture_and_process():
    print("\n🚨 Motion detected! Capturing image...")

    cap = cv2.VideoCapture(0)
    time.sleep(1)  # Let camera warm up

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Failed to capture image")
        return

    # Save captured image temporarily
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_path = f"temp/visitor_{timestamp}.jpg"
    cv2.imwrite(temp_path, frame)
    print(f"Image captured: {temp_path}")

    # Detect face
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        print("No face detected — discarding image")
        os.remove(temp_path)
        return

    print(f"Face detected! Proceeding to cloud...")

    # Upload to S3
    s3_key = f"visitors/visitor_{timestamp}.jpg"
    image_url = upload_to_s3(temp_path, s3_key)
    print(f"Uploaded to S3: {image_url}")

    # Recognize face
    status, name, confidence = recognize_face(temp_path)

    if status == 'known':
        print(f"✅ Known person: {name} ({confidence:.1f}% confidence)")

        log_to_dynamodb(timestamp, name, image_url, 'Authorized')

        send_telegram_message(
            f"✅ <b>Authorized Entry</b>\n"
            f"👤 Identity: <b>{name}</b>\n"
            f"🕐 Time: {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n"
            f"📊 Confidence: {confidence:.1f}%"
        )

        send_email_alert(
            subject=f"✅ Authorized Entry — {name}",
            body=f"Authorized person detected.\n\nIdentity: {name}\nTime: {datetime.now().strftime('%d %b %Y, %I:%M %p')}\nConfidence: {confidence:.1f}%",
            image_path=temp_path
        )

    else:
        print("🚨 Unknown person detected!")

        log_to_dynamodb(timestamp, 'Unknown', image_url, 'Unauthorized')

        send_telegram_photo(
            image_path=temp_path,
            caption=f"🚨 <b>UNKNOWN PERSON DETECTED</b>\n"
                   f"🕐 Time: {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n"
                   f"⚠️ Status: Unauthorized"
        )

        send_email_alert(
            subject="🚨 Unknown Person Detected!",
            body=f"WARNING: Unknown person detected at the door.\n\nTime: {datetime.now().strftime('%d %b %Y, %I:%M %p')}\nStatus: Unauthorized",
            image_path=temp_path
        )

    # Clean up
    os.remove(temp_path)
    print("Done. Watching for next motion...\n")

def main():
    print("=" * 50)
    print("Smart Door Security System Started")
    print("Watching for motion automatically...")
    print("Press Q to quit")
    print("=" * 50)

    from aws_helper import create_rekognition_collection
    create_rekognition_collection()

    cap = cv2.VideoCapture(0)

    # Read first frame as background
    ret, background = cap.read()
    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    background = cv2.GaussianBlur(background, (21, 21), 0)

    # Cooldown so it doesn't trigger repeatedly
    last_trigger_time = 0
    cooldown_seconds = 10

    print("\nSystem is live. Watching for movement...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Compare current frame to background
        delta = cv2.absdiff(background, gray)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(thresh.copy(),
                                        cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) > 5000:
                motion_detected = True
                break

        current_time = time.time()

        if motion_detected and (current_time - last_trigger_time > cooldown_seconds):
            last_trigger_time = current_time
            cap.release()
            cv2.destroyAllWindows()
            capture_and_process()
            # Restart camera and reset background
            cap = cv2.VideoCapture(0)
            ret, background = cap.read()
            background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
            background = cv2.GaussianBlur(background, (21, 21), 0)
        else:
            # Show live feed with status
            status_text = "MOTION DETECTED!" if motion_detected else "Watching..."
            color = (0, 0, 255) if motion_detected else (0, 255, 0)
            cv2.putText(frame, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(frame, "Press Q to quit", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.imshow('Smart Door Security System', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("System shut down.")

if __name__ == "__main__":
    main()