import time
start = time.time()

 #Importar librerias
import csv
import time
import math
import json
import pandas as pd
import numpy as np
#apagar los warnings
import warnings 
warnings.filterwarnings('ignore')

#Toma el archivo json y guarda los datos en un csv llamado datos_nuevos_entrantes
def transfrom_json():
    #Leer datos json y pasarlos a un csv
    f = open('datos_nuevos_entrantes.csv', 'w')


    writer = csv.writer(f)

    header = [
                "id_number",
                "identification_type",
                "site",
                "gender",
                "age",
                "marital_status",
                "number_of_children",
                "blood_type",
                "rh_blood",
                "department",
                "city",
                "stratum",
                "depend_people",
                "hear_about_us",
                "have_acquaintances",
                "have_family_contact_center",
                "referral_external",
                "have_transportation",
                "education_level",
                "profession",
                "learn_english",
                "worked_before_call_center"
    ]

    writer.writerow(header)

    #response.json son los datos de los nuevos entrantes
    with open('static/uploads/response.json') as json_file:
        jsondata = json.load(json_file)


    for data in jsondata:
        try:

            z = data.get('status_active')
            y = z.get('user')
            m = y.get('personal_information')
            education = y.get('education_information')
            callCenter = y.get('call_center_information')

            if data['agent'].lower() == 'agent' :
                data = [
                            m.get("id_number"),
                            m.get("identification_type"),
                            y.get("site"),
                            m.get("gender"),
                            m.get("age"),
                            m.get("marital_status"),
                            m.get("number_of_children"),
                            m.get("blood_type"),
                            m.get("rh_blood"),
                            m.get("department"),
                            m.get("city"),
                            m.get("stratum"),
                            m.get("depend_people"),
                            m.get("hear_about_us"),
                            m.get("have_acquaintances"),
                            m.get("have_family_contact_center"),
                            m.get("referral_external"),
                            m.get("have_transportation"),
                            education.get("education_level"),
                            education.get("profession"),
                            education.get("learn_english"),
                            callCenter.get("worked_before")]
                        
                writer.writerow(data)      

        except Exception as e:
            print(e)
    f.close()    


