
# CO Consulta NIT - Scraper

Este proyecto es un script en python que automatiza la consulta y extracción de datos del NIT en Colombia, basada en los tutoriales prácticos del canal **[Mabb.Dev](https://www.youtube.com/@mabbdev)**.

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
Asegúrate de instalar los paquetes necesarios que usa el proyecto (requests):
```bash
pip install -r requirement.txt
```

### 3. Configurar la Base de Datos Local
Genera tu archivo de base de datos local ejecuntando las migraciones iniciales de Django:
```bash
python manage.py migrate
```

### 4. Ejecutar script
Inicia el script local de desarrollo:
```bash
python consulta_nit.py
```


---

## 📺 Video Tutorial Paso a Paso

Si quieres ver cómo se programó esta lógica desde cero, cómo se estructuraron las peticiones a la API SRI en línea y cómo se integró con la interfaz de Django, mira el video completo aquí:

▶️ **[Ver Tutorial en YouTube - Mabb.Dev](https://www.youtube.com/watch?v=K6n7V8Px718)**

---
_Desarrollado para la comunidad de desarrolladores de LATAM por Mabb.Dev. ¡No olvides dejar tu ⭐ al repositorio si te sirvió!_
