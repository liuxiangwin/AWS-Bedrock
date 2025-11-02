import json
import boto3

# Creating a client connection with Bedrock from this Lambda Function

client_bedrock = boto3.client('bedrock-runtime')

# Creating a function to provide the input text for summarization

def lambda_handler(event, context):
    input_prompt=event['prompt']
    print(input_prompt)

# Invoking the Cohere Command Text model for summarization

    client_bedrockrequest = client_bedrock.invoke_model(
        contentType='application/json',
        accept='application/json',
        modelId='cohere.command-text-v14',
        body=json.dumps({
            "prompt": input_prompt,
            "temperature": 0.9,
            "p": 0.75,
            "k": 0,
            "max_tokens": 50}))
    #print(client_bedrockrequest)
    
    #Read the response from Foundation model and then converts it into bytes
    
    client_bedrock_byte=client_bedrockrequest['body'].read()
    
    # Convert the byte data into a Python Dictionary
    
    client_bedrock_string=json.loads(client_bedrock_byte)
    
    #print(client_bedrock_string)
    
    client_final_response=client_bedrock_string['generations'][0]['text']
    
    #print(client_final_response)

    return {
        'statusCode': 200,
        'body': client_final_response
    }