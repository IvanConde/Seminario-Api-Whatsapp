# 🏗️ Arquitectura del Sistema

## Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────────┐
│                      WhatsApp Cloud API (Meta)                   │
│                     https://graph.facebook.com                   │
└────────────────────┬────────────────────────┬───────────────────┘
                     │                        │
                     │ Webhooks               │ API Calls
                     │ (mensajes entrantes)   │ (enviar mensajes)
                     ▼                        ▲
┌─────────────────────────────────────────────────────────────────┐
│                    Tu Servidor (localhost:8000)                  │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              whatsapp_service.py (FastAPI)                  ││
│  │                                                             ││
│  │  ┌──────────────────────┐    ┌──────────────────────┐    ││
│  │  │  GET /webhook/       │    │  POST /webhook/      │    ││
│  │  │  whatsapp            │    │  whatsapp            │    ││
│  │  │                      │    │                      │    ││
│  │  │  Verificación        │    │  Recibir mensajes    │    ││
│  │  │  de token            │    │  y normalizar        │    ││
│  │  └──────────────────────┘    └──────────────────────┘    ││
│  │                                                             ││
│  │  ┌──────────────────────┐    ┌──────────────────────┐    ││
│  │  │  POST /send/         │    │  GET /               │    ││
│  │  │  whatsapp            │    │                      │    ││
│  │  │                      │    │  Health Check        │    ││
│  │  │  Enviar mensajes     │    │                      │    ││
│  │  └──────────────────────┘    └──────────────────────┘    ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              whatsapp_client.py                             ││
│  │                                                             ││
│  │  • send_text_message()                                      ││
│  │  • send_image_message()                                     ││
│  │  • Manejo de httpx                                          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              models.py (Pydantic)                           ││
│  │                                                             ││
│  │  • NormalizedMessage                                        ││
│  │  • SendMessageRequest                                       ││
│  │  • SendMessageResponse                                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              logger.py                                      ││
│  │                                                             ││
│  │  • Logs en consola (INFO)                                   ││
│  │  • Logs en archivo (DEBUG)                                  ││
│  │  • logs/whatsapp_service_YYYYMMDD.log                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              config.py                                      ││
│  │                                                             ││
│  │  • Variables de entorno (.env)                              ││
│  │  • Settings con Pydantic                                    ││
│  └─────────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────────┘
```

---

## Flujo de Mensaje Entrante (Webhook)

```
Usuario WhatsApp                Meta API              Tu Servidor
     │                             │                       │
     │  "Hola"                     │                       │
     ├────────────────────────────>│                       │
     │                             │                       │
     │                             │  POST /webhook/       │
     │                             │  whatsapp             │
     │                             ├──────────────────────>│
     │                             │                       │
     │                             │  Payload:             │
     │                             │  {                    │
     │                             │    "messages": [{     │
     │                             │      "from": "549...", │
     │                             │      "text": {        │
     │                             │        "body": "Hola" │
     │                             │      }                │
     │                             │    }]                 │
     │                             │  }                    │
     │                             │                       │
     │                             │                       │ Normalizar
     │                             │                       │ mensaje
     │                             │                       │
     │                             │                       │ {
     │                             │                       │   "channel": "whatsapp",
     │                             │                       │   "sender": "+549...",
     │                             │                       │   "message": "Hola",
     │                             │                       │   "timestamp": "..."
     │                             │                       │ }
     │                             │                       │
     │                             │                       │ Guardar en logs
     │                             │                       │
     │                             │       200 OK          │
     │                             │<──────────────────────┤
     │                             │                       │
