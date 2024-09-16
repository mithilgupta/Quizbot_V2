# GitHub Actions taken from : https://www.youtube.com/watch?v=xs9oJaaU8I8&t=265s

import json
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.chains import RetrievalQA
# from langchain.llms import OpenAI

# Load and process the PDF
loader = PyPDFLoader("data/Lesson 2 _ Project Management 101 -uCertify.pdf")
documents = loader.load()

#1 Import boto3 and create client connection with bedrock
import boto3
client_bedrock=boto3.client('bedrock-runtime')
#print(boto3.__version__)

def lambda_handler(event, context):
#2 a. Store the input in a variable, b. print the event
    input_prompt=event['prompt']
    print(input_prompt)
	print("V4")
	# Split the documents into chunks
	text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
	texts = text_splitter.split_documents(documents)
	
	print(len(texts))
   
#3. Create  Request Syntax - Get details from console & body should be json object - use   json.dumps for body

    client_bedrockrequest=client_bedrock.invoke_model(
       contentType='application/json',
       accept='application/json',
       modelId='cohere.command-light-text-v14',
       body=json.dumps( {
        "prompt": input_prompt,
        "temperature": 0.9,
        "p": 0.75,
        "k": 0,
        "max_tokens": 100}))
    #print(client_bedrockrequest)    

#4. Convert Streaming Body to Byte(.read method) and then Byte to String using json.loads#

    client_bedrock_byte=client_bedrockrequest['body'].read()
    #print(client_bedrock_byte)
    #print(type(client_bedrock_byte))
#5 a. Print the event and type , b. Store the input in a variable

    client_bedrock_string=json.loads(client_bedrock_byte)
    #print(client_bedrock_string)
#6. Update the 'return' by changing the 'body'
    client_final_response=client_bedrock_string['generations'][0]['text']
    print(client_final_response)

    return {
        'statusCode': 200,
        'body': json.dumps(client_final_response)
    }