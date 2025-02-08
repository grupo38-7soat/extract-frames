from time import time

from services.saga_control import SagaControl

def lambda_handler(event, context):
    try:
        print('Iniciando processo')
        print(f'Msg de entrada: {event}')
        start_time = time()
        SagaControl(event).run()
        print(f"Tempo total de execução: {time() - start_time} segundos")
    except Exception as e:
        print(f"Erro ao executar o processo: {e}")
        raise

# Exemplo de uso
if __name__ == "__main__":
    payload = {
        "user": "123",
        "video_name": "Tempos Modernos  Charlie Chaplin, Dublado.mp4",
        "start_time_for_cut_frames": 0,
        "end_time_for_cut_frames": None,
        "skip_frame": 1
    }
    lambda_handler(payload, None)

