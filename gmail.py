import smtplib
import ssl

sender_email = "antiolensults@gmail.com"
password = "pythontest"

receiver_email = "to@email.com"
port = 465  # For SSL


def send_email(city, date):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        content = f'New time available in "{city}"\n\n{date.day:02d}.{date.month:02d}.{date.year}\n{date.hour}:{date.minute:02d}'
        server.sendmail(sender_email, receiver_email, content)


if __name__ == "__main__":
    from datetime import datetime
    date_format = "%d.%m.%Y %H:%M"
    date = datetime.strptime("13.01.2021 10:00", date_format)
    send_email("Rakvere", date)
