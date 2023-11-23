# Importar bibliotecas necessárias
from flask import Flask, request, jsonify, make_response  # Importa classes e funções do Flask para criar e manipular a aplicação web.
import pandas as pd  # Importa a biblioteca pandas para manipulação e análise de dados tabulares.
from sklearn.model_selection import train_test_split  # Importa a função train_test_split do scikit-learn para dividir o conjunto de dados em treino e teste.
from sklearn.ensemble import RandomForestRegressor  # Importa o modelo RandomForestRegressor do scikit-learn para regressão usando florestas aleatórias.
from sklearn.impute import SimpleImputer  # Importa a classe SimpleImputer do scikit-learn para tratar valores ausentes em dados.
import os  # Importa módulos relacionados ao sistema operacional para manipulação de caminhos de arquivos.
import numpy as np  # Importa a biblioteca numpy para operações numéricas eficientes.

# Inicializar o Flask
app = Flask(__name__)  # Cria uma instância do Flask, que será a aplicação web.

# Obtém o diretório atual do script
script_dir = os.path.dirname(__file__)  # Obtém o diretório do script em execução.

# Constrói o caminho completo para o arquivo CSV no diretório 'Cria_CSV'
csv_path = os.path.join(script_dir, '..', 'Cria_CSV', 'imoveis_dataset.csv')  # Monta o caminho para o arquivo CSV.

# Carregar o dataset fictício
df = pd.read_csv(csv_path, delimiter=';')  # Lê o CSV e armazena os dados em um DataFrame.

# Converter variáveis categóricas usando one-hot encoding
df_encoded = pd.get_dummies(df, columns=['QuadraQuadribol'])  # Aplica one-hot encoding nas colunas categóricas.

# Separar dados de treinamento e teste
X = df_encoded[['NumeroQuartos', 'NumeroBanheiros', 'NumeroGaragens', 'MetrosQuadrados', 'NumeroEncantamento', 'QuadraQuadribol_N', 'QuadraQuadribol_S']]  # Features para treinamento.
y_aluguel = df_encoded['SugestaoAluguel']  # Variável alvo para sugestão de aluguel.
y_venda = df_encoded['SugestaoVenda']  # Variável alvo para sugestão de venda.
X_train, X_test, y_aluguel_train, y_aluguel_test, y_venda_train, y_venda_test = train_test_split(X, y_aluguel, y_venda, test_size=0.2, random_state=42)  # Divide os dados em conjuntos de treinamento e teste.

# Treinar modelos
model_aluguel = RandomForestRegressor()  # Cria um modelo de regressão para sugestão de aluguel.
model_aluguel.fit(X_train, y_aluguel_train)  # Treina o modelo de aluguel.
model_venda = RandomForestRegressor()  # Cria um modelo de regressão para sugestão de venda.
model_venda.fit(X_train, y_venda_train)  # Treina o modelo de venda.

# Criar o imputer
imputer = SimpleImputer(strategy='mean')  # Cria um imputer para preencher valores ausentes com a média.

# Imputar os valores ausentes nos dados
X_imputed = imputer.fit_transform(X)  # Preenche valores ausentes no conjunto de dados.

# Definir rota para receber dados e retornar sugestões
@app.route('/sugerir_imovel', methods=['GET', 'POST'])  # Define uma rota para a API receber solicitações.
def sugerir_imovel():
    if request.method == 'GET':  # Se a solicitação for do tipo GET:
        # Verificar se há parâmetros na URL
        numero_quartos = request.args.get('NumeroQuartos')  # Obtém o parâmetro NumeroQuartos da URL.
        numero_banheiros = request.args.get('NumeroBanheiros')  # Obtém o parâmetro NumeroBanheiros da URL.
        numero_garagens = request.args.get('NumeroGaragens')  # Obtém o parâmetro NumeroGaragens da URL.
        metros_quadrados = request.args.get('MetrosQuadrados')  # Obtém o parâmetro MetrosQuadrados da URL.
        numero_encantamento = request.args.get('NumeroEncantamento')  # Obtém o parâmetro NumeroEncantamento da URL.
        quadra_quadribol = 1 if request.args.get('QuadraQuadribol') == 'S' else 0  # Converte o parâmetro QuadraQuadribol da URL para 0 ou 1.

        # Criar o array de entrada
        X = np.array([[numero_quartos, numero_banheiros, numero_garagens, metros_quadrados, numero_encantamento, 0, 1]])  # Cria um array numpy com os parâmetros.

        # Imputar os valores ausentes nos dados
        X_imputed = imputer.transform(X)  # Preenche valores ausentes nos novos dados.

        # Fazer previsões
        aluguel_sugerido = model_aluguel.predict(X_imputed)[0]  # Realiza a previsão de sugestão de aluguel.
        venda_sugerida = model_venda.predict(X_imputed)[0]  # Realiza a previsão de sugestão de venda.

        # Retornar sugestões em formato JSON
        return jsonify({'AluguelSugerido': aluguel_sugerido, 'ValorVendaSugerido': venda_sugerida})  # Retorna as sugestões em formato JSON.


    elif request.method == 'POST':  # Se a solicitação for do tipo POST:
        data = request.get_json()  # Obtém os dados do corpo da solicitação em formato JSON.

        # Extrair dados do JSON
        quartos = data['NumeroQuartos']  # Obtém o número de quartos do JSON.
        banheiros = data['NumeroBanheiros']  # Obtém o número de banheiros do JSON.
        garagens = data['NumeroGaragens']  # Obtém o número de garagens do JSON.
        metros_quadrados = data['MetrosQuadrados']  # Obtém a quantidade de metros quadrados do JSON.
        encantamento = data['NumeroEncantamento']  # Obtém o número de encantamento do JSON.
        quadra_quadribol = 1 if data['QuadraQuadribol'] == 'S' else 0  # Converte a informação sobre QuadraQuadribol para 0 ou 1.

        # Criar o array de entrada
        X = np.array([[quartos, banheiros, garagens, metros_quadrados, encantamento, 0, 1]])  # Cria um array numpy com os parâmetros.

        # Imputar os valores ausentes nos dados
        X_imputed = imputer.transform(X)  # Preenche valores ausentes nos novos dados.

        # Fazer previsões
        aluguel_sugerido = model_aluguel.predict(X_imputed)[0]  # Realiza a previsão de sugestão de aluguel.
        venda_sugerida = model_venda.predict(X_imputed)[0]  # Realiza a previsão

        # Retornar sugestões em formato JSON
        return jsonify({'AluguelSugerido': aluguel_sugerido, 'ValorVendaSugerido': venda_sugerida})  # Retorna as sugestões em formato JSON.

# Executar a aplicação
if __name__ == '__main__':
    app.run(debug=True)  # Inicia a execução da aplicação Flask em modo de depuração.
