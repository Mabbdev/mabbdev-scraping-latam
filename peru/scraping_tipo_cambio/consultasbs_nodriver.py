import asyncio
import nodriver as uc
from nodriver import cdp
from nodriver.cdp.input_ import MouseButton
from bs4 import BeautifulSoup
from nodriver.cdp.input_ import MouseButton
import pyodbc
from datetime import datetime

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
    page = await browser.get('https://www.sbs.gob.pe/app/pp/sistip_portal/paginas/publicacion/tipocambiopromedio.aspx')
    await asyncio.sleep(3)
    contador=0
    fecha=""
    while True:
        await page.sleep(1)
        html=await page.get_content()
        pos=html.find("ctl00_cphContent_lblFecha")
        if pos is not None and pos>-1:
            if fecha!="":
                input_fecha = await page.select('input[id="ctl00_cphContent_rdpDate_dateInput"]')
                await input_fecha.send_keys(fecha)
            

                await page.sleep(1)
                await page.send(
                            uc.cdp.input_.dispatch_mouse_event(
                                type_="mousePressed",
                                x=534,
                                y=170,
                                button=MouseButton.LEFT,
                                click_count=1
                            )
                        )
                await page.send(
                    uc.cdp.input_.dispatch_mouse_event(
                        type_="mouseReleased",
                        x=534,
                        y=170,
                        button=MouseButton.LEFT,
                        click_count=1
                    )
                )

                await page.send(
                            uc.cdp.input_.dispatch_mouse_event(
                                type_="mousePressed",
                                x=534,
                                y=170,
                                button=MouseButton.LEFT,
                                click_count=1
                            )
                        )
                await page.send(
                    uc.cdp.input_.dispatch_mouse_event(
                        type_="mouseReleased",
                        x=534,
                        y=170,
                        button=MouseButton.LEFT,
                        click_count=1
                    )
                )
                await page.sleep(5)
            

            
            html=await page.get_content()
            pos=html.find("ctl00_cphContent_lblFecha")

            posMayor=html.find(">",pos)
            posMenor=html.find("<",posMayor+1)
            fechapantalla=html[posMayor+1:posMenor]
            print(fechapantalla)

            pos=html.find("ctl00_cphContent_rgTipoCambio")
            if pos>-1:
                postable=html.find("<table",pos)
                postablefin=html.find("</table>",postable)
                tabla=html[postable:postablefin+8]
                soup=BeautifulSoup(tabla,'html.parser')
                trs=soup.find_all("tr")
                data=[]
                for tr in trs:
                    tds=tr.find_all("td")
                    fila=[]
                    for td in tds:
                        fila.append( td.get_text())
                    if len(fila)>0:
                        data.append(fila)
                

            break



        if contador==10:
            break
        contador=contador+1
    browser.stop()

    afecha=fechapantalla.split(" ")
    listaTipoCambio=[]
    fechaactual=datetime.now().strftime("%Y-%m-%d")
    if len(afecha)==5:
        obj={"fechaPantalla":afecha[4]}
        for fila in data:
            if fila[0]=="Dólar de N.A.":
                obj["DOLAR"]=fila[1]+"|"+fila[2]
                listaTipoCambio.append(fechaactual+"¦USD¦"+fila[1]+"¦"+fila[2])
            if fila[0]=="Euro":
                obj["EURO"]=fila[1]+"|"+fila[2]
                listaTipoCambio.append(fechaactual+"¦XEU¦"+fila[1]+"¦"+fila[2])
    print(obj)
    print(listaTipoCambio)
    rpta=ejecutarComando("uspTipoCambioBacheroGrabar","lstparametros","¬".join(listaTipoCambio),True)
    print("*"*20)
    print(rpta)
    

if __name__ == '__main__':
    uc.loop().run_until_complete(main())
