import requests

URLCONSULTADNI="https://csmwebackendprod.stellamaris.com.pe:7981/api/personas/dni/"

def consultarDNI(dni):
    rptaJson={}
    try:

        header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                "x-api-key":"vK9!xQ2@Lm7#Rz4$Tn8%Wp3^Yh6&Cb1*Fj5+Ua0=Ne9?Gs2_Zq7-Hd4~Pc8!Xr3@Mb6#Kt1$Vf5%Jy0^Aw9&Ls2*Eq7+Zc4=Rp8?"}
        sesion=requests.session()

        req=sesion.get(URLCONSULTADNI+dni,headers=header,verify=False)
        print(req.status_code)
        if req.status_code==200:
            rptaJson=req.json()
                       
               
    except Exception as e:
        print("Error "+ str(e))
      
    return rptaJson

if __name__=="__main__":
    print(consultarDNI("00000000"))



