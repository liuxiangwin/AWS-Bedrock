import json
import boto3

def initialize_bedrock_client():
    return boto3.client('bedrock-runtime')

def invoke_bedrock_model(client, user_prompt):
    """
    Invokes the AWS Bedrock Model ith the given Input.
    Paramters:
      client: Initialized the Bedrock Client.
      user_prompt: The prompt to send to the model.
    
    Returns:
      The response from the model as a string

    """
    response = client.invoke_model(
        modelId="anthropic.claude-instant-v1",
        contentType="application/json",
        accept="*/*",
        body=json.dumps({
            "prompt": f"\n\nHuman: {user_prompt}\n\nAssistant:",
            "max_tokens_to_sample": 600,
            "temperature": 1,
            "top_p": 1,
            "top_k": 250,
            "stop_sequences": ["\n\nHuman:"],
            "anthropic_version": "bedrock-2023-05-31"
        })
    )
    raw_body = response['body'].read()
    response_body = json.loads(raw_body)
    return response_body.get('completion', 'No response received.')
    
