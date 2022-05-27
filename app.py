from copyreg import pickle
from email.policy import default
import re
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import pickle
import numpy as np
import pandas as pd
import os
#file que transforma los datos
import transformData;


app= Flask(__name__)

#Abrir modelo pre-entrenado
model = pickle.load(open('naivebayes.pkl','rb'))

#UPLOADS
#Aca queda guardado el archivo json
app.config["FILE_UPLOADS"] = '/Users/pablo/Documents/2022-1/Tesis Sistemas/FrontModelo/static/uploads'
app.config["ALLOWED_FILE_EXTENSIONS"] = ["JSON"]



#Ruta inicial
@app.route('/')
def index():
    return render_template('index.html')
   
    


#Ruta para cargar un archivo
@app.route('/upload-employees', methods=["GET","POST"])
def upload_json():

    #Acceder al archivo
    if request.method == "POST":

        #Crea un storage object que contiene el archivo subido en el formulario
        if request.files: 

            file_upload = request.files["employees_file"]

            #Verificar que el archivo tenga un nombre
            if(file_upload.filename==''):
                print('The file must have a name')
                return redirect(request.url)


            #Guarda el archivo
            file_upload.save(os.path.join(app.config["FILE_UPLOADS"],file_upload.filename))

            print('The file has been uploaded')

            #Toma los datos cargados y los guarda en el archivo: "datos_nuevos_entrantes.csv"
            transformData.transfrom_json()

            #Carga los datos del csv y los pone en formato dataframe    
            df_employees_loaded = pd.read_csv('datos_nuevos_entrantes.csv')  

            print("The has been uploaded")

            #Dataframe pero sin tener el cuenta el nnumero de identificacion
            df_employees_ready = df_employees_loaded.drop(['id_number'],axis=1)


            #Transfromar dataframe con mascaras
            df_final = transformData.transform_df(df_employees_ready)

            

            #Entrena el modelo con los datos cargados
            predicciones = model.predict(df_final)

            #Predicciones con probabilidad
            pred_proba = model.predict_proba(df_final)
            dfproba= pd.DataFrame(list(map(np.ravel, pred_proba))) #Convertir a df
            zeros = dfproba[0] #Probabilidades de non risky
            ones = dfproba[1] #Probabilidades de risky

            #Anadir columnas de predicciones a dataframe original
            df_employees_loaded['Risky Employee']=predicciones

            df_employees_loaded['Probability of Non Risk']=zeros.to_list()
            df_employees_loaded['Probability of Risk']=ones.to_list()


            #Nuevo dataframe solo con columnas seleccionnadas
            df_show_front = df_employees_loaded[['id_number', 'site', 'education_level','Risky Employee','Probability of Non Risk','Probability of Risk']].copy()
            df_show_front = df_show_front.rename(columns={'id_number': 'Identification Number', 'site': 'Current Working Site','education_level':'Education Level','Risky Employee':'Is the Employee High Risk?'}) #Cambiar nombres

            print(pred_proba)

            return render_template('upload_image.html',tables=[df_show_front.to_html(classes='data')],titles=df_show_front.columns.values)

            #Imprime predicciones
            #print(predicciones)
           



            return redirect(request.url)


    return render_template('upload_image.html')

    



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
    #left = request.form['has_left']
    #returns = request.form['number_of_returns']
    profession = request.form['profession']

    #arreglo con datos
    employee = np.array([[id,site,gender,age,marital,children,blood,rh,department,
                        city,stratum, dependent, hear, aq, family,referal,transportation,
                        ed,profession, eng, worked]])

    #predecir
    pred = model.predict(employee)

    #retorna
    return render_template('after.html',data=pred, namep = name)


if __name__ == "__main__":
    app.run(debug = True)    