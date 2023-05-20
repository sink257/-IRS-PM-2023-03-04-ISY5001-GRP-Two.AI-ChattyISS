from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.document_loaders import TextLoader , CSVLoader
from langchain.document_loaders import UnstructuredPDFLoader, UnstructuredFileLoader
from langchain.document_loaders import PyMuPDFLoader
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
import faiss
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
import pandas as pd
from camelot import read_pdf
import os

#declare OpenAI key
os.environ["OPENAI_API_KEY"] = "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"

## Read in timetable first (currently supports pdf only) 
directory_path = './NUS-ISS documents/Timetable'
directory_files = os.listdir(directory_path)
j = 0
for files in directory_files:
    files = './NUS-ISS documents/Timetable/' + files
    all_tables = read_pdf(files, pages = 'all', copy_text=['v'])


    for i in range(all_tables.n):
      table = all_tables[i].df
      table = table[1:]
      temp_name = 'table{}'.format(j) + ".csv"
      path = "./processed_tables/" + temp_name
      table.to_csv(path, index = False)
      j += 1





## Read in all files##
directory_path = './NUS-ISS documents'
directory_files = os.listdir(directory_path)

#default chunk size for gpt3.5 simple
#text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=200)

#default chunk size for gpt3.5
#text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=4000, chunk_overlap=200)

#Increase chunk size for gpt-4
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=8000, chunk_overlap=200)


embeddings = OpenAIEmbeddings()



#load file by extension type, and split documents into chunk, add into vectorestore
for i in range(len(directory_files)):
  path = os.path.join(directory_path, directory_files[i])
  print(path)
  if path.endswith('.pdf'):
    loader =  PyMuPDFLoader(path)
    documents = loader.load()
    texts = text_splitter.split_documents(documents)
    if i==0:
      store = FAISS.from_documents(texts, OpenAIEmbeddings())
    else:
      store.add_documents(texts)
  if path.endswith('.txt'):
    loader =  TextLoader(path)
    documents = loader.load()
    texts = text_splitter.split_documents(documents)
    if i==0:
      store = FAISS.from_documents(texts, OpenAIEmbeddings())
    else:
      store.add_documents(texts)
      

      
      
      
      
## Add in processed timetable
directory_path = "./processed_tables/"
directory_files = os.listdir(directory_path)

for i in range(len(directory_files)):
  path = os.path.join(directory_path, directory_files[i])
  loader = CSVLoader(file_path=path, encoding = 'UTF-8')
  data = loader.load()
  store.add_documents(data)


#gpt3.5 save model
#store.save_local("./test/gpt3.5_small_model")
#store.save_local("./test/gpt3.5_model")

#gpt4save model
store.save_local("./test/gpt4_model")


    