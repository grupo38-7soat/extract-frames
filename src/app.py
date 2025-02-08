import json
from time import time
from services.saga_control import SagaControl


def lambda_handler(event, context):
    try:
        print('Iniciando processo')
        print(f'Msg de entrada: {event}')
        start_time = time()
        for record in event['Records']:
            body = json.loads(record['body'])
            print(f'Processando mensagem: {body}')
            SagaControl(body).run()

        print(f"Tempo total de execução: {time() - start_time} segundos")
    except Exception as e:
        print(f"Erro ao executar o processo: {e}")
        raise

# Exemplo de uso
# if __name__ == "__main__":
#     # {
#     #     "user": "123",
#     #     "video_name": "SampleVideo_1280x720_1mb.mp4",
#     #     "start_time_for_cut_frames": 0,
#     #     "end_time_for_cut_frames": 0,
#     #     "skip_frame": 1
#     # }
#
#     payload= {'Records': [{'messageId': 'ceeeb811-a50d-43eb-a0ad-595e6467afb6',
#                   'receiptHandle': 'AQEBJTfWu49dGfKhhK1aR7ca854Sb20F/Y7k0VKTB6G4Gdtgm7e2kTgyXSTfKavvVJmybYjTjE2Qn+1LdnAfHr5QCFNq5pHxvPNmC4gnvginWR/tkgGGo3O+qQaGYHnPrYoyhhFIIFkxRelIJ75clPrZkWV4g2xADRYLwESfwNPTrMjaKoY+E0zVGpl0G5cbNf14m3u6B61mDxgR9VSDClPz9b7wA9TnD9IBnGxJlJs71g0iJ1SWbWpQ+r22dpyZTMhWYeicP4yqUsM8xPUkExi4YQadZNmmwFj3xTutBjrj7yRH2cXyUX4AqdPPV+5gt2TTGuAlJpyziTa0sCUi2vZe97+0Piv8wo1HGBAg34rG0OzCY7hdIGk5/8m6xsortmqujn6ujTPWkbOtwd5JFCm3bw==',
#                   'body':
#                       ''
#                       '{\n        "user": "novo_user_1",\n        "video_name": "SampleVideo_1280x720_1mb.mp4",\n        "start_time_for_cut_frames": 0,\n        "end_time_for_cut_frames": 0,\n        "skip_frame": 1\n    }'
#                       '',
#                   'attributes': {'ApproximateReceiveCount': '1', 'SentTimestamp': '1739057437791',
#                                  'SenderId': '940482415113', 'ApproximateFirstReceiveTimestamp': '1739057437802'},
#                   'messageAttributes': {}, 'md5OfBody': 'e721e55644c6e771070575775182d80a', 'eventSource': 'aws:sqs',
#                   'eventSourceARN': 'arn:aws:sqs:us-east-1:940482415113:extract-frames-queue',
#                   'awsRegion': 'us-east-1'}]}
#     lambda_handler(payload, None)
