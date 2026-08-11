# 🇵🇪 Consulta Luna polarizada - Django Scraper

Este proyecto es una aplicación web desarrollada en **Django** que automatiza la consulta y extracción de datos de lunas polarizadas en Perú, sígueme en mi canal **[Mabb.Dev](https://www.youtube.com/@mabbdev)**.

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


---
_Desarrollado para la comunidad de desarrolladores de LATAM por Mabb.Dev. ¡No olvides dejar tu ⭐ al repositorio si te sirvió!_
