from sqlalchemy import create_engine
import pymysql
import pandas as pd
import numpy as np
from perceptron import Perceptron;
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

user = 'root' #usuario mySQL
password = 'toor' #senha mySQL
host = '127.0.0.1' #host
port = 3306 #porta
database = 'statlog' #nome do database

sqlEngine = create_engine(url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database)) #conectando ao bd

dbConnection = sqlEngine.connect() #conectando

creditoDataSet = pd.read_sql("select * from statlog.germancredit", dbConnection) #salvando o dataset

pd.set_option('display.expand_frame_repr', False)

#mudar a partir daqui usando a ia
# treinoDataSet = pd.DataFrame(creditoDataSet[0:int(creditoDataSet.shape[0] * 0.8)])
# avaliacDataSet = pd.DataFrame(creditoDataSet[int(creditoDataSet.shape[0] * 0.8):])
treinoDataSet = pd.DataFrame(creditoDataSet)

Dados = treinoDataSet[[
    'laufkont', 'laufzeit', 'moral', 'verw', 'hoehe', 'sparkont', 'beszeit', 'rate', 'famges', 'buerge',
    'wohnzeit', 'verm', 'alter', 'weitkred', 'wohn', 'bishkred', 'beruf', 'pers', 'telef', 'gastarb'
]]
Resp = treinoDataSet['kredit']

# avaliacDataSetDados = avaliacDataSet[[
#     'laufkont', 'laufzeit', 'moral', 'verw', 'hoehe', 'sparkont', 'beszeit', 'rate', 'famges', 'buerge',
#     'wohnzeit', 'verm', 'alter', 'weitkred', 'wohn', 'bishkred', 'beruf', 'pers', 'telef', 'gastarb'
# ]]

# avaliacDataSetResp = avaliacDataSet['kredit']

X_train, X_test, y_train, y_test = train_test_split(Dados, Resp, test_size=0.8, random_state=42)

# print(y_train)
# print(y_test)
# print(creditoDataSet)
# print(creditoDataSet.shape[0])
# print(treinoDataSet.shape)
# print(avaliacDataSet.shape)
# print(treinoDataSetResp.shape)
# print(avaliacDataSetResp.shape)
# print(treinoDataSetResp)

p = Perceptron(lr = 0.0001, n_epochs = 20000000)

p.train(x = X_train, d = y_train)

teste_resultado = p.test(X_test)
print(np.array(teste_resultado))
print(np.array(y_test))
print(np.array(np.array(teste_resultado)==np.array(y_test)))

dbConnection.close() #fechando a conex