```

---

## Flujo de Mensaje Saliente (Envío)

```
Tu App/Cliente            Tu Servidor              Meta API         Usuario WhatsApp
     │                       │                        │                    │
     │  POST /send/whatsapp  │                        │                    │
     │  {                    │                        │                    │
     │    "to": "+549...",   │                        │                    │
     │    "message": "Hola"  │                        │                    │
     │  }                    │                        │                    │
     ├──────────────────────>│                        │                    │
     │                       │                        │                    │
     │                       │ Validar request        │                    │
     │                       │                        │                    │
     │                       │  POST /messages        │                    │
     │                       │  {                     │                    │
     │                       │    "to": "549...",     │                    │
     │                       │    "type": "text",     │                    │
     │                       │    "text": {           │                    │
     │                       │      "body": "Hola"    │                    │
     │                       │    }                   │                    │
     │                       │  }                     │                    │
     │                       ├───────────────────────>│                    │
     │                       │                        │                    │
     │                       │                        │   Enviar mensaje   │
     │                       │                        ├───────────────────>│
     │                       │                        │                    │
     │                       │                        │   "Hola"           │
     │                       │                        │                    │
     │                       │  {                     │                    │
     │                       │    "messages": [{      │                    │
     │                       │      "id": "wamid..."  │                    │
     │                       │    }]                  │                    │
     │                       │  }                     │                    │
     │                       │<───────────────────────┤                    │
     │                       │                        │                    │
     │                       │ Guardar en logs        │                    │
     │                       │                        │                    │
     │  {                    │                        │                    │
     │    "success": true,   │                        │                    │
     │    "message_id": "..." │                        │                    │
     │  }                    │                        │                    │
     │<──────────────────────┤                        │                    │
     │                       │                        │                    │
```

---

## Flujo de Verificación de Webhook

```
Meta API                          Tu Servidor
    │                                 │
    │  GET /webhook/whatsapp?         │
    │  hub.mode=subscribe&            │
    │  hub.verify_token=TOKEN&        │
    │  hub.challenge=123              │
    ├────────────────────────────────>│
    │                                 │
    │                                 │ Validar token
    │                                 │
    │                                 │ if token == TOKEN:
    │                                 │   return challenge
    │                                 │
    │           "123"                 │
    │<────────────────────────────────┤
    │                                 │
    │  ✅ Webhook verificado          │
    │                                 │
```

---

## Componentes del Sistema

### 1. FastAPI (whatsapp_service.py)
**Responsabilidad:** API REST y endpoints

- Maneja requests HTTP
- Valida webhooks de Meta
- Coordina entre cliente y modelos
- Gestiona respuestas

### 2. WhatsApp Client (whatsapp_client.py)
**Responsabilidad:** Comunicación con WhatsApp API

- Envía requests a Meta
- Maneja autenticación (Bearer token)
- Formatea payloads según API de Meta
- Maneja errores de red

### 3. Models (models.py)
**Responsabilidad:** Validación y estructura de datos

- Define esquemas con Pydantic
- Valida automáticamente tipos
- Documenta estructura de datos
- Serialización/deserialización

### 4. Logger (logger.py)
**Responsabilidad:** Registro de eventos

- Logs en consola para monitoreo
- Logs en archivo para auditoría
- Diferentes niveles (INFO, DEBUG, ERROR)
- Rotación diaria de archivos

### 5. Config (config.py)
**Responsabilidad:** Configuración centralizada

- Lee variables de entorno
- Provee defaults
- Valida configuración
- Acceso centralizado a settings

---

## Formato de Mensaje Normalizado

**Entrada (de WhatsApp API):**
```json
{
  "messages": [{
    "from": "5491112345678",
    "id": "wamid.HBgN...",
    "timestamp": "1633024800",
    "type": "text",
    "text": {
      "body": "Hola, necesito ayuda"
    }
  }]
}
```

**Salida (normalizado):**
```json
{
  "channel": "whatsapp",
  "sender": "+5491112345678",
  "message": "Hola, necesito ayuda",
  "timestamp": "2021-10-01T00:00:00",
  "message_id": "wamid.HBgN...",
  "message_type": "text"
}
```

---

## Stack Tecnológico

```
┌─────────────────────────────────────┐
│         Python 3.9+                 │
└─────────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼────┐      ┌──────▼──────┐
│ FastAPI│      │   Poetry    │
│        │      │             │
│ REST   │      │ Dependency  │
│ API    │      │ Management  │
└───┬────┘      └─────────────┘
    │
    ├──────┬──────────┬─────────┐
    │      │          │         │
