import os
import zipfile


def zip_folder(folder_path, output_dir, zip_name):
    if not os.path.exists(folder_path):
        print("Erro: A pasta que você deseja compactar não existe!")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Cria o diretório de destino, se não existir

    output_zip = os.path.join(output_dir, zip_name)

    # Se o ZIP já existir, remove para evitar problemas
    if os.path.exists(output_zip):
        os.remove(output_zip)

    try:
        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)  # Mantém a estrutura dentro do ZIP
                    zipf.write(file_path, arcname)

        print(f"Pasta '{folder_path}' compactada com sucesso e salva em '{output_zip}'!")
    except PermissionError:
        print("Erro: Permissão negada! Tente rodar o script como administrador.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

