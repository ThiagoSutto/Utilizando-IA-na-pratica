import os
import pandas as pd
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
cliente_ia = OpenAI()

# ====================================================================
# TODO 1: LEITURA DO "PDF" (Lendo o texto sujo)
# ====================================================================
# Leia o arquivo 'fatura_suja_01.txt' e guarde todo o conteúdo 
# em uma variável chamada 'texto_bruto'.

caminho_arquivo = r'C:\Users\25.00638-8\Documents\Ianapratica\ia-na-pratica\Utilizando-IA-na-pratica\ia-na-pratica\dev\exemplos\nota-fiscal-notebook-dell.pdf'

leitor_pdf = PdfReader(caminho_arquivo)
texto_bruto = ""

# texto_bruto = ...
for pagina in leitor_pdf.pages:
    texto_bruto += pagina.extract_text()

# ====================================================================
# TODO 2: EXTRAÇÃO INTELIGENTE COM IA (Structured Output)
# ====================================================================
# Use a API da OpenAI para analisar o 'texto_bruto'.
prompt_sistema = """Você é um extrator de dados de faturas.
Retorne EXATAMENTE um objeto JSON com as seguintes chaves:
- "nome_empresa": Nome da empresa emissora.
- "data_vencimento": Data de vencimento no formato DD/MM/AAAA.
- "valor": Somente números e ponto decimal (ex: 1500.50).
Não retorne nenhum outro texto além do JSON."""

resposta = cliente_ia.chat.completions.create(
         model="gpt-4o-mini", 
         temperature=0.1,
         messages=[
             {"role": "system", "content": prompt_sistema},
             {"role": "user", "content": texto_bruto}
         ]
     )
    
print(f"Resposta da IA: {resposta.choices[0].message.content}\n")
# "nome_empresa", "data_vencimento", "valor" (só os números).


# ====================================================================
# TODO 3: CONSOLIDANDO NO PANDAS
# ====================================================================
# 1. Pegue a resposta em JSON gerada pela IA (que é uma string).
# 2. Converta ela em um dicionário Python (use a biblioteca 'json').
# 3. Transforme esse dicionário em uma linha de um DataFrame do Pandas.

import json
json_extraido = json.loads(resposta)
df_resultado = pd.DataFrame([json_extraido])
print("\n📊 Dado Extraído e Estruturado:")
print(df_resultado)