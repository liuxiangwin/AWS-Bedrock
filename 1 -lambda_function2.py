import json
import boto3
import base64
# print the boto3 version
#print(boto3.__version__)

client_bedrock = boto3.client('bedrock-runtime')
client_s3 = boto3.client('s3')

#Creating a function to give the text input the Lambda Function

def lambda_handler(event, context):
    input_prompt = event['prompt']
    print(input_prompt)
    
# Invoke the Bedrock model (Stable Diffusion to Generate text to Image)
    
    response_bedrock = client_bedrock.invoke_model(
        contentType='application/json',
        accept='application/json',
        modelId='stability.stable-diffusion-xl-v1',
        body=json.dumps({
            "text_prompts": [{"text": input_prompt }],
            "cfg_scale": 10,
            "seed": 0,
            "steps":30
            })
        )

# Processing the Bedrock stable diffusion model response

    response_bedrock_byte=json.loads(response_bedrock['body'].read())
    print(response_bedrock_byte['result'])
    base64_image=response_bedrock_byte.get("artifacts")[0].get("base64")
    base64_bytes=base64_image.encode('ascii')
    image_bytes=base64.b64decode(base64_bytes)

# Define the name of the Bucket and Object Key Name
    
    bucket_name = 'texttoimagestable'
    s3_object_key = 'stableimage.png'

# Upload the Image to S3 Bucket
    client_s3.put_object (
        Bucket=bucket_name,
        Key=s3_object_key,
        Body=image_bytes,
        ContentType='image/png'
        )

# Generate a Presigned URL to access the image from s3 bucket

    generate_presigned_url = client_s3.generate_presigned_url (
        'get_object',
        Params={'Bucket': bucket_name, 'Key': s3_object_key},
        ExpiresIn=3600
        )
    print(generate_presigned_url)


    return {
        'statusCode': 200,
        'body': json.dumps({
            'messgae': 'Hello from Lamda, code executed successfully',
            'url': generate_presigned_url
        })
    }
