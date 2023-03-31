import os
from pathlib import Path
from pdf2image import convert_from_path
from understandimages import tagImages

def generateImgFromPDF():
    # Set paths for input and output folders
    input_folder = Path("pdf")
    output_folder = Path("images")
    output_folder.mkdir(exist_ok=True)
    i = 0

    # Process all PDF files in the input folder
    for pdf_file in input_folder.glob("*.pdf"):
        pdf_path = str(pdf_file)
        images = convert_from_path(pdf_path)

        # Create a subfolder for each PDF's images
        pdf_name = pdf_file.stem
        image_output_folder = output_folder 

        # Save the extracted images
        for index, image in enumerate(images):
            image_path = image_output_folder / f"page_{i + 1}.jpg"
            i+=1
            image.save(image_path, "JPEG")


generateImgFromPDF()
tagImages() 