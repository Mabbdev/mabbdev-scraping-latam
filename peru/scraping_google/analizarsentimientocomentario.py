import os
import pandas as pd
from transformers import pipeline

# Silenciar advertencias de inicialización
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# 1. Cargar el pipeline con el modelo optimizado para español informal
model_name = "pysentimiento/robertuito-sentiment-analysis"
sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)

data=pd.read_excel("Data_YAPE.xlsx")

comentarios=data["Comentario"].to_list()

predicciones=sentiment_pipeline(comentarios)

resultados=[]

for comentario,prediccion in zip(comentarios,predicciones):
    resultados.append({"comentario":comentario,
                       "Sentimiento": prediccion["label"],
             "Confianza": round(prediccion["score"], 4)

    })

df=pd.DataFrame(resultados)

mapa_etiquetas = {"POS": "Positivo", "NEG": "Negativo", "NEU": "Neutral"}
df["Sentimiento"] = df["Sentimiento"].map(mapa_etiquetas)

df.to_excel("analisis_sentimiento_app_yape.xlsx",index=False)
print("print termino de procesar")
