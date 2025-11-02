import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.indexes import VectorstoreIndexCreator
from langchain_aws import BedrockLLM

# Define a function for below steps

def health_index():
    # Define the data source and load data using PyPDFLOADER
    
    data_load=PyPDFLoader('E:/GenerativeAI/RAG/Patient_Report.pdf')
    
    # Split the Text based on Characters etc
    
    data_split=RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size=100, chunk_overlap=20)
    
    # Create text Embeddings
    # 
    data_embeddings=BedrockEmbeddings(
    credentials_profile_name='default',
    model_id='amazon.titan-embed-text-v1'
    )
    
    data_index=VectorstoreIndexCreator(
    text_splitter=data_split,
    embedding=data_embeddings,
    vectorstore_cls=FAISS
    )
    
    db_index=data_index.from_loaders([data_load])
    
    return db_index

# Create a function to connect with Claude FM for processing enriched queries

def health_llm():
    llm=BedrockLLM(
        credentials_profile_name='default',
        model_id='anthropic.claude-v2',
        model_kwargs={
            "max_tokens_to_sample": 3000,
            "temperature": 0.1,
            "top_p": 0.9})
    return llm

# Write a function which take the user input, searches the best match from the Vector DB and finally send (user query + retrieved output from the embedding FM) to the LLM

def health_rag_response(index, question):
    rag_llm=health_llm()
    health_rag_query=index.query(question=question, llm=rag_llm)
    return health_rag_query