┌───▼──┐ ┌─▼──────┐ ┌▼──────┐ ┌▼────────┐
│Pydantic│httpx   │Uvicorn│python-   │
│        │        │       │dotenv    │
│Validation│HTTP  │ASGI   │Env vars  │
│        │Client  │Server │          │
└────────┘└────────┘└───────┘└──────────┘
```

---

## Seguridad

### 1. Validación de Token
- Meta envía `hub.verify_token`
- Se compara con el configurado en `.env`
- Solo requests válidos son aceptados

### 2. Variables de Entorno
- Credenciales nunca en código
- `.env` en `.gitignore`
- Acceso centralizado vía `config.py`

### 3. Validación de Datos
- Pydantic valida todos los inputs
- Tipos verificados automáticamente
- Errores claros si datos inválidos

### 4. Logs de Auditoría
- Todos los eventos registrados
- Timestamps precisos
- Trazabilidad completa

---

## Escalabilidad

### Actual (Desarrollo)
- Servidor único
- Procesamiento síncrono
- Logs en archivo local

### Futuro (Producción)
- Load balancer
- Múltiples instancias
- Base de datos para mensajes
- Queue (RabbitMQ/Redis) para procesamiento
- Logs centralizados (ELK Stack)
- Caché (Redis)
- Monitoreo (Prometheus/Grafana)

---

## Manejo de Errores

```
Request
  │
  ├─> Validación Pydantic
  │     │
  │     ├─> ❌ Error → 422 Unprocessable Entity
  │     │
  │     └─> ✅ OK
  │
  ├─> Lógica de Negocio
  │     │
  │     ├─> ❌ Error → Log + Response estructurado
  │     │
  │     └─> ✅ OK
  │
  ├─> Llamada a WhatsApp API
  │     │
  │     ├─> ❌ Timeout → Log + Error response
  │     ├─> ❌ Auth Error → Log + Error response
  │     ├─> ❌ Rate Limit → Log + Error response
  │     │
  │     └─> ✅ OK
  │
  └─> Response al cliente
```

---

## Testing

```
┌─────────────────────────────────────┐
│         test_service.py             │
│                                     │
│  • Health check                     │
│  • Webhook verification             │
│  • Receive message                  │
│  • Send message                     │
└─────────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼──────────┐  ┌────▼─────────┐
│ Unit Tests   │  │ Integration  │
│              │  │ Tests        │
│ pytest       │  │              │
│ FastAPI      │  │ Real API     │
│ TestClient   │  │ calls        │
└──────────────┘  └──────────────┘
```

---

## Monitoreo

### Logs
```
logs/whatsapp_service_20251005.log
```

Contiene:
- Timestamp de cada evento
- Nivel (INFO, DEBUG, ERROR)
- Mensajes recibidos/enviados
- Errores con stack trace

### Métricas (futuro)
- Mensajes por minuto
- Tasa de error
- Latencia de respuesta
- Uso de API quota

---

## Deployment

### Desarrollo (actual)
```bash
./run.sh
# o
poetry run python -m src.whatsapp_service
```

### Producción (recomendado)
```bash
# Con Gunicorn
gunicorn src.whatsapp_service:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000

# Con Docker
docker build -t whatsapp-service .
docker run -p 8000:8000 --env-file .env whatsapp-service
```

---

## Límites y Consideraciones

### WhatsApp Cloud API (Free Tier)
- **1,000 conversaciones/mes** gratis
- **~80 mensajes/segundo** rate limit
- **5 números de prueba** máximo
- **24h** duración token temporal

### Servidor
- **Puerto 8000** por defecto
- **Webhook público** requerido para recibir mensajes
- **HTTPS** requerido en producción

---

Esta arquitectura es **simple, escalable y lista para producción** con modificaciones mínimas.

