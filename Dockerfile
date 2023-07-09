FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.10
ENV AWS_DEFAULT_REGION ap-northeast-1
COPY requirements.txt ./
ADD data ./data
RUN pip3 install -r requirements.txt
COPY rekognition.py ./
ENV STAGE=dev
CMD ["rekognition.main"]
