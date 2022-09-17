from sqlalchemy import create_engine
import pymysql
import pandas as pd
from perceptron import Perceptron;
import matplotlib.pyplot as plt

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
treinoDataSet = creditoDataSet[0:int(creditoDataSet.shape[0] * 0.8)]
avaliacDataSet = creditoDataSet[int(creditoDataSet.shape[0] * 0.8):]

#print(creditoDataSet)
#print(creditoDataSet.shape[0])
# print(treinoDataSet.shape)
# print(avaliacDataSet.shape)

p = Perceptron(lr = 0.1, n_epochs = 100)
p.train(x = treinoDataSet[:, 1:20], d = treinoDataSet[:, 21])

teste_resultado = p.test(avaliacDataSet[:, 1:20])
print(teste_resultado)

dbConnection.close() #fechando a conex