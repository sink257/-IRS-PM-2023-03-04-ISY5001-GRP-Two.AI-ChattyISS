import os
from pathlib import Path
from pdf2image import convert_from_path
from understandimages import tagImages
#from understandimages_llama import tagImages_llama
import time
import threading

def print_dots(stop_event):
    while not stop_event.is_set():
        print(".", end="", flush=True)
        time.sleep(1)


def generateImgFromPDF():
    import time
    start_time = time.time()
   
    stop_event = threading.Event()
    dot_printer = threading.Thread(target=print_dots, args=(stop_event,))
    dot_printer.start()
    print ("\nStep 1: Generation of Images from PDF file")
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
            image_path = image_output_folder/"page_{i+1}.jpg"
            i+=1
            image.save(image_path, "JPEG")

    elapsed_time = time.time() - start_time
    stop_event.set()
    dot_printer.join()
    print (f"Complete Generation of Images from PDF file, Elapsed time: {elapsed_time:.4f} seconds")


# Does the Tesseract OCT implementations
generateImgFromPDF()
tagImages() 
#tagImages_llama()