from django.shortcuts import render
from django.http.response import HttpResponse,JsonResponse
from django.conf import settings

import requests
import io
from PIL import Image
import numpy as np
import easyocr
import cv2
import time
import json
import os


reader = easyocr.Reader(['en'])
def index(request):

    return render(request,"Demo59.html")

def procesar(request):

    placa=request.POST.get("data")

    rptaJson={}

    try:
        rptaJson=buscarVehiculo(placa)


    except Exception as e:
        print("Error "+ str(e))
      
    return JsonResponse(rptaJson,safe=False)

def buscarVehiculo(placa):
    rptaJson={}
    print("buscar placa "+placa)
    try:
        header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
                }
        print("*"*20)
        sesion=requests.session()
        req=sesion.get("https://sistemas.policia.gob.pe.regpol.digital",headers=header,verify=False)#
        if req.status_code==200:
      

            captcha=obtenerCaptcha(sesion)
            acaptcha=captcha.split("|")
            print(acaptcha)
            if len(acaptcha)==2:
        
                header["origin"]="https://sistemas.policia.gob.pe.regpol.digital"

                header["referer"]="https://sistemas.policia.gob.pe.regpol.digital/"
                header["content-type"]="application/json"


                payload = {
                    "captcha_resuelto": acaptcha[0],
                    "session_id": acaptcha[1],
                    "tipo_certificado": "Placa",
                    "valor": placa
    
                }

                tiempo=int(time.time() * 1000)
                req=sesion.post("https://sistemas.policia.gob.pe.regpol.digital/api_proxy.php?action=consultar&t="+str(tiempo),data=json.dumps(payload) ,headers=header,verify=False)
    
                if req.status_code==200:
                    rpta=req.json()
                    print(rpta)
                    if "ok" in rpta and rpta["ok"] and "datos" in rpta:
                        rptaJson=rpta["datos"]
                    if "mensaje" in rpta and rpta["mensaje"]=="Captcha incorrecto o sin datos":
                        rptaJson=buscarVehiculo(placa)
            else:
                rptaJson=buscarVehiculo(placa)


    except Exception as e:
        print("Error "+ str(e))
    return rptaJson



def obtenerCaptcha(sesion,ms=None):
    global reader
    headers2={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
                "referer":"https://sistemas.policia.gob.pe.regpol.digital/",
                "sec-fetch-dest":"empty"
                }
    
    tiempo=int(time.time() * 1000) if ms is None else ms
    req=sesion.get("https://sistemas.policia.gob.pe.regpol.digital/api_proxy.php?action=captcha&t="+str(tiempo),headers=headers2,verify=False)
    captcha=""
    sessionid=""
    if req.status_code==200:
        r=req.json()
        print(r)
        if "ok" in r and r["ok"]:
            sessionid=r["session_id"]

            headers2["sec-fetch-dest"]="image"
            req=sesion.get(r["image_url"],headers=headers2,verify=False)
            captcha=""
            if req.status_code==200:

                imgByte=io.BytesIO(req.content)
                img=Image.open(imgByte)

                if os.path.exists("captcha.png"):
                    os.remove("captcha.png")

                img.save("captcha"+str(tiempo)+".png",format="PNG")

                gray=cv2.imread("captcha"+str(tiempo)+".png",0)
                thresholded = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                cv2.imwrite("captcha2.png",thresholded)
                kernel = np.ones((3,3), np.uint8) # Kernel de 5x5 de unos
          

                caracteres_permitidos = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                result=reader.readtext(thresholded, detail = 0, paragraph=True)#,allowlist=caracteres_permitidos
                print("capcha:",result)
                if result is not None and len(result)>0:
                    captcha=result[0].replace(" ","").strip().replace("~","").replace("_","").replace("-","").replace("!","").replace("*","").upper()
                    print(captcha)

    if len(captcha)!=5:
        captcha=""#obtenerCaptcha(sesion,tiempo + (20 * 60 * 1000))
    else:
        captcha=captcha+"|"+sessionid
    return captcha
