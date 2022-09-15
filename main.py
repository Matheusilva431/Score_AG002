from sqlalchemy import create_engine
import pymysql
import pandas as pd

user = 'root'
password = 'toor'
host = '127.0.0.1'
port = 3306
database = 'statlog'

sqlEngine = create_engine(url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))

dbConnection = sqlEngine.connect()

creditoDataSet = pd.read_sql("select * from statlog.germancredit", dbConnection);

pd.set_option('display.expand_frame_repr', False)

treinoDataSet = creditoDataSet[0:int(creditoDataSet.shape[0] * 0.8)]
avaliacDataSet = creditoDataSet[int(creditoDataSet.shape[0] * 0.8):]

#print(creditoDataSet)
#print(creditoDataSet.shape[0])
print(treinoDataSet.shape)
print(avaliacDataSet.shape)




dbConnection.close()