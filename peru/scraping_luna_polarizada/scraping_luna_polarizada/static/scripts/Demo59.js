window.onload=function(){

    let btnProcesar=document.getElementById("btnProcesar");
    btnProcesar.onclick=function(){

         let txtFecha=document.getElementById("txtIdentificador").value;

        let fd=new FormData();
        fd.append("data",txtFecha);
        servidor({url:"procesar",data:fd,responsetype:"json"}).then((data)=>{

            document.getElementById("txtPre").innerHTML=JSON.stringify(data,null,2);

        });
    }
}


function servidor({ metodo = "post", url = null, data = null, responsetype = "text" } = {}) {

    return new Promise((resolve, reject) => {
        let divLoading=document.getElementById("divLoading");
        if(divLoading){
            divLoading.classList.remove("hide");
        }

        let xhr = new XMLHttpRequest();
        xhr.open(metodo, url);
        var csrftoken=document.getElementsByName("csrfmiddlewaretoken")[0].value;
        xhr.setRequestHeader("X-CSRFToken", csrftoken);

        xhr.responseType = responsetype;
        xhr.onreadystatechange = function () {

            if (xhr.readyState == 4 && xhr.status == 200) {
                divLoading.classList.add("hide");

                resolve(xhr.response);
            }
        }
        xhr.onerror = function (e) {
            reject(e)
        }

        xhr.send(data);
    });
}
