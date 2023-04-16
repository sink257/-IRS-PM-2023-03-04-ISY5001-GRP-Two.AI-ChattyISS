import pytesseract
import string
from pathlib import Path
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
from nltk.util import ngrams

import nltk
import json
import time
import threading

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Update this path to match your system


 

# Define similarity threshold
similarity_threshold = 0.3

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def preprocess_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Tokenize text
    tokens = word_tokenize(text)

    # Convert to lowercase
    tokens = [word.lower() for word in tokens]

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return tokens



def jaccard_similarity(a, b):
    a = set(a)
    b = set(b)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def print_dots(stop_event):
    while not stop_event.is_set():
        print(".", end="", flush=True)
        time.sleep(1)

def tagImages():
    import time
    start_time = time.time()
    print ("\nStep 2: Tagging images according to Tessaract")
    stop_event = threading.Event()
    dot_printer = threading.Thread(target=print_dots, args=(stop_event,))
    dot_printer.start()
    # Set the folder containing your images
    image_folder = Path("images")

    # Initialize the text_tokens dictionary
    text_tokens = {}

    # Loop through all images in the image folder
    for image_file in image_folder.glob("*.jpg"):
        image_path = str(image_file)

        # Extract text from the image using Tesseract OCR
        text = pytesseract.image_to_string(image_path)

        # Preprocess and tokenize the text
        preprocessed_text = preprocess_text(text)
        text_tokens[' '.join(preprocessed_text)] = image_path

    # Save the text_tokens dictionary to a JSON file
    with open("text_tokens.json", "w") as outfile:
        json.dump(text_tokens, outfile)

    elapsed_time = time.time() - start_time
    stop_event.set()
    dot_printer.join()
    print (f"Complete Tagging images according to Tessaract, Elapsed time: {elapsed_time:.4f} seconds")

def findSuitableImage(search_string, text_tokens):
    search_tokens = preprocess_text(search_string)
    # Calculate Jaccard similarity
    print(f"Size of text_tokens: {len(text_tokens)}")
    for key, value in text_tokens.items():
        similarity = jaccard_similarity(search_tokens, key)
        # Check if the similarity is above the defined threshold
        if similarity >= similarity_threshold:
            print(f"Image with a similarity of {similarity:.2f} found: {value}")
            return value
    return ""

def findSuitableImage2(search_string, text_tokens):
    search_tokens = preprocess_text(search_string)

    # Calculate the total number of words in search_tokens
    total_words = len(search_tokens)

    # Print the size of the text_tokens dictionary
    print(f"Size of text_tokens: {len(text_tokens)}")

    max_proportion = 0  # Initialize a variable to store the maximum proportion
    max_value = None  # Initialize a variable to store the value corresponding to the maximum proportion

    for key, value in text_tokens.items():
        key_tokens = key.split()  # Convert the key back to a list of tokens

        # Calculate the intersection between search_tokens and key_tokens
        intersection = set(search_tokens).intersection(set(key_tokens))

        # Calculate the proportion of the intersection to the total number of words in search_tokens
        proportion = len(intersection) / total_words

        # Update the maximum proportion and corresponding value if needed
        if proportion >= similarity_threshold and proportion > max_proportion:
            max_proportion = proportion
            max_value = value
            print(f"Image with a similarity of {proportion:.2f} found: {value}")

    return max_value if max_value else ""

def findSuitableImage3(search_string, text_tokens):
    search_tokens = preprocess_text(search_string)
    
    
    
    # Print the size of the text_tokens dictionary
    print(f"Size of text_tokens: {len(text_tokens)}")
    
    for key, value in text_tokens.items():
        key_tokens = key.split()  # Convert the key back to a list of tokens
        # Calculate the total number of words in search_tokens
        total_words = len(key_tokens)
        
        # Calculate the intersection between search_tokens and key_tokens
        intersection = set(search_tokens).intersection(set(key_tokens))
        
        # Calculate the proportion of the intersection to the total number of words in search_tokens
        proportion = len(intersection) / total_words
        
        # Check if the proportion is above the defined threshold
        if proportion >= similarity_threshold:
            print(f"Image with a similarity of {proportion:.2f} found: {value}")
            return value
        else:
            print(f"intesection: {len(intersection)}, total words: {total_words}, {proportion}")
            
    return ""







def clearAndLoadTextTokensFromFile():
    text_tokens = {}
    # Load the text_tokens dictionary from the JSON file
    with open("text_tokens.json", "r") as infile:
        text_tokens = json.load(infile)
        print(f"Size of text_tokens: {len(text_tokens)}")
        return text_tokens

   
