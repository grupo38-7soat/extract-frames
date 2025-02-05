import boto3
from botocore.exceptions import NoCredentialsError

class S3Helper:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def download_file_from_s3(self, bucket_name, s3_key, local_path):
        try:
            self.s3.download_file(bucket_name, s3_key, local_path)
            print(f"Arquivo baixado do S3: s3://{bucket_name}/{s3_key} -> {local_path}")
        except NoCredentialsError:
            print("Credenciais não configuradas corretamente.")
            raise
        except Exception as e:
            print(f"Erro ao baixar o arquivo do S3: {e}")
            raise

    def upload_file_to_s3(self, local_path, bucket_name, s3_key):
        try:
            self.s3.upload_file(local_path, bucket_name, s3_key)
            print(f"Arquivo enviado para o S3: {local_path} -> s3://{bucket_name}/{s3_key}")
        except Exception as e:
            print(f"Erro ao fazer upload para o S3: {e}")
            raise