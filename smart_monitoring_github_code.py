# =====================================================
# AI Based Smart Environment & Safety Monitoring System
# Final Simulation Code with Dashboard + Email Alerts
# =====================================================

from Adafruit_IO import Client
import time
import random
import smtplib
from email.mime.text import MIMEText

# =====================================================
# ADAFRUIT IO DETAILS
# =====================================================

AIO_USERNAME = "your_aio_username"
AIO_KEY = "YOUR_ADAFRUIT_KEY"

aio = Client(AIO_USERNAME, AIO_KEY)

# =====================================================
# EMAIL DETAILS
# =====================================================

sender_email = "your_email@gmail.com"
receiver_email = "receiver_email@gmail.com"
app_password = "your_app_password"

# =====================================================
# SEND DATA TO CLOUD
# =====================================================

def send_data(feed, value):
    try:
        aio.send(feed, value)
    except:
        print("Cloud send error:", feed)

# =====================================================
# SEND EMAIL ALERT
# =====================================================

def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("Email Sent Successfully")

    except Exception as e:
        print("Email Error:", e)

# =====================================================
# MAIN LOOP
# =====================================================

while True:

    # ---------------------------------
    # Simulated Sensor Values
    # ---------------------------------
    temperature = random.randint(25, 45)
    gas = random.randint(100, 500)
    motion = random.randint(0, 1)
    light = random.randint(100, 800)

    # ---------------------------------
    # Reset Risk Score
    # ---------------------------------
    risk_score = 0

    # ---------------------------------
    # AI Decision Logic
    # ---------------------------------
    if temperature > 38:
        risk_score += 30

    if gas > 300:
        risk_score += 40

    if motion == 1:
        risk_score += 20

    if light < 300:
        risk_score += 10

    # ---------------------------------
    # Status Decision
    # ---------------------------------
    if risk_score >= 70:
        status = "DANGER"
        alert = "Critical unsafe environment detected. Immediate action required."

    elif risk_score >= 40:
        status = "WARNING"
        alert = "Abnormal conditions detected. Please inspect the area."

    else:
        status = "SAFE"
        alert = "System operating under normal conditions."

    # ---------------------------------
    # Send Data to Dashboard
    # ---------------------------------
    send_data("temperature", temperature)
    send_data("gas", gas)
    send_data("motion", motion)
    send_data("light", light)
    send_data("risk-score", risk_score)
    send_data("status", status)
    send_data("alerts", alert)

    # ---------------------------------
    # Email Alert Only for Warning/Danger
    # ---------------------------------
    if status != "SAFE":
        send_email(
            "Smart Monitoring Alert",
            f"""
Status: {status}

Temperature: {temperature} °C
Gas Level: {gas}
Motion: {motion}
Light: {light}
Risk Score: {risk_score}

Message:
{alert}
"""
        )

    # ---------------------------------
    # Console Output
    # ---------------------------------
    print("Temperature:", temperature)
    print("Gas:", gas)
    print("Motion:", motion)
    print("Light:", light)
    print("Risk Score:", risk_score)
    print("Status:", status)
    print("Alert:", alert)
    print("-----------------------------------")

    time.sleep(5)
