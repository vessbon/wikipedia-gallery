
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def send_with_attachments(sender, recipients, subject, body, attachment_paths,
                          smtp_host, smtp_port, smtp_user, smtp_pass):

    # Create SMTP server connection
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(smtp_user, smtp_pass)

    for recipient in recipients:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        # Loop through the list of attachment paths and attach each file
        for attachment_path in attachment_paths:
            if os.path.isfile(attachment_path):  # Check if the file exists
                attachment = open(attachment_path, 'rb')
                mime_base = MIMEBase('application', 'octet-stream')
                mime_base.set_payload(attachment.read())
                encoders.encode_base64(mime_base)

                # Add header to the attachment part
                mime_base.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(attachment_path)}'
                )

                # Attach the file to the message
                msg.attach(mime_base)
            else:
                print(f"Attachment {attachment_path} not found. Skipping it.")

            # Convert the message to a string
            email_content = msg.as_string()
            # Send it to recipient inbox
            server.sendmail(sender, recipient, email_content)

    print("Emails sent successfully!")
