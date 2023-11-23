import pandas as pd  # Importa a biblioteca pandas e a renomeia como 'pd' para facilitar o uso
import random  # Importa a biblioteca random para gerar valores aleatórios

# Define a quantidade de entradas no dataset
num_entries = 100

# Lista de valores possíveis para cada característica
num_quartos = [2, 3, 4, 5]
num_banheiros = [1, 2, 3, 4]
num_garagens = [1, 2, 3]
metros_quadrados = range(80, 300, 10)
num_encantamento = range(1, 10)
quadra_quadribol = ['S', 'N']

# Criação do DataFrame
data = {
    'NumeroQuartos': [random.choice(num_quartos) for _ in range(num_entries)],  # Gera valores aleatórios para o número de quartos
    'NumeroBanheiros': [random.choice(num_banheiros) for _ in range(num_entries)],  # Gera valores aleatórios para o número de banheiros
    'NumeroGaragens': [random.choice(num_garagens) for _ in range(num_entries)],  # Gera valores aleatórios para o número de garagens
    'MetrosQuadrados': [random.choice(metros_quadrados) for _ in range(num_entries)],  # Gera valores aleatórios para a área em metros quadrados
    'NumeroEncantamento': [random.choice(num_encantamento) for _ in range(num_entries)],  # Gera valores aleatórios para o número de encantamento
    'QuadraQuadribol': [random.choice(quadra_quadribol) for _ in range(num_entries)],  # Gera valores aleatórios para a presença ou não de quadra de quadribol
    'SugestaoAluguel': [random.randint(1000, 5000) for _ in range(num_entries)],  # Valores fictícios para SugestaoAluguel
    'SugestaoVenda': [random.randint(50000, 200000) for _ in range(num_entries)]  # Valores fictícios para SugestaoVenda
}

# Criação de um DataFrame do pandas
df = pd.DataFrame(data)

# Salva o DataFrame como um arquivo CSV com ponto e vírgula como separador
df.to_csv('imoveis_dataset.csv', index=False, sep=';')
