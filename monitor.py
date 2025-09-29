import time
import smtplib
from email.message import EmailMessage

LOG_FILE = "predictions.log"
THRESHOLD = 2  # number of bad predictions to trigger alert
CHECK_INTERVAL = 10  # seconds

EMAIL_ADDRESS = "patelajmal04@gmail.com"
EMAIL_PASSWORD = "wrpv cwmz vpte iruq"

def send_email_alert(subject, body):
    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS  # you can also send to another email
    msg['Subject'] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print("Email alert sent!")

def monitor_logs():
    while True:
        try:
            with open(LOG_FILE, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("Log file not found yet.")
            time.sleep(CHECK_INTERVAL)
            continue

        bad_count = 0
        for line in lines[-10:]:  # check last 10 predictions
            if "Prediction:" in line:
                value = float(line.split("Prediction:")[1].strip())
                if value < 0:  # bad prediction
                    bad_count += 1

        print(f"Bad predictions in last 10 entries: {bad_count}")

        if bad_count > THRESHOLD:
            send_email_alert(
                "ML App Alert: Bad Predictions Detected",
                f"{bad_count} bad predictions detected in the last 10 entries!"
            )

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_logs()
