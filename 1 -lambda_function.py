import json
import boto3
import base64
# Print the version of boto3
print(boto3.__version__)

# Create a client connection with Bedrock and S3 from this Lambda Function

client_bedrock = boto3.client('bedrock-runtime')
client_s3 = boto3.client('s3')

# Defining a Lambda Function Handler

def lambda_handler(event, context):
    input_prompt=event['prompt']
    print(input_prompt)
# Invoke the Bedrock Model (Titan Image Generator G1)
    response_bedrock = client_bedrock.invoke_model(
        modelId='amazon.titan-image-generator-v1',
        body=json.dumps({
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": input_prompt
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "height": 1024,
            "width": 1024,
            "cfgScale": 8.0,
            "seed": 0
        }
    }),
    contentType='application/json',
    accept='application/json'
    )
    print(response_bedrock)
    response_body=json.loads(response_bedrock['body'].read())
    print(response_body)
    
    image_data=response_body['images'][0]
    print(image_data)
    
    #Convert the image data from base64 string to bytes
    
    image_bytes=base64.b64decode(image_data)
    
    #Extract the image from the response_body
    
    # Set the S3 Bucket and Object Key
    
    bucket_name='imagefortesting2024'
    s3_object_key=f'generated_image.png'
    
    # Upload the Image to S3 bucket
    
    client_s3.put_object(
        Bucket=bucket_name,
        Key=s3_object_key,
        Body=image_bytes,
        ContentType='image/png'
        )
    
    # Generate a Presigned URL that allows someone to access the image using URL
    
    generate_presigned_url=client_s3.generate_presigned_url(
        'get_object',
        Params={'Bucket':bucket_name,'Key':s3_object_key},
        ExpiresIn=3600
        )
    #print(generate_presigned_url)
    
    # Return the response with the message and presigned URL
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message':'hello from lambda!!',
            'url':generate_presigned_url
        })
    }
