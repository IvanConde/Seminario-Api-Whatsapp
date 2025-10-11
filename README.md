# WhatsApp Integration Service - Equipo 1

Servicio de integración con WhatsApp usando Meta WhatsApp Cloud API.

## 🚀 Características

- ✅ Webhook receptor para mensajes entrantes (`/webhook/whatsapp`)
- ✅ Validación de token de verificación de Meta
- ✅ Normalización de mensajes a formato estándar
- ✅ Endpoint para envío de mensajes (`/send/whatsapp`)
- ✅ Soporte para texto e imágenes
- ✅ Sistema de logs completo (archivo y consola)
- ✅ Manejo de errores robusto

## 📋 Requisitos

- Python 3.9+
- Poetry (gestor de dependencias)
- Cuenta de Meta Business (para WhatsApp Cloud API)

## 🔧 Instalación

1. **Clonar el repositorio e instalar dependencias:**

```bash
cd tp-seminario
poetry install
```

2. **Configurar variables de entorno:**

Copiar el archivo `.env.example` a `.env` y completar con tus credenciales:

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales de WhatsApp Cloud API:

```env
WHATSAPP_ACCESS_TOKEN=tu_token_de_acceso
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id
WHATSAPP_VERIFY_TOKEN=tu_token_de_verificacion_personalizado
WHATSAPP_BUSINESS_ACCOUNT_ID=tu_business_account_id
```

## 🎯 Cómo obtener credenciales de WhatsApp Cloud API (GRATIS)

Meta ofrece WhatsApp Cloud API **gratis** para desarrollo y testing:

1. **Crear cuenta de Meta for Developers:**
   - Ve a https://developers.facebook.com/
   - Crea una cuenta o inicia sesión

2. **Crear una App:**
   - En el dashboard, click en "Create App"
   - Selecciona "Business" como tipo
   - Completa los detalles de la app

3. **Agregar WhatsApp:**
   - En tu app, busca "WhatsApp" y click en "Set up"
   - Sigue el wizard de configuración

4. **Obtener credenciales:**
   - **Access Token**: En la sección WhatsApp > Getting Started, encontrarás un token temporal (válido 24h). Para producción, genera un token permanente.
   - **Phone Number ID**: En la misma página, verás el "Phone number ID"
   - **Verify Token**: Este lo creas tú (cualquier string), lo usarás para verificar el webhook

5. **Número de prueba:**
   - Meta te da un número de prueba gratis
   - Puedes enviar mensajes a hasta 5 números que agregues como "testers"

## 🏃 Ejecución

### Modo desarrollo:

```bash
poetry run python -m src.whatsapp_service
```

O usando uvicorn directamente:

```bash
poetry run uvicorn src.whatsapp_service:app --reload --host 0.0.0.0 --port 8000
```

El servicio estará disponible en: `http://localhost:8000`

## 📡 Endpoints

### 1. Health Check

```bash
GET /
```

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "WhatsApp Integration Service",
  "timestamp": "2025-10-05T12:00:00"
}
```

### 2. Webhook - Verificación (GET)

```bash
GET /webhook/whatsapp?hub.mode=subscribe&hub.verify_token=tu_token&hub.challenge=123456
```

Este endpoint es llamado por Meta para verificar tu webhook.

### 3. Webhook - Recibir mensajes (POST)

```bash
POST /webhook/whatsapp
```

**Payload de ejemplo (enviado por Meta):**
```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
    "changes": [{
      "value": {
        "messaging_product": "whatsapp",
        "metadata": {
          "display_phone_number": "15551234567",
          "phone_number_id": "PHONE_NUMBER_ID"
        },
        "contacts": [{
          "profile": {
            "name": "Juan"
          },
          "wa_id": "5491112345678"
        }],
        "messages": [{
          "from": "5491112345678",
          "id": "wamid.XXX",
          "timestamp": "1633024800",
          "text": {
            "body": "Hola"
          },
          "type": "text"
        }]
      },
      "field": "messages"
    }]
  }]
}
```

**Mensaje normalizado (formato interno):**
```json
{
  "channel": "whatsapp",
  "sender": "+5491112345678",
  "message": "Hola",
  "timestamp": "2025-10-05T12:00:00",
  "message_id": "wamid.XXX",
  "message_type": "text"
}
```

### 4. Enviar mensaje

```bash
POST /send/whatsapp
```

**Request - Texto:**
```json
{
  "to": "+5491112345678",
  "message": "Hola, este es un mensaje de prueba",
  "message_type": "text"
}
```

**Request - Imagen:**
```json
{
  "to": "+5491112345678",
  "message": "Mira esta imagen",
  "message_type": "image",
  "media_url": "https://ejemplo.com/imagen.jpg"
}
```

**Response:**
```json
{
  "success": true,
  "message_id": "wamid.XXX",
  "details": {
    "messaging_product": "whatsapp",
    "contacts": [{
      "input": "5491112345678",
      "wa_id": "5491112345678"
    }],
    "messages": [{
      "id": "wamid.XXX"
    }]
  }
}
```

## 🧪 Pruebas con cURL

### Enviar mensaje de texto:

```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+5491112345678",
    "message": "Hola desde cURL",
    "message_type": "text"
  }'
