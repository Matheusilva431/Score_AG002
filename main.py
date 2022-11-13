import PySimpleGUI as sg
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from perceptron import Perceptron
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

sg.theme('DarkBlue 15')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Entre com a taxa de aprendizagem(Recomendado 7e-7): ')],
            [sg.InputText()],
            [sg.Text('Entre com o número de épocas (Recomendado 150000~160000 para lr=7e-7): ')],
            [sg.InputText()],
            [sg.Text('Entre com os dados a serem verificados(Recomendações para BOM/RUIM): ')],
            [sg.Text('Laufkont(2/1):       '), sg.InputText(size=(10,10)), sg.Text('laufzeit(10/48): '), sg.InputText(size=(10,10))],
            [sg.Text('moral(2/2):           '), sg.InputText(size=(10,10)), sg.Text('verw(0/0):         '), sg.InputText(size=(10,10))],
            [sg.Text('hoehe(7308/3931):'), sg.InputText(size=(10,10)), sg.Text('sparkont(1/1):  '), sg.InputText(size=(10,10))],
            [sg.Text('beszeit(1/4):         '), sg.InputText(size=(10,10)), sg.Text('rate(2/4):         '), sg.InputText(size=(10,10))],
            [sg.Text('famges(3/3):         '), sg.InputText(size=(10,10)), sg.Text('buerge(1/1):     '), sg.InputText(size=(10,10))],
            [sg.Text('wohnzeit(4/4):       '), sg.InputText(size=(10,10)), sg.Text('verm(4/4):        '), sg.InputText(size=(10,10))],
            [sg.Text('alter(70/46):          '), sg.InputText(size=(10,10)), sg.Text('weitkred(1/3):  '), sg.InputText(size=(10,10))],
            [sg.Text('wohn(3/3):            '), sg.InputText(size=(10,10)), sg.Text('bishkred(1/1):  '), sg.InputText(size=(10,10))],
            [sg.Text('beruf(4/3):           '), sg.InputText(size=(10,10)), sg.Text('pers(2/1):        '), sg.InputText(size=(10,10))],
            [sg.Text('telef(2/1):             '), sg.InputText(size=(10,10)), sg.Text('gastarb(2/2):    '), sg.InputText(size=(10,10))],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Cria a janela
window = sg.Window('Kreditanalysator', layout)
# Loop para os eventos e valores de entrada
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # break se o usuario fechar janela ou clicar em cancel
        break

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
    X_train, X_test, y_train, y_test = train_test_split(Dados, Resp, test_size=0.2, random_state=13)

    #Definido a IA, sua taxa de apredizagem e o numero de épocas
    p = Perceptron(lr = float(values[0]), n_epochs = int(values[1]))

    #Treinando a IA
    p.train(x = X_train, d = y_train)

    #Realizando o teste com resultado da IA
    teste_resultado = p.test(X_test)

    #Métrica de avaliação da IA após treino e teste
    sg.Popup(f"Porcentagem: {accuracy_score(y_test, teste_resultado) * 100}%"+f"\nNúmeros de acertos: {accuracy_score(y_test, teste_resultado, normalize=False)}", keep_on_top=True)
    score = accuracy_score(y_test, teste_resultado)
    print(f"Porcentegem = {accuracy_score(y_test, teste_resultado)*100}%")
    print(f"Números de acertos = {accuracy_score(y_test, teste_resultado, normalize=False)}")

    inHead = [
        values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10], values[11],
        values[12], values[13], values[14], values[15], values[16], values[17], values[18], values[19], values[20], values[21]
    ]
    inDado = np.array([])
    for i in inHead:
        #print(f"{i}: ")
        entrada = int(i)
        inDado = np.append(inDado, entrada)

    if p.activation(p.predict(inDado)) == 1:
        sg.Popup("Bom")
    else:
        sg.Popup("Ruim")

    dbConnection.close() #fechando a conex

window.close()
