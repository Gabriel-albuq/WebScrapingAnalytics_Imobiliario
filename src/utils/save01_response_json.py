import os
import json

def save_response_to_json(data, save_path, layer, title, datetime_now):
    """
    Salva dados em formato JSON no caminho especificado com o título dado.

    :param data: str - O DataFrame a ser salvo.
    :param save_path: str - O caminho do diretório onde o arquivo será salvo.
    :param layer: str - Camada do arquivo.
    :param title: str - O título (nome) do arquivo JSON.
    :param datatime_now: str - Data e hora de extração
    """
    path_bronze = os.path.join(save_path, title, layer, datetime_now)
    os.makedirs(path_bronze, exist_ok=True)
    file_path = os.path.join(path_bronze, f"{title}.json")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Arquivo JSON salvo com sucesso em: {file_path}")