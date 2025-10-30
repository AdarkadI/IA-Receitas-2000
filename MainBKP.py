"""
cardapio_por_ingredientes_sem_lista.py

Fluxo:
1) Usuário informa os ingredientes disponíveis.
2) O modelo Gemini gera um cardápio semanal (segunda a domingo)
   com almoço e jantar, utilizando preferencialmente esses ingredientes.
3) O programa salva os arquivos de saída (JSON e TXT).
"""

import os
import re
import time
import json
from dotenv import load_dotenv
from jsonschema import validate, ValidationError
from google import genai

# ===========================================================
# CONFIGURAÇÃO E SCHEMA DE VALIDAÇÃO
# ===========================================================

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY não encontrada no .env")

client = genai.Client(api_key=API_KEY)

# Estrutura esperada de cada receita
RECEITA_SCHEMA = {
    "type": "object",
    "required": ["nome", "ingredientes", "modo_preparo"],
    "properties": {
        "nome": {"type": "string"},
        "ingredientes": {"type": "array", "items": {"type": "string"}},
        "modo_preparo": {"type": "string"}
    },
    "additionalProperties": True
}

# Estrutura esperada do cardápio semanal
CARDAPIO_SCHEMA = {
    "type": "object",
    "properties": {
        "Segunda": {"type": "array"},
        "Terca": {"type": "array"},
        "Quarta": {"type": "array"},
        "Quinta": {"type": "array"},
        "Sexta": {"type": "array"},
        "Sabado": {"type": "array"},
        "Domingo": {"type": "array"}
    },
    "additionalProperties": True
}

# ===========================================================
# FUNÇÕES AUXILIARES
# ===========================================================

def limpar_json(texto: str) -> str:
    """Remove cercas de código (```json) e espaços extras da resposta da IA."""
    if not isinstance(texto, str):
        return ""
    texto = texto.strip()
    texto = re.sub(r"^```json\s*", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"^```", "", texto)
    texto = re.sub(r"```$", "", texto)
    return texto.strip()

def parse_json_seguro(texto: str):
    """Converte resposta para JSON e mostra o conteúdo em caso de falha."""
    texto = limpar_json(texto)
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        print("⚠️ JSON inválido recebido da IA:\n")
        print(texto)
        return None

def validar_receita_obj(obj: dict) -> bool:
    """Confere se o objeto segue o formato mínimo de uma receita."""
    try:
        validate(instance=obj, schema=RECEITA_SCHEMA)
        return True
    except ValidationError as e:
        print(f"Receita inválida: {e.message}")
        return False

def validar_cardapio_semana(obj: dict) -> bool:
    """Confere se o cardápio contém dias e receitas válidas."""
    try:
        validate(instance=obj, schema=CARDAPIO_SCHEMA)
    except ValidationError as e:
        print(f"Erro de schema no cardápio: {e.message}")
        return False

    for dia, refeicoes in obj.items():
        if not isinstance(refeicoes, list) or len(refeicoes) < 2:
            print(f"Dia {dia} está incompleto (faltam refeições).")
            return False
        for r in refeicoes[:2]:
            if not validar_receita_obj(r):
                print(f"Refeição inválida em {dia}: {r}")
                return False
    return True

# ===========================================================
# COMUNICAÇÃO COM A API (com retry)
# ===========================================================

def gerar_com_retry(prompt: str, max_attempts: int = 3, base_backoff: float = 1.0):
    """Faz a chamada ao modelo com tentativas automáticas em caso de falha."""
    last_exc = None
    for attempt in range(1, max_attempts + 1):
        try:
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            texto = getattr(resp, "text", None) or getattr(resp, "output", None)
            if isinstance(texto, list) and texto:
                texto = texto[0]
            if texto is None:
                texto = str(resp)
            return texto
        except Exception as e:
            last_exc = e
            wait = base_backoff * (2 ** (attempt - 1))
            print(f"Tentativa {attempt} falhou: {e}. Retentando em {wait:.1f}s...")
            time.sleep(wait)
    raise last_exc

# ===========================================================
# PROMPT BUILDER
# ===========================================================

