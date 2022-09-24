from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from perceptron import Perceptron
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

user = 'root' #usuario mySQL
password = 'toor' #senha mySQL
host = '127.0.0.1' #host
port = 3306 #porta
database = 'statlog' #nome do database

sqlEngine = create_engine(url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database)) #conectando ao bd

dbConnection = sqlEngine.connect() #conectando

creditoDataSet = pd.read_sql("select * from statlog.germancredit", dbConnection) #salvando o dataset

pd.set_option('display.expand_frame_repr', False)

#Separando as entradas da IA
Dados = np.array(creditoDataSet[[
    'laufkont', 'laufzeit', 'moral', 'verw', 'hoehe', 'sparkont', 'beszeit', 'rate', 'famges', 'buerge',
    'wohnzeit', 'verm', 'alter', 'weitkred', 'wohn', 'bishkred', 'beruf', 'pers', 'telef', 'gastarb'
]])

#Separando a saída da IA
Resp = np.array(creditoDataSet['kredit'])

#Dividindo 80% para teino e 20% para teste
X_train, X_test, y_train, y_test = train_test_split(Dados, Resp, test_size=0.2, random_state=6)

#Definido a IA, sua taxa de apredizagem e o numero de épocas
p = Perceptron(lr = 0.0001, n_epochs = 2000)

#Treinando a IA
p.train(x = X_train, d = y_train)

#Realizando o teste com resultado da IA
teste_resultado = p.test(X_test)

#Métrica de avaliação da IA após treino e teste
print(f"Porcentegem = {accuracy_score(y_test, teste_resultado)*100}%")
print(f"Números de acertos = {accuracy_score(y_test, teste_resultado, normalize=False)}")


dbConnection.close() #fechando a conex