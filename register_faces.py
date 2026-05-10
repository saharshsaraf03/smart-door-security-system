import cv2
import os
from aws_helper import register_known_face, create_rekognition_collection

def capture_face(name):
    print(f"\nCapturing face for: {name}")
    print("Look at the camera. Press SPACEBAR to capture. Press Q to skip.")
    
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.putText(frame, f"Registering: {name} | SPACE to capture | Q to skip",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.imshow('Face Registration', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):
            image_path = f"known_faces/{name}.jpg"
            cv2.imwrite(image_path, frame)
            print(f"Face captured and saved: {image_path}")
            cap.release()
            cv2.destroyAllWindows()
            return image_path
            
        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return None

def main():
    print("=" * 50)
    print("Face Registration System")
    print("=" * 50)
    
    # Create Rekognition collection first
    create_rekognition_collection()
    
    # Ask how many people to register
    n = int(input("\nHow many people do you want to register? "))
    
    for i in range(n):
        name = input(f"\nEnter name for person {i+1} (no spaces, e.g. Saharsh): ").strip()
        
        image_path = capture_face(name)
        
        if image_path:
            print(f"Uploading {name} to AWS Rekognition...")
            register_known_face(image_path, name)
            print(f"✅ {name} registered successfully!")
        else:
            print(f"Skipped {name}")
    
    print("\n" + "=" * 50)
    print("Registration complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()