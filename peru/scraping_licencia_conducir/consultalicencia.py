
import requests
import io
from PIL import Image
import numpy as np
import easyocr
import cv2

URLLICENCIA="https://recordconductor.mtc.gob.pe/"
URLLICENCIABUSQUEDA="https://recordconductor.mtc.gob.pe/RecCon/ObtenerDatosAdministrado?str_tpbusqueda=1&str_tipo_documento=2&str_num_documento=@DNI&str_captcha=@SESION"

URLLICENCIAVALIDO="captchaisvalid"
URLLICENCIAHOST="recordconductor.mtc.gob.pe"
URLLICENCIAREFERER="https://recordconductor.mtc.gob.pe/"

reader = easyocr.Reader(['en'])

def procesar(dni):

    rptaJson={}
    try:
        rptaJson=buscarLicencia(dni)

    except Exception as e:
        print("Error "+ str(e))
      
    return rptaJson

def buscarLicencia(dni):
    rptaJson={}

    try:
        header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }

        sesion=requests.session()
        req=sesion.get(URLLICENCIA,headers=header,verify=False)
        if req.status_code==200:

            ctxSesion=obtenerContextSesion(sesion)
    
            header["host"]=URLLICENCIAHOST
            header["referer"]=URLLICENCIAREFERER
            url=URLLICENCIABUSQUEDA.replace("@DNI",dni).replace("@SESION",ctxSesion)
            req=sesion.get(url,headers=header,verify=False)
            
            if req.status_code==200:
                rpta=req.json()
                if "dato" in rpta and len(rpta["dato"])>0:
                    datos=rpta["dato"][0]
                    rptaJson["dni"]=dni[0:3]+"****"
                    rptaJson["paterno"]=datos["var_apellido_paterno"][0:3]+"****"
                    rptaJson["materno"]=datos["var_apellido_materno"][0:3]+"****"
                    rptaJson["nombre"]=datos["var_nombre"][0:3]+"****"
                    rptaJson["licencia"]=datos["var_num_licencia"][0:4]+"****"
                    rptaJson["correlativo_licencia"]=datos["var_num_correlato_licencia"]
                    rptaJson["categoria"]=datos["var_categoria"]
                    rptaJson["clase"]=datos["var_clase"]
                    rptaJson["restricciones"]=datos["var_restricciones1"]
                    rptaJson["estado"]=datos["var_estado_licencia"]
                    rptaJson["papeletas"]=[]
                    if len(rpta["dato2"])>0:
                        for i in rpta["dato2"]:
                            rptaJson["papeletas"].append({"falta":i["falta"],"fecha":i["fec_infraccion"],"papeleta":i["papeleta"]})
                if URLLICENCIAVALIDO in rpta and rpta[URLLICENCIAVALIDO]==False:
                    rptaJson=buscarLicencia(dni)


    except Exception as e:
        print("Error "+ str(e))
    return rptaJson



def obtenerContextSesion(sesion):
    global reader
    headers2={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "host":"recordconductor.mtc.gob.pe",
                "referer":"https://recordconductor.mtc.gob.pe/",
                }
    
     
    req=sesion.get("https://recordconductor.mtc.gob.pe/Captcha/CaptchaImage?0.32525617158138354",headers=headers2,verify=False)
    captcha=""
    if req.status_code==200:

        imgByte=io.BytesIO(req.content)
        img=Image.open(imgByte)
        imgnp=np.array(img)
        img.save("captcha.png",format="PNG")

        gray=cv2.imread("captcha.png",0)
        thresholded = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        cv2.imwrite("captcha2.png",thresholded)
        kernel = np.ones((3,3), np.uint8) # Kernel de 5x5 de unos
 

        caracteres_permitidos = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result=reader.readtext(gray, detail = 0, paragraph=True,allowlist=caracteres_permitidos)
        print("sesion",result)
        if result is not None and len(result)>0:
            captcha=result[0].replace(" ","").strip().replace("~","").replace("_","").replace("-","").upper()
            print(captcha)
    if len(captcha)!=6:
        captcha=obtenerContextSesion(sesion)
    return captcha


if __name__=="__main__":
    print(procesar("12345678"))