import boto3
from botocore.exceptions import NoCredentialsError

from constants.constant_env import DOWNLOAD_FOLDER_NAME, BUCKET_NAME, RESULT_FOLDER_NAME


class S3Helper:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def download_s3_stream(self, file_name, temp_video_path):
        try:
            object_key = f'{DOWNLOAD_FOLDER_NAME}/{file_name}'
            print(f"Baixando {object_key} do bucket {BUCKET_NAME} para {temp_video_path}...")

            with open(temp_video_path, 'wb') as f:
                with self.s3.get_object(Bucket=BUCKET_NAME, Key=object_key)['Body'] as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b""):  # Lendo 1MB por vez
                        f.write(chunk)

            print(f"Download concluído: {temp_video_path}")
        except NoCredentialsError:
            print("Credenciais não configuradas corretamente.")
            raise
        except Exception as e:
            print(f"Erro ao baixar o arquivo do S3: {e}")
            raise

    def upload_file_to_s3(self, local_path, result):
        try:
            self.s3.upload_file(local_path, BUCKET_NAME, result)
            print(f"Arquivo enviado para o S3")
        except Exception as e:
            print(f"Erro ao fazer upload para o S3: {e}")
            raise
