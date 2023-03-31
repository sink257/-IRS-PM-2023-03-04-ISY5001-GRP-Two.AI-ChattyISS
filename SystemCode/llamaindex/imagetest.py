import os
import re
import base64
os.environ['OPENAI_API_KEY'] = "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"
#os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
from langchain.llms import OpenAI
from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, ServiceContext
from llama_index.readers.file.base import (
    DEFAULT_FILE_EXTRACTOR, 
    ImageParser,
)
from llama_index.indices.query.query_transform.base import (
    ImageOutputQueryTransform,
)
#llm = HuggingFaceHub(repo_id="gpt2")
#llm = HuggingFaceHub(repo_id="google/flan-t5-xl", model_kwargs={"temperature":0, "max_length":64})
#llm_predictor = LLMPredictor(llm=llm)
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
# NOTE: By default, image parser converts image into text and discard the original image.  
#       Here, we explicitly keep both the original image and parsed text in an image document
image_parser = ImageParser(keep_image=True, parse_text=True)
file_extractor = DEFAULT_FILE_EXTRACTOR
file_extractor.update(
{
    ".jpg": image_parser,
    ".png": image_parser,
    ".jpeg": image_parser,
})
# NOTE: we add filename as metadata for all documents
filename_fn = lambda filename: {'file_name': filename}
image_reader = SimpleDirectoryReader(
    input_dir='data/test',
    file_extractor=file_extractor, 
    file_metadata=filename_fn,
)
image_documents = image_reader.load_data()
image_index = GPTSimpleVectorIndex.from_documents(image_documents, service_context=service_context)
while True:
    query = input('Enter your query: ')
    if query == "quit" or query == "exit":
        break
    #response = image_index.query(
    #    'Is there a map of NUS shuttle bus routes?',
    #    query_transform=ImageOutputQueryTransform(width=600)
    #)
    #print("Response START")
    #print(response)
    #print("Response END")
    response = image_index.query(
        query,
        query_transform=ImageOutputQueryTransform(width=600)
    )
    x = re.search('<img src="(.+)".+"\d+"', response.response)
    if x:
        print(x.group(1))
        with open(x.group(1), "rb") as image_file:
            data = base64.b64encode(image_file.read())
            print(data.decode("utf-8"))
            with open('output.txt','w') as f:
                f.write(data.decode("utf-8"))
    else:
        print('No image found.')
