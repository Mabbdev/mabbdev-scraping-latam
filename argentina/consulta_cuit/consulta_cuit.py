
import urllib.request as req
import json


def buscarEmpresa(cuit):

    rptaJson=None

    try:
        URLEMPRESAaRGENTINA="https://www.argentina.gob.ar/justicia/registro-nacional-sociedades?cuit=@CUIT&razon="
        headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"}
        url=URLEMPRESAaRGENTINA.replace("@CUIT",cuit)

        _request=req.Request(url,method='GET',headers=headers)
        with req.urlopen(_request) as r:
            if  r.status==200:
                html=r.read().decode("utf-8")
        posData=html.find("allItems")
        if posData>-1:
            posllaveapertura=html.find("{",posData)
            posllavecierre=html.find("}",posllaveapertura)
            data=html[posllaveapertura:posllavecierre+1]
            ojson=json.loads(data)
            rptaJson={"razonSocial":ojson["razon_social"][0:3]+"*******",
            "tipoSociedad":ojson["tipo_societario"],
            "domiciliofiscal":ojson["df_calle"][0:3]+"**** "+ojson["df_numero"]+" "+ojson["df_localidad"][0:3]+"*****",
            "provincia":ojson["df_provincia"],
            "fechaContrato":"**-**-"+ojson["fecha_contrato_social"][6:],
            "estadodomicilio":ojson["dl_estado_domicilio"],
            "codigoPostal":ojson["df_cp"],
            "actividades":ojson["desc_actividad"]
            }

    except Exception as e:
        print("Error "+ str(e))
      
    return rptaJson


if __name__=="__main__":
    print(buscarEmpresa("00000000"))