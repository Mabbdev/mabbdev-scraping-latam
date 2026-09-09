import asyncio
import nodriver as uc
import asyncio
from nodriver import cdp
from nodriver.cdp.input_ import MouseButton
import requests
import json
import asyncio



def procesar(placa):

    try:

        header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                "host":"webapp.apeseg.org.pe",
                "content-type":"application/json"
                }

        sesion=requests.session()
        payload={
            "email":"notificaciones@apeseg.org.pe","password":"G3sepa13579!"}

        req=sesion.post(" https://webapp.apeseg.org.pe/consulta-soat/api/login",data=json.dumps(payload),headers=header,verify=False)
        print(req.status_code)
        if req.status_code==200:
            rpta=req.json()
            if "access_token" in rpta:
                token= uc.loop().run_until_complete(obtener_token_optimizado())
                header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                    "host":"webapp.apeseg.org.pe",
                    "authorization":"Bearer "+rpta["access_token"],
                    "cf-turnstile-response":token,
                    "x-source":"apeseg",
                    "x-referrer":"https://www.apeseg.org.pe/",
                    }


                req=sesion.get("https://webapp.apeseg.org.pe/consulta-soat/api/certificados/placa/"+placa,headers=header,verify=False)
                print(req.status_code)
                if req.status_code==200:
                    rpta=req.json()

                    if rpta is not None and len(rpta)>0:
                        rptaJson=rpta[0]
                      
    except Exception as e:
        print("Error "+ str(e))
        rptaJson["mensaje"]="Error en proceso de scraping"
      
    return rptaJson


async def obtener_token_optimizado():

    tokenServicio=""
    browser = await uc.start(
        browser_args=[
            "--window-size=1051,806"
        ]
    )
    page = await browser.get("about:blank")

    await page.send(
            cdp.network.enable()
        )
    
    await page.send(uc.cdp.network.set_blocked_ur_ls(urls=["*.png",
                    "*.jpg",
                    "*.jpeg",
                    "*.gif",
                    "*.webp",
                    "*.svg",
                    "*.woff",
                    "*.woff2",
                    "*google-analytics*",
                    "*googletagmanager*"]))
    
    try:
        await page.get("https://webapp.apeseg.org.pe/consulta-soat/?source=apeseg")
        
        print("Esperando la generación del token...")
        contador=0
        while True:
        
                existeCludflare = await page.evaluate("""(() =>  window.turnstile !== undefined)()""")
                if existeCludflare:
                    token = await page.evaluate("""(() =>  turnstile.getResponse())()""")
                    if token is not None and token!="" and str(token).find("ExceptionDetails")==-1:
                        tokenServicio=token
                        print("--encontro token",token)
                        break
  
                    elif contador>1 and (token is None or token==""):
                        await page.send(
                                uc.cdp.input_.dispatch_mouse_event(
                                    type_="mousePressed",
                                    x=125,
                                    y=454,
                                    button=MouseButton.LEFT,
                                    click_count=1
                                )
                            )
                        await page.send(
                            uc.cdp.input_.dispatch_mouse_event(
                                type_="mouseReleased",
                                x=125,
                                y=454,
                                button=MouseButton.LEFT,
                                click_count=1
                            )
                        )
                        print("hizo clic a cloudflare")

                    contador=contador+1
                await page.sleep(0.5)
                if contador==100:
                     break
                
            
    finally:
        browser.stop()
    return tokenServicio

def consultarplaca():
    print(procesar("brn365"))



if __name__=="__main__":
    consultarplaca()

