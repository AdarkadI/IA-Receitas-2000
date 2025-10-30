GERADOR DE CARDÁPIO SEMANAL POR INGREDIENTES
===============================================================

Versão: 2.0

Linguagem: Python 3.9+ (back-end) / JavaScript (front-end React)

Modelo de IA: Gemini (via biblioteca google-genai)

---------------------------------------------------------------
DESCRIÇÃO DO PROJETO
---------------------------------------------------------------

Este projeto é um sistema completo que gera automaticamente um
CARDÁPIO SEMANAL (segunda a domingo) com almoço e jantar, usando
a API Gemini e uma interface web simples em React.

O usuário informa os ingredientes disponíveis em casa e o sistema
cria receitas variadas, realistas e caseiras, priorizando o uso
dos ingredientes informados.

O back-end em Python se comunica com o modelo Gemini, processa a
resposta e retorna o cardápio em formato JSON para o front-end.

---------------------------------------------------------------
FUNCIONALIDADES
---------------------------------------------------------------

- Interface web para entrada de ingredientes.
- Opção para permitir o uso de ingredientes extras básicos
  (sal, óleo, alho, cebola).
- Geração automática de cardápio semanal (almoço e jantar).
- Resposta estruturada em formato JSON.
- Validação de estrutura (JSON Schema) para garantir formato
  consistente das respostas da IA.
- Comunicação entre front-end (React) e back-end (Flask) via API REST.
- Tentativas automáticas de reconexão à API Gemini em caso de falhas.

---------------------------------------------------------------
CONFIGURAÇÃO DA API GEMINI
---------------------------------------------------------------

1. Crie um arquivo .env dentro da pasta backend com o conteúdo:

   GEMINI_API_KEY=SEU_TOKEN_AQUI

2. Certifique-se de ter uma chave de API válida para o modelo Gemini.

---------------------------------------------------------------
INSTALAÇÃO DO BACK-END (Flask)
---------------------------------------------------------------

1. Acesse a pasta "backend":
       cd backend

2. Crie um ambiente virtual e instale as dependências:

   Windows:
       python -m venv .venv
       .venv\Scripts\activate
       pip install --upgrade pip
       pip install flask flask-cors google-genai python-dotenv jsonschema

   Linux/Mac:
       python3 -m venv .venv
       source .venv/bin/activate
       pip install --upgrade pip
       pip install flask flask-cors google-genai python-dotenv jsonschema

3. Inicie o servidor:
       python app.py

O servidor rodará em http://localhost:5000

---------------------------------------------------------------
INSTALAÇÃO DO FRONT-END (React)
---------------------------------------------------------------

1. Acesse a pasta "frontend":
       cd frontend

2. Instale as dependências:
       npm install
       npm install axios

3. Inicie o servidor de desenvolvimento:
       npm run dev

O front-end abrirá em http://localhost:5173 (ou porta similar).

---------------------------------------------------------------
COMO USAR
---------------------------------------------------------------

1. Abra o front-end no navegador (ex: http://localhost:5173).
2. Digite os ingredientes disponíveis, separados por vírgula.
   Exemplo:
       arroz, frango, batata, feijão
3. Marque a opção "Permitir extras básicos" se desejar.
4. Clique em "Gerar cardápio".
5. Aguarde alguns segundos enquanto o modelo Gemini cria o cardápio.
6. O resultado (almoço e jantar de cada dia) aparecerá na tela.

---------------------------------------------------------------
FORMATO DA REQUISIÇÃO E RESPOSTA
---------------------------------------------------------------

POST /gerar-cardapio
Content-Type: application/json

Corpo:
{
    "ingredientes": "arroz, frango, batata",
    "permitir_extras": true
}

Resposta:
{
    "Segunda": [
        {
            "nome": "Frango assado com batata",
            "ingredientes": ["frango", "batata", "sal"],
            "modo_preparo": "Asse o frango com as batatas até dourar."
        },
        {
            "nome": "Arroz com legumes",
            "ingredientes": ["arroz", "cenoura", "óleo"],
            "modo_preparo": "Refogue e cozinhe normalmente."
        }
    ],
    ...
}

---------------------------------------------------------------
DETALHES TÉCNICOS
---------------------------------------------------------------

- O back-end usa Flask e Flask-CORS para aceitar conexões do front-end.
- A função gerar_com_retry() faz tentativas automáticas com tempo de
  espera crescente entre falhas (backoff exponencial).
- O schema de validação garante que o modelo Gemini responda sempre
  com os campos obrigatórios: nome, ingredientes, modo_preparo.
- O cardápio é salvo em JSON dentro de /backend/cardapio_semana/.

---------------------------------------------------------------
DICAS DE USO
---------------------------------------------------------------

- Quanto mais específicos forem os ingredientes, melhor o resultado.
- Se o modelo gerar texto não estruturado, verifique o arquivo
  "cardapio_semana/cardapio_raw.txt" para depurar.
- É possível ajustar o modelo usado (ex: gemini-2.0-pro) no código
  do back-end se desejar respostas mais criativas.
