import json
from time import time
from datetime import datetime

import os
from constants.constant_env import OUTPUT_FRAMES_DIR_NAME, OUTPUT_ZIP_DIR_NAME, \
    AWS_REGION, DYNAMO_TABLE_NAME, DYNAMO_STATUS_START_PROCESS, \
    DYNAMO_STATUS_DOWNLOAD_VIDEO_IN_PROGRESS, DYNAMO_STATUS_PROCESSING_CUT_FRAMES,\
    DYNAMO_STATUS_ZIP_FILE_IN_PROGRESS, DYNAMO_STATUS_UPLOAD_RESULT_IN_PROGRESS, \
    DYNAMO_STATUS_ERROR, DYNAMO_STATUS_END_PROCESS, OUTPUT_DOWNLOAD_DIR_NAME, \
    RESULT_FOLDER_NAME
from repository.dynamo_db import DynamoRepository
from services.extract_frames import ExtractFrames
from services.s3_helper import S3Helper
from utils.delete_folder import delete_folder
from utils.generate_hash import generate_hash
from utils.zip_folder import zip_folder


class SagaControl(object):
    def __init__(self, payload):
        self.dynamo_aux = DynamoRepository(AWS_REGION, DYNAMO_TABLE_NAME)
        self.datetime_aux = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.payload = payload
        self.user = payload.get('user')
        self.video_name = payload.get('video_name')
        self.start_time_for_cut_frames = payload.get('start_time_for_cut_frames')
        self.end_time_for_cut_frames = payload.get('end_time_for_cut_frames')
        self.skip_frame = payload.get('skip_frame')
        self.identification = generate_hash(f'{self.user}-{self.datetime_aux}-{self.video_name}')

    def __start_process(self):
        try:
            self.dynamo_aux.create_item(
                identification=self.identification,
                datetime=self.datetime_aux,
                date=datetime.now().strftime('%Y-%m-%d'),
                user=self.user,
                result_url=None,
                status=DYNAMO_STATUS_START_PROCESS,
                payload_inbound=json.dumps(self.payload),
                video_name=self.video_name
            )
        except Exception as e:
            print(f'Error creating item in dynamo: {e}')
            raise

    def __download_video(self):
        try:
            self.dynamo_aux.update_item(
                user=self.user,
                datetime=self.datetime_aux,
                status=DYNAMO_STATUS_DOWNLOAD_VIDEO_IN_PROGRESS
            )
            temp_dir_for_download = OUTPUT_DOWNLOAD_DIR_NAME
            if not os.path.exists(temp_dir_for_download):
                os.makedirs(temp_dir_for_download)

            S3Helper().download_s3_stream(self.video_name, f'{OUTPUT_DOWNLOAD_DIR_NAME}/{self.video_name}')
        except Exception as e:
            print(f'Error downloading video: {e}')
            raise

    def __extract_frames(self):
        try:
            self.dynamo_aux.update_item(
                user=self.user,
                datetime=self.datetime_aux,
                status=DYNAMO_STATUS_PROCESSING_CUT_FRAMES
            )
            ExtractFrames(end_time=600, frame_skip=1).run(f'{OUTPUT_DOWNLOAD_DIR_NAME}/{self.video_name}')
        except Exception as e:
            print(f'Error extracting frames: {e}')
            raise

    def __zip_frames(self):
        try:
            self.dynamo_aux.update_item(
                user=self.user,
                datetime=self.datetime_aux,
                status=DYNAMO_STATUS_ZIP_FILE_IN_PROGRESS
            )
            zip_folder(OUTPUT_FRAMES_DIR_NAME, OUTPUT_ZIP_DIR_NAME, f'{self.identification}.zip')
        except Exception as e:
            print(f'Error zipping frames: {e}')
            raise

    def __upload_zip(self):
        try:
            self.dynamo_aux.update_item(
                user=self.user,
                datetime=self.datetime_aux,
                status=DYNAMO_STATUS_UPLOAD_RESULT_IN_PROGRESS
            )
            S3Helper().upload_file_to_s3(f'{OUTPUT_ZIP_DIR_NAME}/{self.identification}.zip',
                                         f'{RESULT_FOLDER_NAME}/{self.user}/{self.identification}.zip')
        except Exception as e:
            print(f'Error uploading zip: {e}')
            raise

    def __end_process(self):
        try:
            self.dynamo_aux.update_item(
                user=self.user,
                datetime=self.datetime_aux,
                status=DYNAMO_STATUS_END_PROCESS
            )
        except Exception as e:
            print(f'Error ending process: {e}')
            raise

    def __error_process(self):
        try:
            self.dynamo_aux.update_item(
                user=self.user,
                datetime=self.datetime_aux,
                status=DYNAMO_STATUS_ERROR
            )
        except Exception:
            raise

    @staticmethod
    def delete_folder():
        try:
            delete_folder(
                [
                    OUTPUT_FRAMES_DIR_NAME,
                    OUTPUT_ZIP_DIR_NAME,
                    OUTPUT_DOWNLOAD_DIR_NAME
                ]
            )
        except Exception as e:
            print(f'Error deleting folders: {e}')
            raise

    def run(self):
        try:
            # Criacao do item no dynamo
            self.__start_process()

            # Baixar o Video do S3
            self.__download_video()

            # Extrair os frames
            self.__extract_frames()

            # Zipar os frames
            self.__zip_frames()

            # Upload do zip para o S3
            self.__upload_zip()

            # Atualizar o status do dynamo
            self.__end_process()

            # Deletar as pastas temporarias
            self.delete_folder()
        except  Exception as e:
            print(f'Error running saga control: {e}')

            self.__error_process()

            # Deletar as pastas temporarias
            self.delete_folder()

            raise
