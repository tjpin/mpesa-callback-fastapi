import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.utils import make_msgid
from redmail import EmailSender
from dotenv import load_dotenv
import os


load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


class MailProvider:
    mail = EmailSender(host="smtp.gmail.com", port=587,
                    username=EMAIL, password=PASSWORD)

    def __init__(self, sender_address, receiver_address, password):
        self.sender_address = sender_address,
        self.receiver_address = receiver_address,
        self.password = password

    def send_otp_mail(self, r, otp: str):
        html_ = """
            <Body>
                <div class="content"">
                    <p style="color: #fff; text-align: center; font-weight: bold; font-size: 40px;">tPay</p>
                </div>
                <h2> Enter this OTP to reset your password 👇</h2>
                <strong><h2 style="color: #0091ff;">{{ otp }}</h2></strong>
                <h1 style="color: #00ff00; font-weight: bold;"> {{ logo }} </h1>
            </Body>
        """
        impath = "D:/python-projects/apis/mpesa/auth/tpay.png"
        self.mail.send(
            sender=self.sender_address,
            receivers=[r, ],
            subject="TCStudios OTP",
            html=html_,
            body_params={'otp': otp},
            body_images={'logo': impath}
        ).as_string()
        print(f"Email sent to {self.receiver_address}")

