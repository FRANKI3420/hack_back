# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
from PIL import Image
import os
import openai
openai.api_type = "azure"
openai.api_version = "2023-05-15" 
openai.api_base = "https://chatgpt-mc-westeurope.openai.azure.com/"  # Your Azure OpenAI resource's endpoint value.
openai.api_key = "7b78d5788869441b82ddd8cf3754d1b9"
deployment_name='chatgpt-mc-westeurope'

# sourceFile: ベースとなる画像, targetFile: 比較対象の画像
def compare_faces(sourceFile, targetFile):
    session = boto3.Session(profile_name='default')
    client = session.client('rekognition')

    with open(sourceFile, 'rb') as imageSource, open(targetFile, 'rb') as imageTarget:
        # SimilarityThreshold: 類似度の閾値
        response = client.compare_faces(
            SimilarityThreshold=0,
            SourceImage={'Bytes': imageSource.read()},
            TargetImage={'Bytes': imageTarget.read()}
        )

    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])

    return response['FaceMatches']

def imageCut(left, top, width, height):
    image = Image.open(target_file)
    left = image.width * left
    top = image.height * top
    right = left + image.width * width
    bottom = top + image.height * height
    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save('./data/cropped.jpg')

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('kokushimusou')
    bucket.upload_file('./data/cropped.jpg', 'cropped.jpg')
    

target_file = "./data/target.jpg"

def mc():
    response = openai.ChatCompletion.create(
    engine=deployment_name, # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
    messages=[
        {"role": "system", "content": "イベントに合わせて一言で客を盛り上げる役割です。"},
        {"role": "user", "content": "チームで開発をするイベントに参加しています。"}
    ]
    )

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('kokushimusou')
    bucket.upload_file('./data/comment.txt.', 'cropped.jpg')

    print(response['content'])

def main():
    s3 = boto3.client('s3')
    s3.download_file('kokushimusou', 'hack_test.png', './data/test_1.png')

    source_file = "./data/source2.png"
    target_file = "./data/test_1.png"
    face_matches = compare_faces(source_file, target_file)
    imageCut(
        face_matches[0]["Face"]["BoundingBox"]["Left"],
        face_matches[0]["Face"]["BoundingBox"]["Top"],
        face_matches[0]["Face"]["BoundingBox"]["Width"],
        face_matches[0]["Face"]["BoundingBox"]["Height"]
    )

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('kokushimusou')
    bucket.upload_file(source_file,'similar.jpg')
    print(f"Similarity: {face_matches[0]['Similarity']}")
    # print("Face matches: " + str(face_matches))
    mc()

if __name__ == "__main__":
    main()
