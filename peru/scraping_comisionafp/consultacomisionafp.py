import asyncio
import nodriver as uc
from nodriver import cdp
from nodriver.cdp.input_ import MouseButton
from bs4 import BeautifulSoup
from nodriver.cdp.input_ import MouseButton
import json

async def main():

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
    page = await browser.get('https://www.sbs.gob.pe/app/spp/empleadores/comisiones_spp/paginas/comision_prima.aspx')
    await asyncio.sleep(3)
    contador=0
    fecha=""
    while True:
        await page.sleep(1)
        html=await page.get_content()
        pos=html.find("lblMes1")
        if pos is not None and pos>-1:
            if fecha!="":
                input_fecha = await page.select('select[id="cboPeriodo"]')
                await input_fecha.send_keys(fecha)
                boton = await page.select('input[id="btnConsultar"]')
                await boton.click()
                await page.sleep(5)
            

            html=await page.get_content()
            pos=html.find("lblMes1")

            posMayor=html.find(">",pos)
            posMenor=html.find("<",posMayor+1)
            fechapantalla=html[posMayor+1:posMenor]
            print(fechapantalla)

            if pos>-1:

                soup=BeautifulSoup(html,'html.parser')
                filas=soup.find_all("tr",class_="JER_filaContenido")
                data=[]
                for fila in filas:
                    tds=fila.find_all("td")
                    filaDatos=[]
                    for td in tds:
                        filaDatos.append( td.get_text().strip())
                    data.append(filaDatos)
                print(data)
                break

        if contador==10:
            
            break
        print("click")
        await page.send(
            uc.cdp.input_.dispatch_mouse_event(
                type_="mousePressed",
                x=391,
                y=285,
                button=MouseButton.LEFT,
                click_count=1
            )
        )
        await page.send(
            uc.cdp.input_.dispatch_mouse_event(
                type_="mouseReleased",
                x=391,
                y=285,
                button=MouseButton.LEFT,
                click_count=1
            )
        )
        contador=contador+1


    browser.stop()

    objData=[]
    for fila in data:
        objData.append({
            "Periodo":fechapantalla,
            "AFP":fila[0],
            "ComisionSobreFlujo":fila[1].replace(",","."),
            "ComisionAnualSobreSaldo":fila[2].replace(",","."),
            "PrimaSeguro":fila[3].replace(",","."),
            "AporteObligatorio":fila[4].replace(",","."),
            "RemuneracionMaxima":fila[5].replace(" ","").replace(",","."),
        })
    print("*"*20)
    print(json.dumps(objData, indent=4, ensure_ascii=False) )


if __name__ == '__main__':
    uc.loop().run_until_complete(main())
