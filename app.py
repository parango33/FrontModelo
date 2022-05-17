from copyreg import pickle
from email.policy import default
import re
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import pickle
import numpy as np


app= Flask(__name__)

#Abrir modelo pre-entrenado
model = pickle.load(open('naivebayes.pkl','rb'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def home():

    #Nombre
    name = request.form['name']

    #Datos para el arreglo
    id= request.form['identification_type']
    site=request.form['site']
    gender=request.form['gender']
    age = request.form['age']
    marital = request.form['marital_status']
    children = request.form['number_of_children']
    blood = request.form['blood_type']
    rh = request.form['rh_blood']
    department = request.form['department']
    city = request.form['city']
    stratum = request.form['stratum']
    dependent = request.form['depend_people']
    hear = request.form['hear_about_us']
    aq = request.form['have_acquaintances']
    family = request.form['have_family_contact_center']
    referal = request.form['referral_external']
    transportation = request.form['have_transportation']
    ed = request.form['education_level']
    eng = request.form['learn_english']
    worked = request.form['worked_before_call_center']
    left = request.form['has_left']
    returns = request.form['number_of_returns']

    #arreglo con datos
    employee = np.array([[id,site,gender,age,marital,children,blood,rh,department,
                        city,stratum, dependent, hear, aq, family,referal,transportation,
                        ed, eng, worked, left, returns]])

    #predecir
    pred = model.predict(employee)

    #retorna
    return render_template('after.html',data=pred, namep = name)


if __name__ == "__main__":
    app.run(debug = True)    