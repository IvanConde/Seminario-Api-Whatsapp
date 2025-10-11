# 📡 Documentación de Endpoints - WhatsApp Integration

## Base URL
```
http://localhost:8000
```

---

## 1. Health Check

**Endpoint:** `GET /`

**Descripción:** Verifica que el servicio esté funcionando correctamente.

**Request:**
```bash
curl http://localhost:8000/
```

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "WhatsApp Integration Service",
  "timestamp": "2025-10-05T12:00:00.000000"
}
```

---

## 2. Webhook - Verificación

**Endpoint:** `GET /webhook/whatsapp`

**Descripción:** Endpoint de verificación usado por Meta para validar tu webhook. Meta llama este endpoint con parámetros específicos para confirmar que tu servidor es legítimo.

**Query Parameters:**
- `hub.mode` (string, required): Debe ser "subscribe"
- `hub.verify_token` (string, required): Tu token de verificación personalizado
- `hub.challenge` (string, required): Challenge enviado por Meta

**Request:**
```bash
curl "http://localhost:8000/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=my_verify_token_123&hub.challenge=test_challenge_123"
```

**Response:** `200 OK`
```
test_challenge_123
```

**Error Response:** `403 Forbidden`
```json
{
  "detail": "Verification token mismatch"
}
```

**Notas:**
- El `verify_token` debe coincidir con el configurado en `.env`
- Meta espera que devuelvas exactamente el `challenge` que envió
- Este endpoint solo se llama una vez durante la configuración inicial

---

## 3. Webhook - Recibir Mensajes

**Endpoint:** `POST /webhook/whatsapp`

**Descripción:** Recibe eventos de WhatsApp (mensajes entrantes, actualizaciones de estado, etc.) enviados por Meta.

**Headers:**
```
Content-Type: application/json
```

**Request Body (ejemplo de mensaje de texto):**
```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15551234567",
              "phone_number_id": "PHONE_NUMBER_ID"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Juan Pérez"
                },
                "wa_id": "5491112345678"
              }
            ],
            "messages": [
              {
                "from": "5491112345678",
                "id": "wamid.HBgNNTQ5MTE1NTU1NTU1NRUCABIYFjNFQjBDMDhGRDFFMDRGRTRBMDk2AA==",
                "timestamp": "1633024800",
                "text": {
                  "body": "Hola, necesito información"
                },
                "type": "text"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

**Request Body (ejemplo de mensaje con imagen):**
```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15551234567",
              "phone_number_id": "PHONE_NUMBER_ID"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Juan Pérez"
                },
                "wa_id": "5491112345678"
              }
            ],
            "messages": [
              {
                "from": "5491112345678",
                "id": "wamid.XXX",
                "timestamp": "1633024800",
                "type": "image",
                "image": {
                  "caption": "Mira esta foto",
                  "mime_type": "image/jpeg",
                  "sha256": "...",
                  "id": "IMAGE_ID"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

**Request Body (ejemplo de status update):**
```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15551234567",
              "phone_number_id": "PHONE_NUMBER_ID"
            },
            "statuses": [
              {
                "id": "wamid.XXX",
                "status": "delivered",
                "timestamp": "1633024800",
                "recipient_id": "5491112345678"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

**Response:** `200 OK`
```json
{
  "status": "ok"
}
```

**Formato Normalizado Interno:**

El servicio convierte automáticamente los mensajes al siguiente formato estándar:

```json
{
  "channel": "whatsapp",
  "sender": "+5491112345678",
  "message": "Hola, necesito información",
  "timestamp": "2021-10-01T00:00:00",
  "message_id": "wamid.HBgNNTQ5MTE1NTU1NTU1NRUCABIYFjNFQjBDMDhGRDFFMDRGRTRBMDk2AA==",
  "message_type": "text"
}
```

**Tipos de mensajes soportados:**
- `text`: Mensaje de texto
- `image`: Imagen con caption opcional
- `audio`: Mensaje de audio
- `video`: Video
- `document`: Documento

**Notas:**
- Siempre devuelve 200 OK para evitar reintentos de Meta
- Los errores se registran en logs pero no se propagan a Meta
- El mensaje se normaliza automáticamente al formato estándar
- Los status updates (delivered, read, sent) también se reciben aquí

**Ejemplo de cURL:**
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
            "profile": {"name": "Test User"},
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

## 4. Enviar Mensaje

**Endpoint:** `POST /send/whatsapp`

**Descripción:** Envía mensajes de WhatsApp a un número específico. Soporta texto e imágenes.

**Headers:**
```
Content-Type: application/json
```

### 4.1 Enviar Mensaje de Texto

**Request Body:**
```json
{
  "to": "+5491112345678",
  "message": "Hola! Este es un mensaje de prueba.",
  "message_type": "text"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message_id": "wamid.HBgNNTQ5MTE1NTU1NTU1NRUCABIYFjNFQjBDMDhGRDFFMDRGRTRBMDk2AA==",
  "details": {
    "messaging_product": "whatsapp",
    "contacts": [
      {
        "input": "5491112345678",
        "wa_id": "5491112345678"
      }
    ],
    "messages": [
      {
        "id": "wamid.HBgNNTQ5MTE1NTU1NTU1NRUCABIYFjNFQjBDMDhGRDFFMDRGRTRBMDk2AA=="
      }
    ]
  }
}
```

**Ejemplo cURL:**
```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+5491112345678",
    "message": "Hola! Este es un mensaje de prueba.",
    "message_type": "text"
  }'
```

### 4.2 Enviar Imagen

**Request Body:**
```json
{
  "to": "+5491112345678",
  "message": "Aquí está la imagen que solicitaste",
  "message_type": "image",
  "media_url": "https://picsum.photos/400/300"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message_id": "wamid.XXX",
  "details": {
    "messaging_product": "whatsapp",
    "contacts": [
      {
        "input": "5491112345678",
        "wa_id": "5491112345678"
      }
    ],
    "messages": [
      {
        "id": "wamid.XXX"
      }
    ]
  }
}
```

**Ejemplo cURL:**
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

### 4.3 Respuesta de Error

**Response:** `200 OK` (con success: false)
```json
{
  "success": false,
  "message_id": null,
  "error": "Invalid access token",
  "details": {
    "error": {
      "message": "Invalid OAuth access token.",
      "type": "OAuthException",
      "code": 190,
      "fbtrace_id": "XXX"
    }
  }
}
```

**Parámetros:**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `to` | string | Sí | Número de WhatsApp con código de país (ej: "+5491112345678") |
| `message` | string | Sí | Texto del mensaje o caption (para imágenes) |
| `message_type` | string | Sí | Tipo de mensaje: "text" o "image" |
| `media_url` | string | Condicional | URL de la imagen (requerido solo para message_type="image") |

**Notas:**
- El número debe incluir el código de país con `+`
- Para imágenes, la URL debe ser accesible públicamente
- El servicio normaliza el número internamente (remueve el `+` para la API)
- Los errores se registran en logs automáticamente

---

## Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | Operación exitosa |
| 400 | Request inválido (parámetros faltantes o incorrectos) |
| 403 | Token de verificación incorrecto |
| 500 | Error interno del servidor |

---

## Formato de Números de Teléfono

**Formato esperado:** `+[código_país][número]`

Ejemplos:
- Argentina: `+5491112345678`
- México: `+5215512345678`
- España: `+34612345678`
- USA: `+15551234567`

**Importante:**
- Siempre incluir el código de país
- No incluir espacios, guiones ni paréntesis
- El `+` es requerido en los requests pero se remueve internamente para la API

---

## Logs

Todos los eventos se registran en:
- **Consola**: Nivel INFO
- **Archivo**: `logs/whatsapp_service_YYYYMMDD.log` (nivel DEBUG)

**Ejemplo de logs:**
```
2025-10-05 12:00:00 - whatsapp_service - INFO - Webhook event received
2025-10-05 12:00:01 - whatsapp_service - INFO - Normalized message: {'channel': 'whatsapp', 'sender': '+5491112345678', 'message': 'Hola', 'timestamp': '2025-10-05T12:00:00'}
2025-10-05 12:00:02 - whatsapp_service - INFO - Sending text message to +5491112345678
2025-10-05 12:00:03 - whatsapp_service - INFO - Message sent successfully to +5491112345678
```

---

## Documentación Interactiva

Una vez que el servicio esté corriendo, puedes acceder a la documentación interactiva (Swagger UI) en:

```
http://localhost:8000/docs
```

O la documentación alternativa (ReDoc) en:

```
http://localhost:8000/redoc
```

Estas interfaces te permiten:
- Ver todos los endpoints disponibles
- Probar los endpoints directamente desde el navegador
- Ver los esquemas de request/response
- Descargar la especificación OpenAPI

---

## Ejemplos de Integración

### Python (requests)

```python
import requests

# Enviar mensaje de texto
response = requests.post(
    "http://localhost:8000/send/whatsapp",
    json={
        "to": "+5491112345678",
        "message": "Hola desde Python",
        "message_type": "text"
    }
)
print(response.json())
```

### JavaScript (fetch)

```javascript
// Enviar mensaje de texto
fetch('http://localhost:8000/send/whatsapp', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    to: '+5491112345678',
    message: 'Hola desde JavaScript',
    message_type: 'text'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Node.js (axios)

```javascript
const axios = require('axios');

// Enviar mensaje de texto
axios.post('http://localhost:8000/send/whatsapp', {
  to: '+5491112345678',
  message: 'Hola desde Node.js',
  message_type: 'text'
})
.then(response => console.log(response.data))
.catch(error => console.error(error));
```

---

## Rate Limits

**WhatsApp Cloud API (Free Tier):**
- 1,000 conversaciones gratis por mes
- Límite de rate: ~80 mensajes por segundo
- Números de prueba: hasta 5 números

Para más información sobre límites, consulta la [documentación oficial de Meta](https://developers.facebook.com/docs/whatsapp/cloud-api/overview#throughput).

