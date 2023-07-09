# KDDIHacks2023-TeamF-api


## デプロイ手順
1. コンテナビルド
    ```
    docker build -t lambda_container_demo .
    ```
2. タグ付け
    ```
    docker tag lambda_container_demo:latest \
    ${ACCOUNTID}.dkr.ecr.${REGION}.amazonaws.com/lambda_container_demo:latest
    ```
3. ECRにプッシュ
    ```
    docker push ${ACCOUNTID}.dkr.ecr.${REGION}.amazonaws.com/lambda_container_demo:latest
    ```
