"""Cloudflare R2 上传模板（S3 兼容）
免费档：存储 10GB-月，A 类操作 100 万次/月，B 类 1000 万次/月，出站免费
仅 Standard 存储有免费额度；不要用 Infrequent Access 蹭免费。
用法：
  R2_ENDPOINT=<https://<account>.r2.cloudflarestorage.com> \\
  R2_ACCESS_KEY_ID=<key> R2_SECRET_ACCESS_KEY=<secret> \\
  R2_BUCKET=<bucket> python3 upload.py <本地文件>
需要：pip install boto3
"""
import os, sys, boto3

ENDPOINT = os.environ["R2_ENDPOINT"]
BUCKET = os.environ["R2_BUCKET"]

s3 = boto3.client(
    "s3",
    endpoint_url=ENDPOINT,
    aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
    region_name="auto",
)

path = sys.argv[1]
key = os.path.basename(path)
s3.upload_file(path, BUCKET, key)
print(f"已上传 s3://{BUCKET}/{key}")
