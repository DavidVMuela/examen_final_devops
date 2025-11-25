# 🚀 Proyecto CI/CD Flask + IA

Proyecto completo de Integración y Entrega Continua (CI/CD) con Flask, IA (Claude API) y despliegue automatizado.

## 📋 Descripción

Aplicación web desarrollada con Flask que integra la API de Claude (Anthropic) para procesamiento de lenguaje natural, con pipeline completo de CI/CD implementado mediante GitHub Actions, contenedorización con Docker y despliegue automatizado en VPS.

## 🏗️ Arquitectura

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   GitHub    │───▶│GitHub Actions│───▶│   GHCR      │
│  Repository │    │   Pipeline   │    │  Packages   │
└─────────────┘    └──────────────┘    └─────────────┘
                           │                    │
                           │                    ▼
                           │            ┌─────────────┐
                           └───────────▶│  VPS Server │
                                        │   Docker    │
                                        └─────────────┘
                                               │
                                               ▼
                                    [apellido].byronrm.com
```

## 🛠️ Tecnologías

- **Backend**: Flask 3.0.0
- **IA**: Anthropic Claude API
- **Contenedorización**: Docker
- **CI/CD**: GitHub Actions
- **Registry**: GitHub Container Registry (GHCR)
- **Orquestación**: Docker Swarm
- **Proxy Reverso**: Traefik
- **Testing**: pytest

## 📦 Estructura del Proyecto

```
.
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # Pipeline de CI/CD
├── app.py                     # Aplicación Flask principal
├── test_app.py                # Tests automatizados
├── requirements.txt           # Dependencias Python
├── Dockerfile                 # Imagen Docker
├── docker-compose.yml         # Stack para despliegue
├── .gitignore
└── README.md
```

## 🚦 Pipeline CI/CD

### 1️⃣ **Test** (Integración Continua)
- Checkout del código
- Setup de Python 3.11
- Instalación de dependencias
- Ejecución de tests con pytest

### 2️⃣ **Build & Push** (Construcción)
- Login a GitHub Container Registry
- Build de imagen Docker
- Tag con versión 1.0.5
- Push a GHCR

### 3️⃣ **Deploy** (Entrega Continua)
- Conexión SSH al VPS
- Pull de nueva imagen
- Actualización del servicio
- Limpieza de imágenes antiguas

## 🧪 Tests Automatizados

```bash
pytest test_app.py -v
```

Los tests validan:
- ✅ Carga correcta de la página principal
- ✅ Endpoint de health check
- ✅ Endpoint de API (con/sin prompt)
- ✅ Versión correcta (1.0.5)

## 🐳 Construcción Local

```bash
# Build
docker build -t [apellido]:1.0.5 .

# Run
docker run -p 5000:5000 -e ANTHROPIC_API_KEY=tu_api_key [apellido]:1.0.5
```

## 🌐 Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Interfaz web principal |
| `/health` | GET | Health check del servicio |
| `/api/chat` | POST | Endpoint de consulta a IA |

## 🔧 Configuración

### Secrets de GitHub

Configurar en: `Settings > Secrets and variables > Actions`

- `VPS_HOST`: IP o dominio del VPS
- `VPS_USERNAME`: Usuario SSH del VPS
- `VPS_SSH_KEY`: Clave privada SSH
- `GITHUB_TOKEN`: Token automático (ya incluido)

### Variables de Entorno

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx  # API key de Claude (opcional)
```

## 📝 Instrucciones de Uso

### 1. Crear Repositorio

```bash
git init
git add .
git commit -m "Initial commit: Flask AI CI/CD project"
git branch -M [APELLIDO]
git remote add origin https://github.com/[USUARIO]/[REPO].git
git push -u origin [APELLIDO]
```

### 2. Configurar Secrets

Ir a `Settings > Secrets and variables > Actions` y añadir:
- VPS_HOST
- VPS_USERNAME
- VPS_SSH_KEY

### 3. Personalizar Archivos

Reemplazar en todos los archivos:
- `[APELLIDO]` → tu segundo apellido
- `[USUARIO]` → tu usuario de GitHub
- `/path/to/stack/[APELLIDO]` → ruta del stack en VPS

### 4. Preparar VPS

```bash
# Crear directorio del stack
mkdir -p /path/to/stack/[apellido]
cd /path/to/stack/[apellido]

# Copiar docker-compose.yml personalizado
# Inicializar el stack
docker stack deploy -c docker-compose.yml [apellido]
```

### 5. Configurar DNS

Crear registro A en DNS apuntando:
```
[apellido].byronrm.com → IP_DEL_VPS
```

### 6. Hacer Push para Activar Pipeline

```bash
git add .
git commit -m "feat: configure CI/CD pipeline"
git push origin [APELLIDO]
```

## 🎯 Resultado Esperado

Después del push:
1. ✅ Tests ejecutados y pasados
2. ✅ Imagen construida y publicada en GHCR
3. ✅ Despliegue automático en VPS
4. ✅ Aplicación accesible en `[apellido].byronrm.com`

## 🔍 Verificación

```bash
# Ver imagen en GHCR
https://github.com/[USUARIO]?tab=packages

# Verificar servicio en VPS
docker service ls | grep [apellido]

# Ver logs
docker service logs [apellido]_app

# Test del health endpoint
curl https://[apellido].byronrm.com/health
```

## 📊 Versión

**Versión Actual**: 1.0.5

## 👤 Autor

[Tu Nombre] - [Segundo Apellido]

## 📄 Licencia

Proyecto educativo para evaluación de CI/CD