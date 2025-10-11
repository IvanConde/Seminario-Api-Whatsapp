# 🟢 Equipo 1 – WhatsApp Integration

## 📦 Entregables Completados

### ✅ Archivos Principales

1. **`src/whatsapp_service.py`** - Servicio principal con FastAPI
   - Webhook receptor (`/webhook/whatsapp`)
   - Endpoint de envío (`/send/whatsapp`)
   - Validación de token de Meta
   - Normalización de mensajes

2. **`src/whatsapp_client.py`** - Cliente para WhatsApp Cloud API
   - Envío de mensajes de texto
   - Envío de imágenes
   - Manejo de errores

3. **`src/models.py`** - Modelos de datos (Pydantic)
   - NormalizedMessage (formato estándar)
   - SendMessageRequest/Response
   - Validación automática

4. **`src/config.py`** - Configuración y variables de entorno

5. **`src/logger.py`** - Sistema de logging
   - Logs en consola (INFO)
   - Logs en archivo (DEBUG)
   - Rotación diaria

### 📚 Documentación

- **`README.md`** - Documentación completa del proyecto
- **`QUICKSTART.md`** - Guía rápida de inicio
- **`DOCUMENTACION_ENDPOINTS.md`** - Documentación detallada de endpoints
- **`POSTMAN_COLLECTION.json`** - Colección de Postman para pruebas

### 🧪 Testing

- **`tests/test_whatsapp_service.py`** - Tests básicos
- **`test_service.py`** - Script de prueba automática

### 🚀 Scripts de Ejecución

- **`run.sh`** - Script para ejecutar el servicio fácilmente
- **`.env`** - Variables de entorno (con valores demo)
- **`pyproject.toml`** - Dependencias con Poetry

---

## 🎯 Funcionalidades Implementadas

### ✅ Webhook Receptor (`/webhook/whatsapp`)

- **GET**: Validación de token de verificación de Meta
- **POST**: Recepción de mensajes entrantes y status updates
- Normalización automática a formato estándar:
  ```json
  {
    "channel": "whatsapp",
    "sender": "+54911...",
    "message": "Hola",
    "timestamp": "2025-10-05T12:00:00"
  }
  ```

### ✅ Endpoint de Envío (`/send/whatsapp`)

- Envío de mensajes de texto
- Envío de imágenes con caption
- Validación de parámetros
- Respuestas estructuradas con `message_id`

### ✅ Sistema de Logs

- Logs en consola (nivel INFO)
- Logs en archivo: `logs/whatsapp_service_YYYYMMDD.log` (nivel DEBUG)
- Registro de todos los eventos (mensajes recibidos, enviados, errores)

### ✅ Manejo de Errores

- Validación de tokens
- Manejo de timeouts
- Respuestas estructuradas de error
- Logs detallados de errores

---

## 🚀 Cómo Ejecutar

### Opción 1: Script de ejecución

```bash
./run.sh
```

### Opción 2: Comando directo

```bash
poetry install
poetry run python -m src.whatsapp_service
```

### Opción 3: Con uvicorn

```bash
poetry run uvicorn src.whatsapp_service:app --reload --host 0.0.0.0 --port 8000
```

El servicio estará disponible en: **http://localhost:8000**

---

## 🧪 Ejemplos de Prueba

### 1. Health Check

```bash
curl http://localhost:8000/
```

### 2. Verificar Webhook

```bash
curl "http://localhost:8000/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=my_verify_token_123&hub.challenge=test123"
```

### 3. Enviar Mensaje de Texto

```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+5491112345678",
    "message": "Hola desde cURL",
    "message_type": "text"
  }'
```

### 4. Enviar Imagen

```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+5491112345678",
    "message": "Aquí está la imagen",
    "message_type": "image",
    "media_url": "https://picsum.photos/400/300"
  }'
```

### 5. Simular Mensaje Entrante

```bash
curl -X POST "http://localhost:8000/webhook/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "object": "whatsapp_business_account",
    "entry": [{
      "id": "123456",
      "changes": [{
        "value": {
          "messaging_product": "whatsapp",
          "metadata": {
            "display_phone_number": "15551234567",
            "phone_number_id": "PHONE_ID"
          },
          "contacts": [{
            "profile": {"name": "Test"},
            "wa_id": "5491112345678"
          }],
          "messages": [{
            "from": "5491112345678",
            "id": "wamid.test123",
            "timestamp": "1633024800",
            "text": {"body": "Hola"},
            "type": "text"
          }]
        },
        "field": "messages"
      }]
    }]
  }'
```

---

## 🔑 Configuración de WhatsApp Cloud API (GRATIS)

### Paso 1: Crear cuenta en Meta for Developers

1. Ve a: https://developers.facebook.com/
2. Crea una cuenta o inicia sesión
3. Crea una nueva App (tipo "Business")

### Paso 2: Agregar WhatsApp

1. En tu app, busca "WhatsApp" y haz click en "Set up"
2. Sigue el wizard de configuración

### Paso 3: Obtener credenciales

En "WhatsApp" → "Getting Started":

- **Access Token**: Token temporal (24h) o genera uno permanente
- **Phone Number ID**: ID del número de prueba
- **Verify Token**: Créalo tú (cualquier string)

