#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
from PIL import Image

# sourceFile: ベースとなる画像, targetFile: 比較対象の画像
def compare_faces(sourceFile, targetFile):

    seesion = boto3.Session(profile_name='default')
    client=boto3.client('rekognition')
   
    imageSource=open(sourceFile,'rb')
    imageTarget=open(targetFile,'rb')

    # SimilarityThreshold: 類似度の閾値
    response=client.compare_faces(SimilarityThreshold=0,
                                  SourceImage={'Bytes': imageSource.read()},
                                  TargetImage={'Bytes': imageTarget.read()})
    

    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])

    imageSource.close()
    imageTarget.close()     
    return response['FaceMatches']    

def imageCut(left,top,width,height):
    image = Image.open(target_file)
    left = image.width * left
    top = image.height * top
    right = left + image.width * width
    bottom = top + image.height * height
    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save('./data/cropped.jpg')

    s3 = boto3.resource('s3') #S3オブジェクトを取得
    bucket = s3.Bucket('バケット名')
    bucket.upload_file('UPするファイルのpath', '保存先S3のpath')
    
target_file = "./data/target.jpg"

def main():
    s3 = boto3.resource('s3') #S3オブジェクトを取得
    bucket = s3.Bucket('バケット名')
    target_file = bucket.download_file('S3のバケット以下のpath', '保存先のpath')

    source_file = "./data/source.jpg"
    # target_file = "./data/target.jpg"
    face_matches = compare_faces(source_file, target_file)
    imageCut(face_matches[0]["Face"]["BoundingBox"]["Left"],
             face_matches[0]["Face"]["BoundingBox"]["Top"],
             face_matches[0]["Face"]["BoundingBox"]["Width"],
             face_matches[0]["Face"]["BoundingBox"]["Height"],
             )
    
    print(f"Similarity:{face_matches[0]['Similarity']}")
    # print("Face matches: " + str(face_matches))



if __name__ == "__main__":
    main()