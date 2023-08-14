import cv2
import time
import smtplib
import imghdr
from email.message import EmailMessage

# Sender and Receiver Email Addresses
sender_email = "harishcooper379@gmail.com"
receiver_emails = ["yuvadilli2004@gmail.com","sathish.s1611@gmail.com", "sathishsathish41694@gmail.com","surendararikrish03@gmail.com","mohammadthayupe@gmail.com","lokeshbdms2003@gmail.com"]  # Add additional email addresses here

# App Password for Gmail
app_password = "ypzdzkwootyfjxsf"  # Replace with your app password

# Capture Video from Webcam
cap = cv2.VideoCapture(0)

# Wait for 2 seconds for the webcam to start
time.sleep(2)

# Create Motion Detection Object
motion_detector = cv2.createBackgroundSubtractorMOG2()

# Email Configuration
msg = EmailMessage()
msg['Subject'] = 'Intruder Alert!'
msg['From'] = sender_email
msg['To'] = ", ".join(receiver_emails)  # Join the email addresses with a comma and space


sent_msg_count=1

# Loop Through Video Frames
while True:
    ret, frame = cap.read()

    # Apply Motion Detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    mask = motion_detector.apply(gray)

    # Apply Thresholding
    threshold = cv2.threshold(mask, 20, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)

    # Find Contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw Contours
    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv2.putText(frame, "Intruder Detected", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # Save Image
        img_name = "intruder.jpg"
        cv2.imwrite(img_name, frame)

        # Send Email
        with open(img_name, 'rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name
        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)

            if sent_msg_count<=3:
                server.send_message(msg)
                sent_msg_count+=1

    cv2.imshow("Video Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


 
