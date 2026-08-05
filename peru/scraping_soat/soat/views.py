from django.shortcuts import render
from django.http.response import HttpResponse,JsonResponse
from django.conf import settings
import requests
import json
import nodriver as uc
import asyncio
from nodriver import cdp
from nodriver.cdp.input_ import MouseButton

def index(request):

    return render(request,"Demo32.html")

def procesar(request):

    placa=request.POST.get("data")

    rptaJson={}
    print("buscar placa "+placa)
    try:
        header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"}
        sesion=requests.session()
        req=sesion.get("https://www.apeseg.org.pe/consultas-soat/",headers=header,verify=False)
        if req.status_code==200:
            header["host"]="webapp.apeseg.org.pe"
            header["origin"]="https://webapp.apeseg.org.pe"
            header["content-type"]="application/json"

            payload={"email":"notificaciones@apeseg.org.pe","password":"G3sepa13579!"}
            req=sesion.post("https://webapp.apeseg.org.pe/consulta-soat/api/login",headers=header,data=json.dumps(payload),verify=False)

            if req.status_code==200:
                objrpta=req.json()
                captchacloudflare=asyncio.run(obtenertoken())
                header["authorization"]=objrpta["token_type"]+" "+objrpta["access_token"]
                header["x-referrer"]="https://www.apeseg.org.pe/"
                header["x-source"]="apeseg"
                header["origin"]="https://webapp.apeseg.org.pe"
                header["referer"]="https://webapp.apeseg.org.pe/"
                header["cf-turnstile-response"]=captchacloudflare
                req=sesion.get("https://webapp.apeseg.org.pe/consulta-soat/api/certificados/placa/"+placa,headers=header,verify=False)
                print(req.status_code)
                if req.status_code==200:
                    rptaJson=req.json()


    except Exception as e:
        print("Error "+ str(e))
      
    return JsonResponse(rptaJson,safe=False)

async def obtenertoken():
    limite = asyncio.Semaphore(3)
    tokenencontrado=None
    async with limite:
        try:
            browser = await uc.start(browser_args=["--window-size=1051,806"])
            page = await browser.get("about:blank")
            await page.send(
                cdp.network.enable()
            )

            await page.send(
                cdp.network.set_blocked_ur_ls(
                    urls=[
                        "*.png",
                        "*.jpg",
                        "*.jpeg",
                        "*.gif",
                        "*.webp",
                        "*.svg",
                        "*.woff",
                        "*.woff2",
                        "*google-analytics*",
                        "*googletagmanager*"
                    ]
                )
            )

            page = await page.get("https://webapp.apeseg.org.pe/consulta-soat/?source=soat")
            contador=0
            while True:
                existeCludflare = await page.evaluate("""(() =>  window.turnstile !== undefined)()""")
                if existeCludflare:
                    token = await page.evaluate("""(() => document.querySelector('[name="cf-turnstile-response"]')?.value)()""")
                    print(token)
                    if token is not None and token!="" and str(token).find("ExceptionDetails")==-1:
                        print("--encontro token",token)
                        tokenencontrado=token
                        break
    
                    elif contador>2 and token is  None:
                        await page.send(
                                uc.cdp.input_.dispatch_mouse_event(
                                    type_="mousePressed",
                                    x=125,
                                    y=453,
                                    button=MouseButton.LEFT,
                                    click_count=1
                                )
                            )
                        await page.send(
                            uc.cdp.input_.dispatch_mouse_event(
                                type_="mouseReleased",
                                x=125,
                                y=453,
                                button=MouseButton.LEFT,
                                click_count=1
                            )
                        )
                        print("hizo clic a cloudflare")
                await page.sleep(0.5)
                if contador==70:
                    break
                contador=contador+1


        finally:
            browser.stop()
 
    return tokenencontrado