# NVVT Backend

Backend del proyecto **NVVT**, desarrollado con **FastAPI** para proporcionar una API robusta y escalable.

## 🚀 Características

- **FastAPI**: Framework moderno y de alto rendimiento para construir APIs
- **Documentación automática**: Swagger UI y ReDoc integrados
- **Validación de datos**: Usando Pydantic para modelos de datos
- **Asíncrono**: Soporte completo para operaciones asíncronas
- **MongoDB**: Base de datos requerida para el proyecto

> Nota:
> Puedes levantar una instancia de MongoDB usando el archivo docker-compose.yaml.

## 📋 Requisitos

- **Python**: 3.10 o superior
- **pip**: Gestor de paquetes de Python
- **Entorno virtual**: Recomendado (`venv` o `virtualenv`)

## ⚙️ Variables de entorno

En el archivo .env.example encontrarás un ejemplo de todas las variables necesarias para ejecutar el proyecto.
Copia este archivo y renómbralo a .env, luego ajusta los valores según tu entorno:

```bash
cp .env.example .env
```

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/santiagoa150/nvvt_backend.git
cd nvvt_backend
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. (Opcional) Levantar MongoDB con Docker

```bash
docker-compose up -d
```

## 🚦 Ejecución

### Servidor de desarrollo

```bash
fastapi dev src/main.py
```

### Servidor de producción

```bash
fastapi run src/main.py
```

## Linter y Formateo de Código

Para mantener un código limpio y consistente, el proyecto incluye configuraciones para Flake8, Black e isort.

Ejecuta los siguientes comandos desde la raíz del proyecto:

```bash
# Linter
flake8 .

# Formateo automático
black .

# Ordenar imports
isort .
```