#Transformar datos del dataframe utilizando las mascaras
def transform_df(dftest):
    #idtype
    dftest['identification_type'] = dftest['identification_type'].astype('str') 
    maskPPT = dftest['identification_type'].str.contains('PPT')
    maskResident = dftest['identification_type'].str.contains('Resident') | dftest['identification_type'].str.contains('PA')
    maskCE = dftest['identification_type'].str.contains('CE')
    maskPEP = dftest['identification_type'].str.contains('PEP')
    maskTI = dftest['identification_type'].str.contains('TI')
    maskCC = dftest['identification_type'].str.contains('CC')

    dftest.loc[maskPPT,'identification_type'] = 1
    dftest.loc[maskResident,'identification_type'] = 0
    dftest.loc[maskCE,'identification_type'] = 2
    dftest.loc[maskPEP,'identification_type'] = 3
    dftest.loc[maskTI,'identification_type'] = 4
    dftest.loc[maskCC,'identification_type'] = 5


    #profesion
    maskNan = (dftest['profession']).isna()
    maskNotNan = ~ maskNan
    dftest.loc[maskNan,'profession'] = 0
    dftest.loc[maskNotNan,'profession'] = 1

    #gender
    dftest['gender'] = dftest['gender'].astype('str') 
    maskFemale = dftest['gender'].str.contains('Female')
    maskMale = dftest['gender'].str.contains('Male')

    dftest.loc[maskFemale,'gender'] = 0
    dftest.loc[maskMale,'gender'] = 1

    #Marrital status
    dftest['marital_status'] = dftest['marital_status'].astype('str') 
    maskSingleMother = dftest['marital_status'].str.contains('Single Mother')
    maskSingleFather  = dftest['marital_status'].str.contains('Single Father')
    maskCommonlawmarriage = dftest['marital_status'].str.contains('Common law marriage')
    maskMarried = dftest['marital_status'].str.contains('Married') | dftest['marital_status'].str.contains('asado')
    maskSingle = (dftest['marital_status'] == ('Single')) | dftest['marital_status'].str.contains('oltero')
    maskULibre = dftest['marital_status'].str.contains('ibre')    

    dftest.loc[maskSingleMother,'marital_status'] = 2
    dftest.loc[maskSingleFather,'marital_status'] = 1
    dftest.loc[maskCommonlawmarriage,'marital_status'] = 3
    dftest.loc[maskMarried,'marital_status'] = 4
    dftest.loc[maskSingle,'marital_status'] = 5
    dftest.loc[maskULibre,'marital_status'] = 0


    #blood type
    dftest['blood_type'] = dftest['blood_type'].astype('str') 
    maskO = (dftest['blood_type'] =='O')
    maskA  = (dftest['blood_type']=='A')
    maskB= (dftest['blood_type']=='B')
    maskAB = (dftest['blood_type']=='AB')
    masko = (dftest['blood_type']=='o')
    maskCorreccion = (dftest['blood_type']=='-')

    dftest.loc[maskO,'blood_type'] = 3
    dftest.loc[masko,'blood_type'] = 3
    dftest.loc[maskA,'blood_type'] = 2
    dftest.loc[maskB,'blood_type'] = 1
    dftest.loc[maskAB,'blood_type'] = 0
    dftest.loc[maskCorreccion,'blood_type'] = 3

    #rh
    dftest['rh_blood'] = dftest['rh_blood'].astype('str') 
    maskPositive = (dftest['rh_blood'] =='Positive')
    maskNegative = (dftest['rh_blood']=='Negative')
    masknull = ~ maskPositive & ~ maskNegative

    dftest.loc[maskPositive,'rh_blood'] = 1
    dftest.loc[maskNegative,'rh_blood'] = 0
    dftest.loc[masknull,'rh_blood'] = 1 

    #department
    dftest['department'] = dftest['department'].astype('str') 
    maskAmazonas = dftest['department'].str.contains('zonas')
    maskAntioquia = dftest['department'].str.contains('tioquia')
    maskArauca = dftest['department'].str.contains('rauca')
    maskAtlantico = dftest['department'].str.contains('ntico')
    maskBogota = dftest['department'].str.contains('Bogo')
    maskBolivar= dftest['department'].str.contains('Bol')
    maskBoyaca = dftest['department'].str.contains('Boya')
    maskCaldas = dftest['department'].str.contains('Caldas')
    maskCaqueta = dftest['department'].str.contains('Caquet')
    maskCasanare = dftest['department'].str.contains('Casa')
    maskCauca = dftest['department'].str.contains('Cauca')
    maskCesar = dftest['department'].str.contains('Cesar')
    maskChoco = dftest['department'].str.contains('Choc')
    maskCordoba = dftest['department'].str.contains('rdoba')
    maskCundinamarca = dftest['department'].str.contains('Cundi')
    maskGuainia = dftest['department'].str.contains('Guai')
    maskGuaviare = dftest['department'].str.contains('Guavi')
    maskHuila = dftest['department'].str.contains('Huila')
    maskGuajira = dftest['department'].str.contains('Guajira')
    maskMagdalena = dftest['department'].str.contains('alena')
    maskMeta = dftest['department'].str.contains('Meta')
    maskNarino = dftest['department'].str.contains('Nari')
    maskNorteSantander = dftest['department'].str.contains('Norte')
    maskPutumayo = dftest['department'].str.contains('Putumayo')
    maskQuindio = dftest['department'].str.contains('Quind')
    maskRisaralda = dftest['department'].str.contains('Risaralda')
    maskSanAndres = dftest['department'].str.contains('Andr')
    maskSantander = dftest['department'].str.contains('Santan')
    maskSucre = dftest['department'].str.contains('Sucre')
    maskTolima = dftest['department'].str.contains('Tolima')
    maskValleDelCauca= dftest['department'].str.contains('Valle')
    maskVaupes = dftest['department'].str.contains('Vaup')
    maskVichada = dftest['department'].str.contains('Vichada')

    dftest.loc[maskAmazonas,'department'] = 91
    dftest.loc[maskAntioquia,'department'] = 5
    dftest.loc[maskArauca,'department'] = 81
    dftest.loc[maskAtlantico,'department'] = 8
    dftest.loc[maskBogota,'department'] = 11
    dftest.loc[maskBolivar,'department'] = 13
    dftest.loc[maskBoyaca,'department'] = 15
    dftest.loc[maskCaldas,'department'] = 17
    dftest.loc[maskCaqueta,'department'] = 18
    dftest.loc[maskCasanare,'department'] = 85
    dftest.loc[maskCauca,'department'] = 19
    dftest.loc[maskCesar,'department'] = 20
    dftest.loc[maskChoco,'department'] = 27
    dftest.loc[maskCordoba,'department'] = 23
    dftest.loc[maskCundinamarca,'department'] = 25
    dftest.loc[maskGuainia,'department'] = 94
    dftest.loc[maskGuaviare,'department'] = 95
    dftest.loc[maskHuila,'department'] = 41
    dftest.loc[maskGuajira,'department'] = 44
    dftest.loc[maskMagdalena,'department'] = 47
    dftest.loc[maskMeta,'department'] = 50
    dftest.loc[maskNarino,'department'] = 52
    dftest.loc[maskNorteSantander,'department'] = 54
    dftest.loc[maskPutumayo,'department'] = 86
    dftest.loc[maskQuindio,'department'] = 63
    dftest.loc[maskRisaralda,'department'] = 66
    dftest.loc[maskSanAndres,'department'] = 88
    dftest.loc[maskSantander,'department'] = 68
    dftest.loc[maskSucre,'department'] = 70
    dftest.loc[maskTolima,'department'] = 73
    dftest.loc[maskValleDelCauca,'department'] = 76
    dftest.loc[maskVaupes,'department'] = 97
    dftest.loc[maskVichada,'department'] = 99

    #Ciudad
    maskPei = dftest['city'].str.contains('Perei') | dftest['city'].str.contains('perei')
    maskBucaramanga = dftest['city'].str.contains('Buca') | dftest['city'].str.contains('buca')
    maskCali = dftest['city'].str.contains('Cali') | dftest['city'].str.contains('cali')
    maskBogo = dftest['city'].str.contains('Bogo') | dftest['city'].str.contains('bogo') | dftest['city'].str.contains('Bogotá')
    maskOtros = ~maskPei & ~maskBucaramanga & ~maskBogo & ~maskCali

    dftest.loc[maskPei,'city'] = 1
    dftest.loc[maskBucaramanga,'city'] = 2
    dftest.loc[maskCali,'city'] = 0
    dftest.loc[maskBogo,'city'] = 4
    dftest.loc[maskOtros,'city'] = 3

    #site
    dftest['site'] = dftest['site'].astype('str') 
    maskPei = dftest['site'].str.contains('perei')
    maskBucaramanga = dftest['site'].str.contains('buca')
    maskCali = dftest['site'].str.contains('cali')
    maskBogo = dftest['site'].str.contains('bogo')

    dftest.loc[maskPei,'site'] = 0
    dftest.loc[maskBucaramanga,'site'] = 1
    dftest.loc[maskCali,'site'] = 3
    dftest.loc[maskBogo,'site'] = 2

    #hear about us
    maskSocial = dftest['hear_about_us'].str.contains('Apply') | dftest['hear_about_us'].str.contains('stagra') | dftest['hear_about_us'].str.contains('book') | dftest['hear_about_us'].str.contains('oogl') | dftest['hear_about_us'].str.contains('sapp')
    maskReferidos = dftest['hear_about_us'].str.contains('iend') | dftest['hear_about_us'].str.contains('mily') | dftest['hear_about_us'].str.contains('eferral')
    maskFerias = dftest['hear_about_us'].str.contains('air') | dftest['hear_about_us'].str.contains('iversity') | dftest['hear_about_us'].str.contains('camello') | dftest['hear_about_us'].str.contains('Sena') 
    maskComputrabajoOtros = dftest['hear_about_us'].str.contains('trabajo') | dftest['hear_about_us'].str.contains('mpleo')
    maskOtros = ~ maskSocial & ~maskReferidos & ~ maskFerias & ~ maskComputrabajoOtros

    dftest.loc[maskSocial,'hear_about_us'] = 4
    dftest.loc[maskReferidos,'hear_about_us'] = 3
    dftest.loc[maskFerias,'hear_about_us'] = 0
    dftest.loc[maskComputrabajoOtros,'hear_about_us'] = 2
    dftest.loc[maskOtros,'hear_about_us'] = 1


    #aquatiences
    maskAcquaintancesTrue = dftest['have_acquaintances']
    maskAcquaintancesFalse = ~ maskAcquaintancesTrue

    dftest.loc[maskAcquaintancesTrue,'have_acquaintances'] = 1
    dftest.loc[maskAcquaintancesFalse,'have_acquaintances'] = 0

    #family
    maskFamilyTrue = dftest['have_family_contact_center']
    maskFamilyFalse = ~ maskFamilyTrue
    dftest.loc[maskFamilyTrue,'have_family_contact_center'] = 1
    dftest.loc[maskFamilyFalse,'have_family_contact_center'] = 0
    dftest['have_family_contact_center'].value_counts()

    maskReferalTrue = dftest['referral_external']
    maskReferalFalse = ~ maskReferalTrue
    dftest.loc[maskReferalTrue,'referral_external'] = 1
    dftest.loc[maskReferalFalse,'referral_external'] = 0
    dftest['referral_external'].value_counts()

    #Transportation
    dftest['have_transportation'] = dftest['have_transportation'].astype('bool') 
    maskTransportationTrue = dftest['have_transportation']
    maskTransportationFalse = ~maskTransportationTrue
    dftest.loc[maskTransportationTrue,'have_transportation'] = 1
    dftest.loc[maskTransportationFalse,'have_transportation'] = 0
    dftest['have_transportation'].value_counts()

    #Educacion
    maskBachiller = dftest['education_level'].str.contains('Bachiller') | dftest['education_level'].str.contains('Bachelor')
    maskEstudianteUni = dftest['education_level'].str.contains('Estudiante universitario') | dftest['education_level'].str.contains('College student') 
    maskProfesional = dftest['education_level'].str.contains('Profesional') | dftest['education_level'].str.contains('Professional')
    maskTecnico = dftest['education_level'].str.contains('Tecnico') | dftest['education_level'].str.contains('Tecnologo') | dftest['education_level'].str.contains('Technical') | dftest['education_level'].str.contains('Technologist')
    maskMaster = ~maskTecnico & ~maskEstudianteUni & ~maskBachiller & ~maskProfesional

    dftest.loc[maskBachiller,'education_level'] = 4
    dftest.loc[maskEstudianteUni,'education_level'] = 3
    dftest.loc[maskProfesional,'education_level'] = 1
    dftest.loc[maskTecnico,'education_level'] = 2
    dftest.loc[maskMaster,'education_level'] = 0

    #English
    dftest['learn_english'] = dftest['learn_english'].astype('str') 
    dftest['learn_english'].value_counts()

    maskMyself = dftest['learn_english'].str.contains('yself') 
    maskUni = dftest['learn_english'].str.contains('niver') | dftest['learn_english'].str.contains('utp') | dftest['learn_english'].str.contains('UTP') 
    maskCole= dftest['learn_english'].str.contains('chool') 
    maskInstituto = dftest['learn_english'].str.contains('mericano') | dftest['learn_english'].str.contains('tute') | dftest['learn_english'].str.contains('entro')
    maskOtro = ~maskMyself & ~maskUni & ~maskCole & ~maskInstituto

    dftest.loc[maskMyself,'learn_english'] = 3
    dftest.loc[maskUni,'learn_english'] = 1
    dftest.loc[maskCole,'learn_english'] = 0
    dftest.loc[maskInstituto,'learn_english'] = 2
    dftest.loc[maskOtro,'learn_english'] = 4

    #worked before call center
    dftest['worked_before_call_center'] = dftest['worked_before_call_center'].astype('bool') 

    maskWorkedBeforeCallCenterTrue = dftest['worked_before_call_center']
    maskWorkedBeforeCallCenterFalse = ~maskWorkedBeforeCallCenterTrue
    dftest.loc[maskWorkedBeforeCallCenterTrue,'worked_before_call_center'] = 1
    dftest.loc[maskWorkedBeforeCallCenterFalse,'worked_before_call_center'] = 0
    dftest['worked_before_call_center'].value_counts()

    #Retornar dataframe transformado
    return dftest




























    