def montar_prompt_por_ingredientes(ingredientes: list, permitir_extras: bool = False):
    """Monta o prompt em português, instruindo o modelo a criar um cardápio."""
    ingredientes_texto = ", ".join(ingredientes) if ingredientes else "nenhum"
    extras_text = (
        "Pode usar ingredientes básicos como sal, óleo, alho e cebola se necessário."
        if permitir_extras
        else "Use apenas os ingredientes listados, adaptando as receitas se necessário."
    )

    prompt = (
        "Você é um chef criativo. Usando SOMENTE os ingredientes fornecidos, crie um cardápio semanal "
        "(Segunda a Domingo) com duas refeições por dia: Almoço e Jantar.\n\n"
        "Formato de resposta obrigatório:\n"
        "{\n"
        '  "Segunda": [ {"nome": "...", "ingredientes": ["..."], "modo_preparo": "..."}, {"nome": "..."} ],\n'
        '  "Terca": [...], "Quarta": [...], ...\n'
        "}\n\n"
        "Regras:\n"
        " - Cada refeição deve ter nome, lista de ingredientes e breve modo de preparo.\n"
        " - As receitas devem ser simples, caseiras e variadas.\n"
        f" - Ingredientes disponíveis: {ingredientes_texto}.\n"
        f" - {extras_text}\n"
        " - Responda APENAS com JSON válido, sem texto adicional.\n"
    )
    return prompt

# ===========================================================
# SALVAMENTO DOS RESULTADOS
# ===========================================================

def salvar_cardapio_json(cardapio_obj, caminho="cardapio_semana/cardapio_final.json"):
    """Salva o cardápio como JSON bem formatado."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(cardapio_obj, f, indent=2, ensure_ascii=False)
    print(f"✅ Cardápio JSON salvo em: {caminho}")

def salvar_cardapio_txt(cardapio_obj):
    """Cria um arquivo .txt para cada dia com as receitas."""
    os.makedirs("cardapio_semana", exist_ok=True)
    for dia, refeicoes in cardapio_obj.items():
        nome_arquivo = f"cardapio_semana/{dia.lower()}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(f"📅 {dia}\n")
            f.write("=" * 40 + "\n\n")
            for tipo, refeicao in zip(["Almoço", "Jantar"], refeicoes[:2]):
                f.write(f"🍽️ {tipo}: {refeicao.get('nome','<sem nome>')}\n")
                f.write("Ingredientes:\n")
                for ing in refeicao.get("ingredientes", []):
                    f.write(f" - {ing}\n")
                f.write("\nModo de preparo:\n")
                f.write(f"{refeicao.get('modo_preparo','')}\n\n")
                f.write("-" * 40 + "\n\n")
        print(f"✅ Arquivo salvo: {nome_arquivo}")

# ===========================================================
# FLUXO PRINCIPAL
# ===========================================================

def main():
    print("=== Gerador de cardápio por ingredientes ===")
    entrada = input("Digite os ingredientes que você tem em casa (separe por vírgula):\n> ").strip()
    if not entrada:
        print("Nenhum ingrediente informado. Encerrando.")
        return

    ingredientes = [i.strip() for i in entrada.split(",") if i.strip()]
    extras = input("Posso usar extras básicos (sal, óleo, alho, cebola)? [s/N]: ").strip().lower().startswith("s")

    prompt = montar_prompt_por_ingredientes(ingredientes, permitir_extras=extras)

    print("\nEnviando dados à API...\n")
    texto = gerar_com_retry(prompt)

    # Salva resposta bruta da IA
    os.makedirs("cardapio_semana", exist_ok=True)
    with open("cardapio_semana/cardapio_raw.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    print("✅ Resposta bruta salva em: cardapio_semana/cardapio_raw.txt")

    # Converte para JSON
    data = parse_json_seguro(texto)
    if data is None:
        print("❌ Não foi possível converter a resposta da IA em JSON válido.")
        return

    # Normaliza nomes dos dias para português
    dias_map = {
        "monday": "Segunda", "segunda": "Segunda",
        "tuesday": "Terca", "terça": "Terca", "terca": "Terca",
        "wednesday": "Quarta", "quarta": "Quarta",
        "thursday": "Quinta", "quinta": "Quinta",
        "friday": "Sexta", "sexta": "Sexta",
        "saturday": "Sabado", "sábado": "Sabado", "sabado": "Sabado",
        "sunday": "Domingo", "domingo": "Domingo"
    }
    padronizado = {dias_map.get(k.lower(), k): v for k, v in data.items()}

    # Valida estrutura final
    if not validar_cardapio_semana(padronizado):
        print("⚠️ Cardápio com formato inesperado. Veja cardapio_raw.txt para depuração.")
        return

    # Salva os resultados
    salvar_cardapio_json(padronizado)
    salvar_cardapio_txt(padronizado)

    print("\n🎉 Cardápio gerado com sucesso! Confira a pasta 'cardapio_semana'.")

if __name__ == "__main__":
    main()
