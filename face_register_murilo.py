import face_recognition
import cv2 
import os
import pickle
from datetime import datetime, timedelta
import numpy as np 

known_face_encodings = []
known_face_metadata = []

def load_known_faces():
    '''função que carrega as faces conhecidas contidas no arquivo .dat'''
    global known_face_encodings, known_face_metadata
    try:
        with open("known_faces.dat", "rb") as f:
            known_face_encodings, known_face_metadata = pickle.load(f)
        print("Base de faces carregada com sucesso.")
    except FileNotFoundError:
        print("ERRO, criando nova base será criada.")
        known_face_encodings = []
        known_face_metadata = []

def save_known_faces():
    '''função que salva as faces conhecidas em um arquivo .dat'''
    with open("known_faces.dat", "wb") as f:
        pickle.dump((known_face_encodings, known_face_metadata), f)
    print("Faces salvas em known_faces.dat")

def register_new_face(face_encoding, face_image, name): # nao usei a variável face_image porque o modelo precisa apenas do vetor numérico (face_encoding) para realizar o reconhecimento. Salvar as imagens inteiras deixaria o arquivo .dat muito pesado, acho que ia pesar na Jetson.
    '''função registrar novas faces'''
    known_face_encodings.append(face_encoding)
    # data antiga pra que a primeira visita real seja imediatamente contabilizada
    known_face_metadata.append({
        "name": name,
        "seen_count": 0,
        "last_seen": datetime(2000, 1, 1) 
    })
    print(f"Rosto de {name} cadastrado com sucesso.")

def add_faces_from_gallery(gallery_path):
    '''função que adiciona as faces contidas em imagens (salvas em uma pasta) no arquivo .dat '''
    load_known_faces()
    
    if not os.path.exists(gallery_path):
        print(f"A pasta {gallery_path} não existe. Por favor, crie-a e adicione fotos.")
        return

    for file_name in os.listdir(gallery_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            name = os.path.splitext(file_name)[0]
            img_path = os.path.join(gallery_path, file_name)

            print(f"Processando imagem: {file_name}...")
            image = face_recognition.load_image_file(img_path)
            face_encodings = face_recognition.face_encodings(image)

            if len(face_encodings) > 0:
                # Caso haja varios rostos, pega o primeiro da imagem
                register_new_face(face_encodings[0], image, name)
            else:
                print(f"AVISO: Nenhum rosto encontrado em {file_name}")

    save_known_faces()

if __name__ == "__main__":
    gallery_path = "./gallery"
    # Cria o diretório se não tiver
    if not os.path.exists(gallery_path):
        os.makedirs(gallery_path)
        print(f"Diretório '{gallery_path}' criado. Insira as fotos e rode novamente.")
    else:
        add_faces_from_gallery(gallery_path)