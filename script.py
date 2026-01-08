import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import smtplib
from dotenv import load_dotenv

load_dotenv()

current_day = datetime.now().day
current_month = datetime.now().month
current_year = datetime.now().year

LAST_URL_FILE = "last_url.txt"
SMTP_SERVER = "smtp.sapo.pt"
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

receiver_raw = os.getenv("EMAIL_RECEIVER", "")
EMAIL_RECEIVER = [e.strip() for e in receiver_raw.split(",") if e.strip()]

SUBJECT = f"Votações AR - {current_day}/{current_month}/{current_year}"
BODY = "Attached is the latest voting results PDF."

def load_last_url():
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, LAST_URL_FILE)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read().strip()
    return None

def save_last_url(file_name):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, LAST_URL_FILE)
    print(f"Saving last URL to {file_name} in {file_path}")
    with open(file_path, "w") as f:
        f.write(file_name)

def get_latest_pdf_url():
    url = "https://www.parlamento.pt/ArquivoDocumentacao/Paginas/Arquivodevotacoes.aspx"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch the webpage.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    latest_div = soup.find('div', class_='row home_calendar hc-detail')
    if not latest_div:
        print("No voting results found.")
        return None

    pdf_link = latest_div.find('a', href=True)
    if pdf_link:
        return pdf_link['href']
    return None

def strip_file_name(file_name):
    try:
        return file_name.split("Fich=")[1].split(".pdf")[0]
    except (IndexError, AttributeError):
        return file_name

def download_pdf(pdf_url, save_path):
    response = requests.get(pdf_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"PDF downloaded successfully: {save_path}")
        return True
    print("Failed to download PDF.")
    return False

def send_email_with_attachment(smtp_server, smtp_port, sender_email, sender_password, receiver_emails, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(receiver_emails)  # Convert list to comma-separated string
    msg["Subject"] = subject

    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
    msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_emails, msg.as_string())  # Send to all emails

    print("Email sent successfully!")


def main():
    pdf_url = get_latest_pdf_url()
    if not pdf_url:
        print("No PDF link found!")
        return

    # NEW — Do not process if URL is the same
    last_url = load_last_url()
    current_pdf_name = strip_file_name(pdf_url)
    last_pdf_name = strip_file_name(last_url)
    print(f"Current PDF name: {current_pdf_name}")
    print(f"Last PDF name: {last_pdf_name}")

    if current_pdf_name == last_pdf_name:
        print("Same PDF URL as yesterday. Skipping download and email.")
        save_last_url(current_pdf_name)
        return

    save_last_url(current_pdf_name)
    pdf_filename = "latest_voting_results.pdf"
    downloaded = download_pdf(pdf_url, pdf_filename)

    if downloaded:
        send_email_with_attachment(
            SMTP_SERVER,
            SMTP_PORT,
            EMAIL_SENDER,
            EMAIL_PASSWORD,
            EMAIL_RECEIVER,
            SUBJECT,
            BODY,
            pdf_filename
        )        

        os.remove(pdf_filename)

if __name__ == "__main__":
    main()