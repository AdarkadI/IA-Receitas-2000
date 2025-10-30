
GERADOR DE CARDÁPIO SEMANAL POR INGREDIENTES
===============================================================

Autor: [Seu Nome]
Versão: 1.0
Linguagem: Python 3.9+
Modelo de IA: Gemini (via biblioteca google-genai)

---------------------------------------------------------------
DESCRIÇÃO DO PROJETO
---------------------------------------------------------------

Este programa utiliza a API Gemini para gerar automaticamente um
cardápio semanal (de segunda a domingo) com almoço e jantar,
baseando-se nos ingredientes que o usuário tem em casa.

A ideia é simples: você informa os ingredientes disponíveis e a
inteligência artificial cria receitas realistas, caseiras e
variadas, priorizando o uso desses itens.

Os resultados são salvos em formato JSON e também em arquivos TXT,
um para cada dia da semana, dentro da pasta "cardapio_semana".

---------------------------------------------------------------
FUNCIONALIDADES
---------------------------------------------------------------

- Entrada interativa dos ingredientes (exemplo: "arroz, frango, batata").
- Opção para permitir o uso de ingredientes extras básicos
  (sal, óleo, alho, cebola).
- Geração de cardápio semanal completo (almoço e jantar).
- Salvamento automático dos resultados em:
      cardapio_semana/cardapio_final.json
      cardapio_semana/<dia>.txt
- Validação de formato JSON para garantir consistência.
- Repetição automática de tentativas na comunicação com a API
  (com tempo de espera crescente entre as tentativas).

---------------------------------------------------------------
EXEMPLO DE EXECUÇÃO
---------------------------------------------------------------

> python cardapio_por_ingredientes_sem_lista.py

Saída esperada:

=== Gerador de cardápio por ingredientes ===
Digite os ingredientes que você tem em casa (separe por vírgula):
> arroz, feijão, frango, batata, cenoura

Posso usar extras básicos (sal, óleo, alho, cebola)? [s/N]:
> s

Enviando dados à API...

✅ Resposta bruta salva em: cardapio_semana/cardapio_raw.txt

✅ Cardápio JSON salvo em: cardapio_semana/cardapio_final.json

✅ Arquivo salvo: cardapio_semana/segunda.txt

✅ Arquivo salvo: cardapio_semana/terca.txt

...

🎉 Cardápio gerado com sucesso! Confira a pasta 'cardapio_semana'.

---------------------------------------------------------------
CONFIGURAÇÃO DA API
---------------------------------------------------------------

1. Crie um arquivo .env na raiz do projeto com o conteúdo:

   GEMINI_API_KEY=SEU_TOKEN_AQUI

2. Certifique-se de possuir uma chave de API Gemini válida.

---------------------------------------------------------------
INSTALAÇÃO DE DEPENDÊNCIAS
---------------------------------------------------------------

Crie um ambiente virtual e instale os pacotes necessários:

Windows:
    python -m venv .venv
    .venv\Scripts\activate
    pip install --upgrade pip
    pip install google-genai python-dotenv jsonschema

Linux/Mac:
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install google-genai python-dotenv jsonschema

---------------------------------------------------------------
DETALHES TÉCNICOS
---------------------------------------------------------------

- O script valida a estrutura das respostas da IA com a biblioteca
  "jsonschema" para garantir o formato correto.

- A função gerar_com_retry() realiza múltiplas tentativas com
  tempo de espera progressivo, para evitar falhas de rede temporárias.

- A resposta bruta da IA é salva antes da conversão em JSON,
  no arquivo cardapio_semana/cardapio_raw.txt, para facilitar depuração.

===============================================================
