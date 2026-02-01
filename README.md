# AI Vision Comparison

Aplicação web desenvolvida com Streamlit que compara as respostas dos modelos de IA **Google Gemini** e **OpenAI GPT-4o** na análise de imagens.

## Sobre o Projeto

Esta aplicação permite fazer upload de imagens e enviar perguntas ou instruções sobre elas, recebendo simultaneamente as respostas de ambos os modelos de IA. Todas as interações são salvas automaticamente em um histórico local para referência futura.

### Funcionalidades

- Upload de imagens em múltiplos formatos (PNG, JPEG, WEBP, HEIC, HEIF)
- Comparação paralela entre Gemini 3 Flash Preview e GPT-4o
- Processamento simultâneo com ThreadPoolExecutor para respostas mais rápidas
- Histórico de interações salvo automaticamente
- Interface amigável e responsiva

## Requisitos

- Python 3.8 ou superior
- Chaves de API do Google Gemini e OpenAI

## Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd curso-extensao-1-1
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv

# No Windows
venv\Scripts\activate

# No macOS/Linux
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as API Keys

Copie o arquivo de exemplo e configure suas chaves:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione suas chaves de API:

```env
# Gemini API Key
# Obtenha em: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=sua_chave_gemini_aqui

# OpenAI API Key
# Obtenha em: https://platform.openai.com/api-keys
OPENAI_API_KEY=sua_chave_openai_aqui
```

#### Como obter as API Keys:

- **Gemini**: Acesse [Google AI Studio](https://aistudio.google.com/app/apikey)
- **OpenAI**: Acesse [OpenAI Platform](https://platform.openai.com/api-keys)

## Como Usar

### 1. Execute a aplicação

```bash
streamlit run app.py
```

### 2. Acesse no navegador

A aplicação abrirá automaticamente no navegador, ou acesse manualmente:
```
http://localhost:8501
```

### 3. Use a aplicação

1. Faça upload de uma imagem
2. Digite sua pergunta ou instrução sobre a imagem
3. Clique em "Comparar Respostas"
4. Veja as respostas lado a lado do Gemini e OpenAI
5. Consulte o histórico de interações quando necessário

## Estrutura do Projeto

```
hackaton-aula1/
├── app.py                          # Aplicação principal
├── requirements.txt                # Dependências Python
├── .env.example                    # Exemplo de configuração
├── .env                           # Suas configurações (não versionado)
├── historico_interacoes.txt       # Histórico salvo automaticamente
└── README.md                      # Esta documentação
```

## Tecnologias Utilizadas

- **Streamlit** - Framework para interface web
- **Google GenAI** - SDK do Google Gemini
- **OpenAI** - SDK da OpenAI
- **Pillow** - Processamento de imagens
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## Modelos de IA

- **Gemini**: gemini-3-flash-preview
- **OpenAI**: gpt-4o

## Histórico de Interações

Todas as interações são automaticamente salvas em `historico_interacoes.txt` com:
- Data e hora
- Nome da imagem
- Pergunta feita
- Resposta do Gemini
- Resposta do OpenAI

## Notas

- As respostas são processadas em paralelo para maior velocidade
- O histórico é salvo localmente e pode crescer com o tempo
- Certifique-se de que suas API Keys estão ativas e com créditos disponíveis

## Licença

Este projeto foi desenvolvido para fins educacionais.
