# NVVT Backend

Backend del proyecto **NVVT**, desarrollado con **FastAPI** para proporcionar una API robusta y escalable.

## 🚀 Características

- **FastAPI**: Framework moderno y de alto rendimiento para construir APIs
- **Documentación automática**: Swagger UI y ReDoc integrados
- **Validación de datos**: Usando Pydantic para modelos de datos
- **Asíncrono**: Soporte completo para operaciones asíncronas

## 📋 Requisitos

- **Python**: 3.10 o superior
- **pip**: Gestor de paquetes de Python
- **Entorno virtual**: Recomendado (`venv` o `virtualenv`)

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

## 🚦 Ejecución

### Servidor de desarrollo
```bash
fastapi dev src/main.py
```

### Servidor de producción
```bash
fastapi run src/main.py
```