```

### Enviar imagen:

```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+5491112345678",
    "message": "Aquí está la imagen",
    "message_type": "image",
    "media_url": "https://picsum.photos/200"
  }'
```

### Verificar webhook:

```bash
curl "http://localhost:8000/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=my_verify_token_123&hub.challenge=test123"
```

## 📝 Colección Postman

Importa esta colección en Postman:

```json
{
  "info": {
    "name": "WhatsApp Integration",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": [""]
        }
      }
    },
    {
      "name": "Send Text Message",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"to\": \"+5491112345678\",\n  \"message\": \"Hola desde Postman\",\n  \"message_type\": \"text\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/send/whatsapp",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["send", "whatsapp"]
        }
      }
    },
    {
      "name": "Webhook Verification",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=my_verify_token_123&hub.challenge=test123",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["webhook", "whatsapp"],
          "query": [
            {
              "key": "hub.mode",
              "value": "subscribe"
            },
            {
              "key": "hub.verify_token",
              "value": "my_verify_token_123"
            },
            {
              "key": "hub.challenge",
              "value": "test123"
            }
          ]
        }
      }
    }
  ]
}
```

## 📊 Logs

Los logs se guardan en:
- **Consola**: Nivel INFO
- **Archivo**: `logs/whatsapp_service_YYYYMMDD.log` (nivel DEBUG)

Ejemplo de log:
```
2025-10-05 12:00:00 - whatsapp_service - INFO - Webhook event received
2025-10-05 12:00:01 - whatsapp_service - INFO - Normalized message: {'channel': 'whatsapp', 'sender': '+5491112345678', 'message': 'Hola', 'timestamp': '2025-10-05T12:00:00'}
2025-10-05 12:00:02 - whatsapp_service - INFO - Sending text message to +5491112345678
2025-10-05 12:00:03 - whatsapp_service - INFO - Message sent successfully to +5491112345678
```

## 🌐 Exponer webhook públicamente

Para que Meta pueda enviar webhooks a tu servidor local, necesitas exponerlo públicamente. Opciones gratuitas:

### Opción 1: ngrok (recomendado)

```bash
# Instalar ngrok
brew install ngrok  # macOS
# o descargar de https://ngrok.com/

# Exponer puerto 8000
ngrok http 8000
```

Obtendrás una URL como: `https://abc123.ngrok.io`

Usa esta URL en la configuración del webhook en Meta: `https://abc123.ngrok.io/webhook/whatsapp`

### Opción 2: localtunnel

```bash
npm install -g localtunnel
lt --port 8000
```

## 🔒 Configurar Webhook en Meta

1. Ve a tu app en Meta for Developers
2. WhatsApp > Configuration
3. En "Webhook", click "Edit"
4. **Callback URL**: `https://tu-url-publica.com/webhook/whatsapp`
5. **Verify Token**: El mismo que pusiste en `.env`
6. Click "Verify and Save"
7. Suscríbete a los eventos: `messages` y `message_status`

## 📁 Estructura del Proyecto

```
tp-seminario/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuración y variables de entorno
│   ├── logger.py              # Sistema de logging
│   ├── models.py              # Modelos de datos (Pydantic)
│   ├── whatsapp_client.py     # Cliente para WhatsApp Cloud API
│   └── whatsapp_service.py    # Servicio principal (FastAPI)
├── logs/                      # Logs generados
├── .env                       # Variables de entorno (no commitear)
├── .env.example              # Ejemplo de variables de entorno
├── .gitignore
├── pyproject.toml            # Dependencias Poetry
└── README.md
```

## 🐛 Troubleshooting

### Error: "Verification token mismatch"
- Verifica que el `WHATSAPP_VERIFY_TOKEN` en `.env` coincida con el configurado en Meta

### Error: "Invalid access token"
- El token temporal expira en 24h, genera un token permanente en Meta
- Verifica que el token esté correctamente en `.env`

### No recibo webhooks
- Verifica que el webhook esté correctamente configurado en Meta
- Asegúrate de que tu URL pública sea accesible
- Revisa los logs en `logs/`

### Error al enviar mensajes
- Verifica que el número de destino esté agregado como "tester" en Meta
- El número debe incluir código de país sin `+` en la API

## 📚 Recursos

- [WhatsApp Cloud API Docs](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Meta for Developers](https://developers.facebook.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

## 👥 Equipo 1

Servicio desarrollado para el TP Seminario - Integración WhatsApp

