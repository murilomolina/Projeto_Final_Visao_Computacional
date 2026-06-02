# Configuração do Ambiente

## Instalação da biblioteca `face_recognition`

Requer algumas dependências específicas. O procedimento completo está documentado no repositório do professor Gabriel Lima:

https://github.com/GabrielLima1995/FaceRecognitionOnJetsonNano

Siga as instruções descritas no README do repositório para concluir a instalação da biblioteca e de suas dependências.

---

## Inicialização do Ambiente Virtual

Após a instalação do `face_recognition`, crie e ative um ambiente virtual Python para isolar as dependências do projeto.

### Criar o ambiente virtual

```bash
python -m venv .venv
```


### Ativar o ambiente virtual

#### Linux/macOS
```bash
source .venv/bin/activate
```

#### Windows (PowerShell)

```bash
.venv\Scripts\Activate.ps1
```

## Instalação das Dependências do Projeto

Com o ambiente virtual ativo, instale as dependências listadas no arquivo requirements.txt:

```bash
pip install -r requirements.txt
```


# 1. Script de Registro de Faces (face_register_murilo.py)
Este script é responsável por carregar imagens de uma pasta chamada ./gallery, extrair as características faciais de cada indivíduo e salvá-las no arquivo de banco de dados .dat. 
## Instruções antes de rodar:
### Crie uma pasta chamada `gallery` no mesmo diretório do script. 
### Adicione fotos dos integrantes do grupo dentro da pasta gallery. O nome do arquivo será o nome registrado (Ex: murilo.jpg, Maria.png).

# 2. Script da Campainha Inteligente (doorbell_murilo.py)
Este script abre a câmera conectada à Jetson Nano, aquece o modelo , processa o vídeo em tempo real e verifica se as pessoas são conhecidas usando um limiar de 0.5 para maior precisão. 

A lógica de contagem de visitas (a cada 2 minutos) foi incorporada na função de lookup.

