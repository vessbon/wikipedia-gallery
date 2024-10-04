# [ -- LIBRARIES START

# General
import scraper
import pdf_handler
import email_handler

# Information
from getpass import getpass

# Time
from time import time
from datetime import datetime

# Files
import zipfile
import os

# Csv
import csv

# -- LIBRARIES END ]


FINAL_PDF_END = 'gallery.pdf'
FINAL_CSV_END = 'date_data.csv'

send_email = True
attachment_paths = []


class Gallery:
    def __init__(self, image_urls):
        self.images = image_urls
        self.pdfs = []

    # Creates a PDF file for each image
    def generate_pdfs(self):
        self.pdfs = pdf_handler.images_to_pdfs(self.images)

    # Merge the PDFs into one
    def merge_pdfs(self, gallery_location):
        pdf_handler.merge_pdfs(self.pdfs, gallery_location)


if __name__ == '__main__':
    # Scraping preparation
    wikipedia_articles = [
        'https://en.wikipedia.org/wiki/History_of_atomic_theory',
        'https://en.wikipedia.org/wiki/Isaac_Newton'
    ]

    # Email preparation
    info = {'email': '', 'password': '', 'subject': ''}

    recipients = [  # Only accepts gmails (@gmail.com domain)
        'example1@gmail.com',
        'example2@gmail.com'
    ]

    if send_email:
        info['email'] = input("Email: ")
        info['password'] += getpass("Password: ")
        info['subject'] = input("Enter the subject line: ")

    # Starts timer after input
    start_time = time()

    # Get images as urls
    images = scraper.get_wikipedia_images(wikipedia_articles)
    # Join the lists of urls from the different pages into one list
    joined_images = []
    for image_list in images:
        joined_images.extend(image_list)

    # Create gallery
    gallery = Gallery(joined_images)
    gallery.generate_pdfs()
    gallery.merge_pdfs('Payload\\' + FINAL_PDF_END)

    # Create CSV file
    now = datetime.now()

    date_data = open('Payload\\' + FINAL_CSV_END, encoding='utf-8', mode='w', newline='')
    csv_writer = csv.writer(date_data, delimiter=',')

    # Create date information as rows
    csv_writer.writerow(['Year', 'Month', 'Day', 'Hour', 'Second', 'Microsecond'])
    csv_writer.writerow([now.year, now.month, now.day, now.hour, now.second, now.microsecond])
    date_data.close()

    # Zip files
    path_to_compressed_file = 'Payload\\gallery.zip'
    compressed_file = zipfile.ZipFile(path_to_compressed_file, 'w')
    compressed_file.write('Payload\\' + FINAL_PDF_END, arcname=FINAL_PDF_END, compress_type=zipfile.ZIP_DEFLATED)
    compressed_file.write('Payload\\' + FINAL_CSV_END, arcname=FINAL_CSV_END, compress_type=zipfile.ZIP_DEFLATED)
    compressed_file.close()
    attachment_paths.append(path_to_compressed_file)

    files = os.listdir('Payload')
    for file in files:
        file_path = os.path.join('Payload', file)
        if os.path.isfile(file_path) and 'zip' not in file_path:
            os.remove(file_path)
        else:
            print(file_path)

    # Email sending
    if send_email:
        host = 'smtp.gmail.com'
        port = 587

        body = f'It took {(time() - start_time):.3f}s to start sending this email.'
        email_handler.send_with_attachments(info['email'], recipients, info['subject'], body, attachment_paths,
                                            host, port, info['email'], info['password'])

    # Ends timer
    end_time = time()
    elapsed_time = end_time - start_time
    print(elapsed_time)