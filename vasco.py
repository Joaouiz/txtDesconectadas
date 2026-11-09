import requests
import json
import pandas as pd
import os

TOKEN_AILOS = "e48beb4f1a6257d8c9615dac47ced5ecd18bf53d"
TOKEN_TOYOTA = "0c7ac3691cdfb63766bd642ac4dd01796e4d105d"
url_ailos = "https://eggeremesquita.digisac.app//api/v1/services?query=%7B%22where%22%3A%7B%22archivedAt%22%3A%7B%22%24eq%22%3Anull%7D%7D%2C%22order%22%3A%5B%5B%22name%22%2C%22asc%22%5D%5D%2C%22page%22%3A1%2C%22perPage%22%3A200%7D"
url_toyota = "https://eem.digisac.co//api/v1/services?query=%7B%22where%22%3A%7B%22archivedAt%22%3A%7B%22%24eq%22%3Anull%7D%7D%2C%22order%22%3A%5B%5B%22name%22%2C%22asc%22%5D%5D%2C%22page%22%3A1%2C%22perPage%22%3A200%7D"
caminho_excel = r"U:\Planilhas\ESTOQUE.xlsx"
caminho_txt_ailos = r"U:\Planilhas\desconectadasAilos.txt" #caminho que sera gerado o txt com as desconexoes
caminho_txt_toy = r"U:\Planilhas\desconectadasToyota.txt"

def puxar_telefones(token, url):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    dados = response.json()
    #print(json.dumps(dados, indent=4))
    #PRINTA O JSON

    numeros_desconectados = []
    for conexao in dados["data"]:
        if conexao["type"] == "whatsapp":
            status = conexao["data"]["status"].get("isConnected", False)
            if not status:
                phone = conexao["data"]["myId"]
                phone = phone.replace("@c.us", "")

                numeros_desconectados.append(phone)

    return numeros_desconectados

def main(empresa):
    planilha_estoque = pd.read_excel(caminho_excel, sheet_name="Estoque")
    print(planilha_estoque.head())
    #print(planilha_estoque.columns.to_list)

    nomes_planilha = planilha_estoque["Unnamed: 0"].astype(str).tolist()
    numeros_planilha = planilha_estoque["Unnamed: 1"].astype(str).tolist()
    telefones_planilha = planilha_estoque[" "].astype(str).tolist()

    if empresa == "AILOS":
        TOKEN = TOKEN_AILOS
        url = url_ailos
        caminho_txt = caminho_txt_ailos
    elif empresa == "TOYOTA":
        TOKEN = TOKEN_TOYOTA
        url = url_toyota
        caminho_txt = caminho_txt_toy

    abacate = puxar_telefones(TOKEN, url)

    desconectados = []
    desconectados_nomes = []
    for i in range(len(telefones_planilha)):
        if numeros_planilha[i] in abacate:
            desconectados.append(str(telefones_planilha[i]))
            desconectados_nomes.append(str(nomes_planilha[i]))

    if os.path.exists(caminho_txt):
        os.remove(caminho_txt)
    for i in range(len(desconectados)):
        with open(caminho_txt, "a") as arquivo:
            arquivo.write(desconectados_nomes[i] + " - " + desconectados[i] + "\n")

if __name__ == '__main__':
    main("AILOS")
    main("TOYOTA")