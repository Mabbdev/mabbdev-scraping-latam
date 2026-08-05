# 🇵🇪 Consulta SOAT - Django Scraper

Este proyecto es una aplicación web desarrollada en **Django** que automatiza la consulta y extracción de datos del SOAT en Perú, basada en los tutoriales prácticos del canal **[Mabb.Dev](https://youtube.com)**.

---

## 🛠️ Requisitos e Instalación

Para ejecutar este scraper de forma local en tu entorno de desarrollo, sigue estos pasos:

### 1. Preparar el Entorno Virtual
Crea y activa un entorno virtual de Python dentro de esta carpeta para evitar conflictos de librerías:
```bash
python -m venv venv
```
* **En Windows:**
  ```bash
  .\venv\Scripts\activate
  ```
* **En Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```

### 2. Instalar Dependencias
Asegúrate de instalar los paquetes necesarios que usa el proyecto (Django, requests, noDriver, etc.):
```bash
pip install -r requirements.txt
```

### 3. Configurar la Base de Datos Local
Genera tu archivo de base de datos local ejecuntando las migraciones iniciales de Django:
```bash
python manage.py migrate
```

### 4. Desplegar el Servidor
Inicia el servidor local de desarrollo:
```bash
python manage.py runserver
```

Ahora abre tu navegador e ingresa a: **`http://127.0.0`**

---

## 📺 Video Tutorial Paso a Paso

Si quieres ver cómo se programó esta lógica desde cero, cómo se estructuraron las peticiones a las entidades del SOAT y cómo se integró con la interfaz de Django, mira el video completo aquí:

▶️ **[Ver Tutorial en YouTube - Mabb.Dev](https://www.youtube.com/watch?v=7SZ3pNPOTy4)**

---
_Desarrollado para la comunidad de desarrolladores de LATAM por Mabb.Dev. ¡No olvides dejar tu ⭐ al repositorio si te sirvió!_
