# Importação de bibliotecas:
# A biblioteca 'requests' é utilizada para realizar requisições HTTP.
# A biblioteca 'json' é utilizada para manipular dados no formato JSON.
import requests
import json

# ========================================
# Demonstração dos principais tipos de variáveis em Python
# ========================================

# Numéricos: inteiro e float
num_int = 42              # Exemplo de número inteiro
num_float = 3.1415        # Exemplo de número com ponto flutuante (float)
print("Integer:", num_int, "| Tipo:", type(num_int))
print("Float:", num_float, "| Tipo:", type(num_float))

# String: sequência de caracteres
texto = "Hello, Python!"
print("String:", texto, "| Tipo:", type(texto))

# Booleanos: valores True ou False
verdadeiro = True
falso = False
print("Boolean True:", verdadeiro, "| Tipo:", type(verdadeiro))
print("Boolean False:", falso, "| Tipo:", type(falso))

# Listas: coleção ordenada e mutável de elementos
lista = [1, 2, 3, "quatro", 5.0]
print("List:", lista, "| Tipo:", type(lista))

# Tuplas: coleção ordenada e imutável
tupla = (1, 2, 3)
print("Tuple:", tupla, "| Tipo:", type(tupla))

# Dicionários: coleção de pares chave-valor
dicionario = {"nome": "efrem", "idade": 30}
print("Dictionary:", dicionario, "| Tipo:", type(dicionario))

# Sets: coleção de elementos únicos (não ordenada)
conjunto = {1, 2, 3, 2, 1}
print("Set:", conjunto, "| Tipo:", type(conjunto))

# ========================================
# Operações e conversão de tipos
# ========================================

# Exemplo de concatenação de string com número (necessário converter o número para string)
soma = num_int + num_float
print("Soma (num_int + num_float):", soma, "| Tipo:", type(soma))

# ========================================
# Estrutura condicional (if, elif, else)
# ========================================

# Verifica se a variável 'texto' possui um valor específico e concatena com uma mensagem.
if texto == "Olá, Python!":
    resultado = texto + " é incrível!"
elif texto == "Olá":
    resultado = texto + ", mundo!"
else:
    resultado = texto + " - valor não esperado."
print("Resultado condicional:", resultado)

# ========================================
# Estruturas de repetição (loops)
# ========================================

# Loop sobre uma lista: itera e imprime cada elemento da lista 'lista'
print("Iterando sobre a lista:")
for item in lista:
    print("Item:", item)

# Loop utilizando 'range': gera uma sequência de números e imprime cada um dividido por 10
print("Iterando com range:")
for i in range(10, 100, 6):  # Inicia em 10, vai até 100, incrementando de 6 em 6
    print("Valor:", i / 10)

# ========================================
# Consumo de API Externa: Google Maps Places API
# ========================================

# Monta a URL da API e define os parâmetros para a requisição.
# NOTA: Substitua '[API-KEY]' pela sua chave de API válida.
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
params = {
    "location": "-7.136722,-34.845641",  # Coordenadas de localização
    "radius": 20000,                     # Raio de busca (em metros)
    "types": "restaurant",               # Tipo de estabelecimento a ser buscado
    "key": "[API-KEY]"                   # Chave da API
}

# Envia a requisição GET para a API com os parâmetros especificados
response = requests.get(url, params=params)

# Converte a resposta para o formato JSON
data = response.json()

# Exibe os restaurantes encontrados (localização)
print("Restaurantes encontrados:")
for place in data.get('results', []):
    print("Local:", place.get('vicinity'))

# Exibe o JSON completo, formatado para melhor visualização
print("Dados JSON formatados:")
print(json.dumps(data, indent=4, sort_keys=True))
