import requests
import pyodbc
from datetime import datetime,timedelta
import json
import time

def ejecutarComando( nombreSP, nombreParametro="", valorParametro="",commit=False):
    driver ="{ODBC Driver 17 for SQL Server}"
    servidor = "127.0.0.1"
    usuario = "sa"
    clave = "sql"
    basedatos = "BDConexionAduanas"
    TrustServerCertificate = "yes"
    CadenaConexion = "Driver={0};server={1};database={2};UID={3};PWD={4};TrustServerCertificate={5}".format(driver, servidor, basedatos, usuario, clave,TrustServerCertificate)


    rpta = None
    try:
        conn = pyodbc.connect(CadenaConexion)
        cursor = conn.cursor()
        if(nombreParametro!="" and valorParametro!=""):
            cursor.execute("exec {0} @{1}=?".format(nombreSP, nombreParametro), (valorParametro,))
        else:
            cursor.execute(nombreSP)
        rpta = cursor.fetchval()
        if commit:
            cursor.commit()

        cursor.close()
        conn.close()
    except Exception as error:
        print("Error ejecutarComando: {0}".format(str(error)))
        
        
        rpta=None
    return rpta

def main(fechaconsulta):

    
    url=f"https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04639PD-PD04640PD-PD04647PD-PD04648PD/json/{fechaconsulta}/{fechaconsulta}"

    req=requests.get(url)
    print(req.status_code)
    if req.status_code==200:
        obj=req.text
        objjson=json.loads(obj)
        #print(objjson)

        if "periods" in objjson and len(objjson["periods"])>0:
            lista=objjson["periods"][0]
            [usdcompra,usdventa,eucompra,euventa]=lista["values"]
            print(usdcompra,usdventa,eucompra,euventa)
            if usdventa=="n.d.":
                fechaconsultanueva=datetime.strptime(fechaconsulta,"%Y-%m-%d")
                fechaconsulta=(fechaconsultanueva-timedelta(days=1)).strftime("%Y-%m-%d")
                time.sleep(5)
                main(fechaconsulta)
            else:
                fechaactual=datetime.now().strftime("%Y-%m-%d")
                lista=[fechaactual+"¦USD¦"+usdcompra+"¦"+usdventa,fechaactual+"¦XEU¦"+eucompra+"¦"+euventa]
                tipoCambioGrabar(lista)
        else:
            fechaconsultanueva=datetime.strptime(fechaconsulta,"%Y-%m-%d")
            fechaconsulta=(fechaconsultanueva-timedelta(days=1)).strftime("%Y-%m-%d")
            time.sleep(5)
            main(fechaconsulta)



def tipoCambioGrabar(listaTipoCambio):   

    print(listaTipoCambio)
    rpta=ejecutarComando("uspTipoCambioBacheroGrabar","lstparametros","¬".join(listaTipoCambio),True)
    print("*"*20)
    print(rpta)
    

if __name__ == '__main__':
    fechaactual=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
    main(fechaactual)
