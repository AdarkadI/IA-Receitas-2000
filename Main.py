import json
import os
from collections import Counter
from dotenv import load_dotenv
from google import genai
import re

# --- Função auxiliar para limpar JSON ---
def limpar_json(texto):
    texto = re.sub(r"^```json\s*", "", texto)
    texto = re.sub(r"^```", "", texto)
    texto = re.sub(r"```$", "", texto)
    return texto.strip()

# --- 1. Carregar API Key ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API Key não encontrada! Coloque GEMINI_API_KEY no arquivo .env")

client = genai.Client(api_key=api_key)

# --- 2. Gerar receitas automaticamente ---
def gerar_receitas_automaticas(qtd=10):
    prompt = (
        f"Crie {qtd} receitas variadas em formato JSON, cada uma com os campos: "
        "{{'nome': string, 'ingredientes': [lista de ingredientes], 'modo_preparo': string}}. "
        "As receitas devem ser simples, variadas e realistas, ideais para um cardápio semanal."
    )

    try:
        resposta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        texto = limpar_json(resposta.text)
        print("\n📜 Receitas geradas pela IA:\n", texto)
        return json.loads(texto)
    except Exception as e:
        print("Erro ao gerar receitas:", e)
        return []

# --- 3. Gerar cardápio ---
def gerar_cardapio_semana(receitas):
    prompt = (
        "Selecione 2 refeições diferentes por dia da semana "
        "com base nas receitas fornecidas. "
        "Use o formato JSON: {\"Segunda\": [\"Almoço\", \"Jantar\"], ...} "
        "Escolha apenas nomes das receitas fornecidas."
    )
    receitas_nomes = [r["nome"] for r in receitas]

    try:
        resposta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{prompt}\nReceitas disponíveis: {receitas_nomes}"
        )
        texto = limpar_json(resposta.text)
        print("\n🔮 Resposta da IA (Cardápio):\n", texto)
        return json.loads(texto)
    except Exception as e:
        print("Erro ao gerar cardápio:", e)
        return {}

# --- 4. Gerar lista de compras ---
def gerar_lista_compras(cardapio, receitas):
    todos_ingredientes = []
    for dia, refeicoes in cardapio.items():
        for refeicao in refeicoes:
            for r in receitas:
                if r["nome"] == refeicao:
                    todos_ingredientes.extend(r["ingredientes"])
                    break
    contador = Counter(todos_ingredientes)
    return dict(contador)

# --- 5. Salvar receitas diárias em TXT ---
def salvar_receitas_txt(cardapio, receitas):
    os.makedirs("cardapio_semana", exist_ok=True)

    for dia, refeicoes in cardapio.items():
        nome_arquivo = f"cardapio_semana/{dia.lower()}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(f"📅 {dia}\n")
            f.write("=" * 40 + "\n\n")

            for nome_refeicao in refeicoes:
                for r in receitas:
                    if r["nome"] == nome_refeicao:
                        f.write(f"🍽️ {r['nome']}\n")
                        f.write("Ingredientes:\n")
                        for ing in r["ingredientes"]:
                            f.write(f" - {ing}\n")
                        f.write("\nModo de preparo:\n")
                        f.write(f"{r['modo_preparo']}\n")
                        f.write("\n" + "-" * 40 + "\n\n")
                        break
        print(f"✅ Arquivo salvo: {nome_arquivo}")

# --- 6. Salvar lista de compras em TXT ---
def salvar_lista_compras_txt(lista):
    os.makedirs("cardapio_semana", exist_ok=True)
    caminho = "cardapio_semana/lista_compras_semana.txt"
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("🛒 LISTA DE COMPRAS DA SEMANA\n")
        f.write("=" * 40 + "\n\n")
        for item, qtd in lista.items():
            f.write(f"- {item}: {qtd}\n")
    print(f"🛍️ Lista de compras salva em: {caminho}")

# --- 7. Executar ---
if __name__ == "__main__":
    print("🧠 Gerando receitas automaticamente com o Gemini...")
    receitas = gerar_receitas_automaticas(10)

    if not receitas:
        print("❌ Não foi possível gerar as receitas.")
        exit()

    cardapio = gerar_cardapio_semana(receitas)
    if not cardapio:
        print("❌ Não foi possível gerar o cardápio.")
        exit()

    print("\n🍽️ CARDÁPIO SEMANAL:")
    for dia, refeicoes in cardapio.items():
        print(f"\n{dia}:")
        print(f"  Almoço: {refeicoes[0]}")
        print(f"  Jantar: {refeicoes[1]}")

    salvar_receitas_txt(cardapio, receitas)

    lista = gerar_lista_compras(cardapio, receitas)
    salvar_lista_compras_txt(lista)

    print("\n🎉 Todos os arquivos .txt foram gerados com sucesso!")
