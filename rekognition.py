# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3,random
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

    try:
        with open(sourceFile, 'rb') as imageSource, open(targetFile, 'rb') as imageTarget:
            # SimilarityThreshold: 類似度の閾値
            response = client.compare_faces(
                SimilarityThreshold=0,
                SourceImage={'Bytes': imageSource.read()},
                TargetImage={'Bytes': imageTarget.read()}
            )
    except Exception as e:
        print("error")
        return



    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])

    return response['FaceMatches']

def imageCut(left, top, width, height, image):

    left = image.width * left
    top = image.height * top
    right = left + image.width * width
    bottom = top + image.height * height
    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save('./data/cropped.png')


def mc():
    response = openai.ChatCompletion.create(
    engine=deployment_name, # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
    messages=[
        {"role": "system", "content": "イベントに合わせて25文字以内の一言で客を盛り上げる役割です。"},
        {"role": "user", "content": "チームで開発をするイベントに参加しています。"}
    ]
    )

    with open("comment.txt", "w") as contents:
        contents.write(response['choices'][0]['message']['content'])

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('kokushimusou')
    bucket.upload_file('./comment.txt', 'coment.txt')
    print(response['choices'][0]['message']['content'])

def main():
    global target_file
    s3 = boto3.client('s3')
    s3.download_file('kokushimusou', 'hack_test.png', './data/getimg.png')
    file_num = [random.randint(1, 40)  for _ in range(5)]
    Similarity ,Similarity_degree = [], []
    target_file = "./data/getimg.png"
    for num in file_num:
        source_file = f"./data/source{num}.png"
        face_matches = compare_faces(source_file, target_file)
        if(face_matches):
            Similarity.append([face_matches[0],source_file])
            Similarity_degree.append(face_matches[0]["Similarity"])
    index = Similarity_degree.index(max(Similarity_degree))
    print(Similarity_degree)
    print(index)

    image = Image.open(target_file)
    imageCut(
        Similarity[index][0]["Face"]["BoundingBox"]["Left"],
        Similarity[index][0]["Face"]["BoundingBox"]["Top"],
        Similarity[index][0]["Face"]["BoundingBox"]["Width"],
        Similarity[index][0]["Face"]["BoundingBox"]["Height"],
        image
    )

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('kokushimusou')
    bucket.upload_file(Similarity[index][1],'similar.png')
    bucket.upload_file('./data/cropped.png', 'cropped.png')
    print(source_file)
    print(f"Similarity: {Similarity[index][0]['Similarity']}")
    # print("Face matches: " + str(face_matches))
    mc()

if __name__ == "__main__":
    main()


