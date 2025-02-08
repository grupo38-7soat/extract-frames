import os
import imageio
import threading

MAX_NUMER_OF_THREADS = 10
OUTPUT_DIR_NAME = 'temp_output_frames'

class ExtractFrames(object):
    def __init__(self, start_time=0, end_time=None, frame_skip=1):
        self.output_dir = OUTPUT_DIR_NAME
        self.start_time = start_time
        self.end_time = end_time
        self.frame_skip = frame_skip

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
    def __file_name(index):
        return f"frame_{index}.png"

    def __executor(self, video_path, output_dir, start_frame, end_frame, frame_skip=1, thread_id=0):
        try:
            reader = imageio.get_reader(video_path, 'ffmpeg')
            os.makedirs(output_dir, exist_ok=True)

            print(f"[Thread {thread_id}]: Processando frames de {start_frame} a {end_frame}")

            for index, frame in enumerate(reader):
                if index < start_frame:
                    continue
                if index >= end_frame:
                    break
                if (index - start_frame) % frame_skip == 0:
                    output_path = os.path.join(output_dir, f"{self.__file_name(index)}")
                    imageio.imwrite(output_path, frame)

            print(f"[Thread {thread_id}] Concluído!")
        except Exception as e:
            print(f"Erro ao processar frames: {e}")

    def __extract_frames(self, video_path, start_frame, end_frame, frames_per_thread):
        threads = []
        for thread_id in range(MAX_NUMER_OF_THREADS):
            thread_start_frame = start_frame + thread_id * frames_per_thread * self.frame_skip
            thread_end_frame = thread_start_frame + frames_per_thread * self.frame_skip
            if thread_id == MAX_NUMER_OF_THREADS - 1:
                thread_end_frame = end_frame

            thread = threading.Thread(
                target=self.__executor,
                args=(video_path, self.output_dir, thread_start_frame, thread_end_frame, self.frame_skip, thread_id)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def run(self, video_path):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Abrindo o vídeo
        reader = imageio.get_reader(video_path, 'ffmpeg')
        meta_data = reader.get_meta_data()
        fps = meta_data['fps']
        duration = meta_data['duration']  # Duração total do vídeo em segundos

        self.__valid_attributes(duration)

        print('Tempo total do vídeo: {} segundos'.format(duration))

        # Calculando os frames correspondentes ao intervalo
        start_frame = self.__calculate_frame(self.start_time, fps)
        end_frame = self.__calculate_frame(self.end_time, fps)

        total_frames = (end_frame - start_frame) // self.frame_skip
        print('Numero de frames no video: {}'.format(total_frames))

        frames_per_thread = total_frames // MAX_NUMER_OF_THREADS

        self.__extract_frames(video_path, start_frame, end_frame, frames_per_thread)

        print(f"Frames extraídos com sucesso para o diretório: {self.output_dir}")