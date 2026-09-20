import requests
import time

def procesar(datarucs):
    rucs=datarucs.split("|")
    rucs=rucs[0:20]
    lista=[]

    for ruc in rucs:
        url="https://srienlinea.sri.gob.ec/sri-catastro-sujeto-servicio-internet/rest/ConsolidadoContribuyente/obtenerPorNumerosRuc?ruc="+ruc

        req=requests.get(url)
        if req.status_code==200:
            rptaJson=req.json()
            if rptaJson is not None and len(rptaJson)>0:
                rucconsulta=rptaJson[0]
                lista.append({"ruc":rucconsulta["numeroRuc"][0:5]+"*****",
                              "nombre":rucconsulta["razonSocial"],
                            "estado":rucconsulta["estadoContribuyenteRuc"],
                            "retencion":rucconsulta["agenteRetencion"]})
        time.sleep(1.5)
                

    return lista


if __name__=="__main__":
    print(procesar("1790010937001"))


