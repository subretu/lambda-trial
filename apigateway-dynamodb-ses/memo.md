- API GatewayでAPIを作るときは「REST API」にすること。
- s3で静的ホスティングを行う場合。
  - 本の記載内容が古く、そのままやってもオブジェクトをパブリックアクセスにできないので注意。
  - パブリックアクセスをブロックをオフにする。
  - バケットポリシーを下記のようにする。
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::バケット名/*"
        }
    ]
}
  ```