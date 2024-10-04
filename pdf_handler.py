
import PyPDF2
import requests
from io import BytesIO
from PIL import Image


# Convert images to PDFs
def images_to_pdfs(image_urls):
    pdf_streams = []  # List to hold the in-memory PDFs

    for image_url in image_urls:
        res = requests.get(image_url)
        if res.status_code == 200:
            img_data = BytesIO(res.content)  # Store image data in memory
            with Image.open(img_data) as img:
                img = img.convert('RGB')  # Convert image to RGB

                pdf_stream = BytesIO()  # Creates an in-memory BytesIO object for the PDF
                img.save(pdf_stream, format="PDF")  # Saves the image as a PDF to the BytesIO object
                pdf_stream.seek(0)  # Move the pointer to the start of the BytesIO object
                pdf_streams.append(pdf_stream)  # Add the in-memory PDF to the list

        else:
            print(f"Failed to download image from {image_url}")

    return pdf_streams


# Merge multiple PDFs into one
def merge_pdfs(pdf_streams, output_pdf):
    pdf_merger = PyPDF2.PdfMerger()

    for pdf_stream in pdf_streams:
        pdf_merger.append(pdf_stream)

    with open(output_pdf, 'wb') as final_pdf:
        pdf_merger.write(final_pdf)
        final_pdf.close()
