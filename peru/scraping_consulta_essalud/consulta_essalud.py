import requests
import json
URLCONSULTADNI="https://apps.essalud.gob.pe/dondemeatiendo-service/api/consultarAcreditacion?captchaToken=-"

def consultarDNI(dni,fechaNacimeinto):
    rptaJson={}
    try:

        header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
                "content-type":"application/json"}
        sesion=requests.session()
        digito=calculardigitoVerificacion(dni)
        payload={
                "codOpcion":"1",
                "codTipDoc": "1",
                "digitoVerif":digito,
                "fecNacimiento": fechaNacimeinto,#dd/mm/yyyy
                "numDoc":dni

            }
        req=sesion.post(URLCONSULTADNI,data=json.dumps( payload),headers=header,verify=False)
        print(req.status_code)
        if req.status_code==200:
            rptaJson=req.json()
                       
               
    except Exception as e:
        print("Error "+ str(e))
      
    return rptaJson

def calculardigitoVerificacion(dni):
  
    c = 0
    resultado = 0
    pesos =[3, 2, 7, 6, 5, 4, 3, 2, 1]

    digitos = [ "6", "7", "8", "9", "0", "1", "1", "2", "3", "4", "5"]
   

    for s in dni:
        print(s)
        resultado += (int(s) * pesos[c])
        c=c+1

    residuo = resultado % 11
    indice = (11 - residuo) if residuo > 0 else 0
    return digitos[indice]

if __name__=="__main__":
    print(consultarDNI("00000000","dd/mm/yyyy"))



