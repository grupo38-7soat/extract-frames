import os
import zipfile


def zip_folder(folder_path, output_zip):
    if not os.path.exists(folder_path):
        print("Erro: Pasta não encontrada!")
        return

    if os.path.exists(output_zip):
        os.remove(output_zip)  # Remove ZIP existente para evitar erros

    try:
        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)

        print(f"Pasta '{folder_path}' compactada em '{output_zip}' com sucesso!")
    except PermissionError:
        print("Erro: Permissão negada! Tente rodar como administrador.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

