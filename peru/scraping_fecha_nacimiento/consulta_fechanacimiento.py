import asyncio
import nodriver as uc
from nodriver import cdp
from nodriver.cdp.input_ import MouseButton
import requests
import json

URLCONSULTAFECHANAC="https://api1.midni.pe/verificar"
URLCONSULTAFECHANACORIGIN="https://midni.pe"


def consultarFechaNacimeinto(dni):
    rptaJson={}
    try:
        contextoSesion= uc.loop().run_until_complete(obtener_sesion())
        header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                "referer":URLCONSULTAFECHANACORIGIN+"/",
                "origin":URLCONSULTAFECHANACORIGIN,
                "content-type":"application/json"
                }

        sesion=requests.session()
        payload={"type":"DNI",
                 "document":dni,
                 "captcha_token":contextoSesion}

        req=sesion.post(URLCONSULTAFECHANAC,data=json.dumps(payload),headers=header,verify=False)
        print(req.status_code)
        if req.status_code==200:
            rpta=req.json()
            if "success" in rpta and rpta["success"]:
                obj=rpta["data"]

                rptaJson={"fechaNacimiento":obj["birthDate"],
                            "paterno":obj["paternalSurname"][0:3]+"******",
                            "materno":obj["maternalSurname"][0:3]+"******",
                            "nombre":obj["firstName"][0:3]+"******",
                            "dni":dni[0:3]+"*****"}
                        

                
                      
    except Exception as e:
        print("Error "+ str(e))
        rptaJson["dni"]=dni
        rptaJson["mensaje"]="Error en proceso de scraping"
      
    return rptaJson


async def obtener_sesion():

    sesionServicio=""
    browser = await uc.start(
        browser_args=[
            "--window-size=1051,806"
        ],
        user_data_dir="D:/Proyectos/ProyectosDjango/DemosYoutube/Demo91/perfil_chrome"
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

        await page.get("https://midni.pe/")
        
        contador=0
        while True:
        
                existeCludflare = await page.evaluate("""(() =>  window.turnstile !== undefined)()""")
                if existeCludflare:
                    token = await page.evaluate("""(() =>  turnstile.getResponse())()""")
                    if token is not None and token!="" and str(token).find("ExceptionDetails")==-1:
                        sesionServicio=token
                        #print("--encontro token",token)
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
                        #print("hizo clic a cloudflare")

                    contador=contador+1
                await page.sleep(1)
                if contador==100:
                     break
                
            
    finally:
        browser.stop()
    return sesionServicio


if __name__=="__main__":
    print(consultarFechaNacimeinto("11111111"))
