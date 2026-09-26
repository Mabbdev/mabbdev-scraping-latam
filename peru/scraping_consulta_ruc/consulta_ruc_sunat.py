
import curl_cffi
from bs4 import BeautifulSoup


def buscarRUC(ruc):
    dtRuc={}

    try:
                
        URLCONSULTARUC="https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"
        payload={
        'accion':'consPorRuc',
        'razSoc':'',
        'nroRuc': ruc,
        'nrodoc': '',
        'token': '123',
        'contexto': 'ti-it',
        'modo': '1',
        'rbtnTipo': '1',
        'search1': ruc,
        'tipdoc':'1',
        'search2': '',
        'search3': '',
        'codigo': ''
        }


        req=curl_cffi.post(URLCONSULTARUC,data=payload,impersonate="chrome")
        print(req.status_code)
        if req.status_code==200:
            html=req.text
            soup=BeautifulSoup(html,'html.parser')
            items=soup.find_all("div",class_="list-group-item")

            for i,item in enumerate(items):
                fila=str(item)
                posClave = fila.find("list-group-item-heading")
                if posClave > -1:
                    posMayor = fila.find(">", posClave)
                    if posMayor > -1:
                        posMenor = fila.find("<", posMayor)

                        clave = fila[posMayor + 1: posMenor ]
                        if i <= 1:
                            posClave = fila.find("list-group-item-heading", posMenor)
                        else:
                            posClave = fila.find("list-group-item-text", posMenor)
                        if posClave > -1:
                            posMayor = fila.find(">", posClave)
                            posMenor = fila.find("<", posMayor)
                            valor = fila[posMayor + 1: posMenor ]
                            clave = clave.replace(":", "").replace(" ", "_").replace("í", "i").replace("ó", "o").replace("ú", "u")
                            dtRuc[clave]= valor.strip()
                            posClave = fila.find("list-group-item-heading", posMenor)
                            if posClave > -1:
                                posMayor = fila.find(">", posClave)
                                if posMayor > -1:
                                    posMenor = fila.find("<", posMayor)
                                    clave = fila[posMayor + 1: posMenor]
                                    posClave = fila.find("list-group-item-text", posMenor)
                                    posMayor = fila.find(">", posClave)
                                    posMenor = fila.find("<", posMayor)
                                    valor = fila[posMayor + 1: posMenor ]
                                    clave = clave.replace(":", "").replace(" ", "_").replace("í", "i").replace("ó", "o").replace("ú", "u")
                                    dtRuc[clave]= valor.replace("    ","").strip()
                        else:
                            posClave = fila.find("tblResultado", posMenor)
                            if posClave > -1:
                                htmlTabla = fila[posClave: len(fila) ]
                                detalle=[]
                                trs = htmlTabla.split("<tr>")
                                ntr=len(trs)
                                postd = -1
                                postdd = -1
                                for j in range(ntr):
                                    postd = trs[j].find("<td>")
                                    if postd > -1:
                                        postdd = trs[j].find("<", postd + 1)
                                        detalle.append(trs[j][postd + 4: postdd ])
                                valor = ",".join(detalle)
                                clave = clave.replace(":", "").replace(" ", "_").replace("í", "i").replace("ó", "o").replace("ú", "u")


    except Exception as e:
        print("Error "+ str(e))
    return dtRuc




if __name__=="__main__":
    print(buscarRUC("20100364451"))