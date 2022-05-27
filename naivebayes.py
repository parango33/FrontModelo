import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, BernoulliNB, CategoricalNB, ComplementNB, MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report, precision_score, recall_score, f1_score, accuracy_score

import pickle

import ast

#Importar datos
df_test = pd.read_csv('datos_ready_final.csv')

#Fijar el Target para el modelo
target = df_test.risky_employee
inputs = df_test.drop('risky_employee', axis='columns')

#Separar datos train y test
x_train, x_test, y_train, y_test = train_test_split(inputs,target,test_size=0.1)

#modelo
model = GaussianNB()
model.fit(x_train,y_train)
model.score(x_test,y_test)

#Exportar modelo
pickle.dump(model,open('naivebayes.pkl','wb'))