### Paso 4: Actualizar `.env`

```env
WHATSAPP_ACCESS_TOKEN=tu_token_aqui
WHATSAPP_PHONE_NUMBER_ID=tu_phone_id_aqui
WHATSAPP_VERIFY_TOKEN=mi_token_secreto_123
```

### Paso 5: Agregar número de prueba

- Agrega tu número personal como "tester"
- Recibirás un código de verificación por WhatsApp
- Ahora puedes enviar mensajes a ese número

### Paso 6: Exponer webhook públicamente

**Usando ngrok (recomendado):**

```bash
ngrok http 8000
```

Obtendrás una URL como: `https://abc123.ngrok.io`

**Configurar en Meta:**

1. WhatsApp → Configuration → Webhook
2. **Callback URL**: `https://abc123.ngrok.io/webhook/whatsapp`
3. **Verify Token**: El mismo que pusiste en `.env`
4. Suscríbete a: `messages` y `message_status`

---

## 📊 Estructura del Proyecto

```
tp-seminario/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuración
│   ├── logger.py              # Sistema de logging
│   ├── models.py              # Modelos de datos
│   ├── whatsapp_client.py     # Cliente API
│   └── whatsapp_service.py    # Servicio principal
├── tests/
│   ├── __init__.py
│   └── test_whatsapp_service.py
├── logs/                      # Logs generados
├── .env                       # Variables de entorno
├── .gitignore
├── pyproject.toml            # Dependencias Poetry
├── run.sh                    # Script de ejecución
├── test_service.py           # Script de pruebas
├── README.md                 # Documentación completa
├── QUICKSTART.md             # Guía rápida
├── DOCUMENTACION_ENDPOINTS.md # Docs de endpoints
└── POSTMAN_COLLECTION.json   # Colección Postman
```

---

## 📡 Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/webhook/whatsapp` | Verificación webhook (Meta) |
| POST | `/webhook/whatsapp` | Recibir mensajes |
| POST | `/send/whatsapp` | Enviar mensajes |
| GET | `/docs` | Documentación interactiva (Swagger) |
| GET | `/redoc` | Documentación alternativa (ReDoc) |

---

## 🔒 Características de Seguridad

- ✅ Validación de token de verificación
- ✅ Validación de parámetros con Pydantic
- ✅ Manejo seguro de errores
- ✅ Variables de entorno para credenciales
- ✅ Logs detallados para auditoría

---

## 📝 Formato de Mensaje Normalizado

Todos los mensajes entrantes se convierten automáticamente a este formato estándar:

```json
{
  "channel": "whatsapp",
  "sender": "+5491112345678",
  "message": "Contenido del mensaje",
  "timestamp": "2025-10-05T12:00:00",
  "message_id": "wamid.XXX",
  "message_type": "text"
}
```

**Tipos de mensaje soportados:**
- `text` - Mensaje de texto
- `image` - Imagen con caption
- `audio` - Mensaje de audio
- `video` - Video
- `document` - Documento

---

## 💰 Costos - 100% GRATIS para Desarrollo

**WhatsApp Cloud API - Free Tier:**
- ✅ 1,000 conversaciones gratis por mes
- ✅ Número de prueba incluido
- ✅ Hasta 5 números de prueba
- ✅ Sin tarjeta de crédito requerida para empezar

**Herramientas gratuitas:**
- ✅ ngrok: Plan gratuito disponible
- ✅ Poetry: Open source
- ✅ FastAPI: Open source
- ✅ Python: Open source

---

## 🐛 Troubleshooting

### Error: "Verification token mismatch"
➡️ Verifica que el token en `.env` coincida con el configurado en Meta

### Error: "Invalid access token"
➡️ El token temporal expira en 24h, genera uno permanente

### No recibo webhooks
➡️ Verifica que ngrok esté corriendo
➡️ Verifica la configuración del webhook en Meta
➡️ Revisa los logs en `logs/`

### Error al enviar mensajes
➡️ Verifica que el número esté agregado como "tester"
➡️ El número debe tener formato: `+5491112345678`

---

## 📚 Recursos Adicionales

- [WhatsApp Cloud API Docs](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Meta for Developers](https://developers.facebook.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)

---

## ✅ Checklist de Entrega

- [x] Webhook receptor configurado (`/webhook/whatsapp`)
- [x] Validación de token de Meta
- [x] Recepción de mensajes entrantes
- [x] Recepción de status updates
- [x] Normalización a formato estándar
- [x] Endpoint de envío (`/send/whatsapp`)
- [x] Soporte para texto
- [x] Soporte para imágenes
- [x] Sistema de logs (archivo y consola)
- [x] Manejo de errores robusto
- [x] Documentación completa
- [x] Ejemplos de request/response
- [x] Colección de Postman
- [x] Scripts de prueba con cURL
- [x] Tests automatizados
- [x] Uso de Poetry para dependencias
- [x] API gratuita (WhatsApp Cloud API)

---

## 👥 Equipo 1

**Proyecto:** TP Seminario - WhatsApp Integration  
**Tecnologías:** Python 3.9+, FastAPI, Poetry, WhatsApp Cloud API  
**Estado:** ✅ Completado y funcional

