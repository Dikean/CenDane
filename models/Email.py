import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, sender_email, password):
        self.sender_email = sender_email
        self.password = password
        self.context = ssl.create_default_context()

    def send_email(self, receiver_email, subject, text_content, html_content):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = receiver_email

        # Partes del mensaje en texto plano y HTML
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")

        # Agregar ambas partes al mensaje MIMEMultipart
        message.attach(part1)
        message.attach(part2)

        # Enviar el correo electrónico
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")

# Uso de la clase
if __name__ == "__main__":
    email_sender = EmailSender("dylan01aponte@gmail.com", "szab bkhv nosb pgkv")
    email_sender.send_email(
        "dylan01aponte@gmail.com",
        "Multipart Test",
        "Hi,\nHow are you?\nReal Python has many great tutorials:\nwww.realpython.com",
        "<html><body><p>Hi,<br>How are you?<br><a href='http://www.realpython.com'>Real Python</a> has many great tutorials.</p></body></html>"
    )
