# 🤖 Chatbot Pro con IA (Django + OpenAI)

Chatbot web desarrollado con **Django 5** y la API de **OpenAI**, con historial de conversación, control de tokens y una interfaz moderna.  
Pensado para ser fácilmente desplegable en **Render** y personalizable para distintos casos de uso.

---

## ✨ Características

- **Historial en sesión** para mantener el contexto en la conversación.
- **Prompt de sistema** configurable para definir la personalidad del bot.
- **Contador de tokens** (entrada, salida y total).
- **UI limpia** con indicador "escribiendo...".
- Configuración mediante `.env` (sin claves en el código).
- Preparado para **deploy en Render** y subdominio personalizado.

---

## 📂 Estructura de carpetas
``
chatbot-pro-ia/
│
├── core/ # Proyecto principal de Django
├── chat/ # App del chatbot
├── templates/ # HTML (index.html)
├── static/ # CSS y JS
├── .env # Variables de entorno (no subir)
├── requirements.txt # Dependencias
└── Procfile # Configuración para Render
``

---

## ⚙️ Instalación y uso en local

1. **Clonar el repositorio**

git clone https://github.com/tu-usuario/chatbot-pro-ia.git
cd chatbot-pro-ia

Crear y activar entorno virtual

python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

Instalar dependencias

pip install -r requirements.txt
Configurar variables de entorno

Crea el archivo .env y completa los valores:

DEBUG=True
SECRET_KEY=django-insecure-tu_clave
OPENAI_API_KEY=sk-tu_api_key
OPENAI_MODEL=gpt-4o-mini
ALLOWED_HOSTS=127.0.0.1,localhost

Migrar y ejecutar servidor

python manage.py migrate
python manage.py runserver

Abrir en http://127.0.0.1:8000

🚀 Deploy en Render
Subir el proyecto a GitHub.

Crear un nuevo servicio web en Render y conectar el repo.

Configuración en Render:

Build command: pip install -r requirements.txt

Start command: gunicorn core.wsgi:application --preload

Variables de entorno en Render:

DEBUG=False
SECRET_KEY=django-insecure-tu_clave
OPENAI_API_KEY=sk-tu_api_key
OPENAI_MODEL=gpt-4o-mini
ALLOWED_HOSTS=.onrender.com,.tudominio.com
CSRF_TRUSTED_ORIGINS=https://*.onrender.com,https://*.tudominio.com

Opcional: configurar subdominio (ej. chat.tudominio.com).

🛠 Tecnologías utilizadas

Django 5

OpenAI Python SDK

HTML5, CSS3, JavaScript (fetch API)

Gunicorn para producción

Render para despliegue

📄 Licencia
Este proyecto se distribuye bajo la licencia MIT. Eres libre de usarlo y modificarlo.

✍️ Desarrollado por: Ire
