import requests
requests.packages.urllib3.disable_warnings()

def consultaNit(nit):
    rpta=None
    try:
        header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"}
        URLCONSULTANITCOLOMBIA="https://rulex.org/api/data/public/rues"
        req=requests.get(URLCONSULTANITCOLOMBIA+"?nit="+nit,headers=header)
        if req.status_code==200:
            obj=req.json()
            if "ok" in obj and obj["ok"]:
                resultado=obj["resultados"][0]
                rpta={"razonsocial":resultado["razon_social"],
                      "camaracomercio":resultado["camara_comercio"],
                      "matricula":resultado["matricula"][0:3]+"*****",
                      "codigoactividad":resultado["cod_ciiu_act_econ_pri"],
                      "tiposociedad":resultado["tipo_sociedad"],
                      "organizacionjuridica":resultado["organizacion_juridica"],
                      "estado":resultado["estado_matricula"],
                      }
    except Exception as e:
        print("Error "+ str(e))
    return rpta


if __name__=="__main__":
    print(consultaNit("000000000"))