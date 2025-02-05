import os
from time import time
import imageio
from functools import partial
from utils.query_result_thread import QueryResultThread

MAX_NUMER_OF_THREADS = 10

class ExtractFrames(object):
    def __init__(self, start_time=0, end_time=None, frame_skip=1):

        self.start_time = start_time
        self.end_time = end_time
        self.frame_skip=frame_skip

    @staticmethod
    def __calculate_frame(value, fps):
        return int(value * fps)

    def __valid_attributes(self, duration):
        if self.frame_skip < 1:
            raise ValueError("O valor de frame_skip deve ser maior ou igual a 1.")

        # Validando os parâmetros de tempo
        if self.end_time is None or self.end_time > duration:
            self.end_time = duration

        if self.start_time >= self.end_time:
            raise ValueError("O tempo inicial deve ser menor que o tempo final.")

    @staticmethod
    def __list_comprehension(reader):
        frames = [(index, frame) for index, frame in enumerate(reader)]
        group_size = max(1, len(frames) // MAX_NUMER_OF_THREADS + (1 if len(frames) % MAX_NUMER_OF_THREADS != 0 else 0))
        grouped_frames = [frames[i:i + group_size] for i in range(0, len(frames), group_size)]
        return grouped_frames

    def __file_name(self, index):
        return f"frame_{index}.png"

    def __executor(self, group, start_frame, end_frame):
        try:
            for index, frame in group:
                if index < start_frame:  # Ignora frames antes do intervalo
                    continue
                if index >= end_frame:  # Para quando atingir o fim do intervalo ou o máximo de frames
                    break
                if (index - start_frame) % self.frame_skip == 0:  # Pula frames com base em frame_skip
                    output_path = os.path.join(output_dir, self.__file_name(index))
                    imageio.imwrite(output_path, frame)
        except Exception as e:
            print(f"Erro ao processar frames: {e}")

    def __extract_frames(self, grouped_frames, start_frame, end_frame):
        threads = []
        count_theads = 1
        for group in grouped_frames:
            thread = QueryResultThread(partial(self.__executor, group, start_frame, end_frame))
            thread.start()
            threads.append(thread)
            print(f"Iniciando Thread: {count_theads}")
            count_theads += 1

        for thread in threads:
            thread.join()


    def run(self, video_path, output_dir):
        """
        Extrai frames de um vídeo com base nos parâmetros fornecidos usando imageio.

        Args:
            video_path (str): Caminho do vídeo de entrada.
            output_dir (str): Diretório para salvar os frames extraídos.
            max_frames (int): Número máximo de frames a serem extraídos (opcional).
            start_time (int): Tempo inicial em segundos para começar o recorte (default: 0).
            end_time (int): Tempo final em segundos para finalizar o recorte (opcional).
            frame_skip (int): Intervalo de frames a serem pulados (default: 1 - sem pular).

        Returns:
            None
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Abrindo o vídeo
        reader = imageio.get_reader(video_path, 'ffmpeg')
        meta_data = reader.get_meta_data()
        fps = meta_data['fps']
        duration = meta_data['duration']  # Duração total do vídeo em segundos

        self.__valid_attributes(duration)

        print('Tempo total do vídeo: {} segundos'.format(duration))
        print('Numero de frames no video: {}'.format(fps))

        # Calculando os frames correspondentes ao intervalo
        start_frame = self.__calculate_frame(self.start_time, fps)
        end_frame = self.__calculate_frame(self.end_time, fps)

        grouped_frames = self.__list_comprehension(reader)

        self.__extract_frames(grouped_frames, start_frame, end_frame)

        print(f"Frames extraídos com sucesso para o diretório: {output_dir}")


# Exemplo de uso
if __name__ == "__main__":
    start_time = time()
    # Exemplo de uso
    video_path = "D:\FIAP\pythonProject\SampleVideo.mp4"
    output_dir = "filme"
    # Exemplo de uso:

    ExtractFrames(end_time= 600,frame_skip=1).run(video_path, output_dir)

    print(f"Tempo total de execução: {time() - start_time} segundos")