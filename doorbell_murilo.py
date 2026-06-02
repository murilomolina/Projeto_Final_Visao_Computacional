import face_recognition
import cv2  
from datetime import datetime, timedelta
import numpy as np 
import platform
import pickle

known_face_encodings = []
known_face_metadata = []

def warm_up_encoding():
    '''função que faz a pre inicialização dos modelos'''
    print("Aquecendo o modelo de detecção de faces. Aguarde...")
    # Cria uma imagem preta minúscula para forçar o carregamento do modelo na memória
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
    face_recognition.face_encodings(dummy_image)
    print("Modelo funfa")

def load_known_faces():
    '''função que carrega as faces conhecidas contidas no arquivo .dat'''
    global known_face_encodings, known_face_metadata
    try:
        with open("known_faces.dat", "rb") as f:
            print("passou no open do .dat")
            known_face_encodings, known_face_metadata = pickle.load(f)
        print(f"Base carregada. n° de faces conhecidas: {len(known_face_metadata)}")
    except FileNotFoundError:
        print("Erro: Arquivo known_faces.dat não encontrado. tem que rodar o register")
        exit()

def lookup_known_face(face_encoding):
    '''função que verifica se a pessoa é conhecida. USA 0.5 como limiar de comparação'''
    global known_face_metadata
    
    if len(known_face_encodings) == 0:
        return "Desconhecido", 0

    # Calcula a similaridade/distância de face
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)

    # Limiar de 0.5
    if face_distances[best_match_index] <= 0.5:
        metadata = known_face_metadata[best_match_index]
        now = datetime.now()

        # 2 min para contar nova visita
        if now - metadata["last_seen"] > timedelta(minutes=2):
            metadata["seen_count"] += 1
            print(f"Campainha tocou! Nova visita detectada: {metadata['name']}. Total de visitas: {metadata['seen_count']}")
        
        # ultima detecção
        metadata["last_seen"] = now
        
        return metadata["name"], metadata["seen_count"]
    else:
        return "Desconhecido", 0

def main_loop():
    '''função principal aqui'''
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Erro na camera")
        return

    print("Sistema de Campainha Inicializado. Pressione 'q' na janela de vídeo para sair.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Redimensionar o frame para 1/4 (pode ser que deixe a jetson mais rapida n sei)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Converte a imagem do formato BGR do OpenCV para o formato RGB suportado pelo face_recognition
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Achar todos os rostos e calcular as assinaturas faciais (encodings) no frame de vídeo
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Escalonar localizações do rosto de volta para o frame original?
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Descobre quem é
            name, count = lookup_known_face(face_encoding)

            # moldura (Verde para Conhecidos, Vermelho para Desconhecidos)
            color = (0, 255, 0) if name != "Desconhecido" else (0, 0, 255)

            # Desenhar um retângulo do rosto
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            #  label do nome (e o número de visitas se for conhecido)
            if name != "Desconhecido":
                label = f"{name} (Visitas: {count})"
            else:
                label = "Desconhecido"

            #  rótulo de fundo e o texto
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, label, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)

        # Exibe o vídeo
        cv2.imshow('Smart Doorbell - Jetson Nano', frame)

        # Parar com'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Salvar os dados, contagem atual das visitas de volta no arquivo
            with open("known_faces.dat", "wb") as f:
                pickle.dump((known_face_encodings, known_face_metadata), f)
            print("Dados salvos e sistema encerrado.")
            break

    # fecha a camera
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    warm_up_encoding()
    load_known_faces()
    main_loop()