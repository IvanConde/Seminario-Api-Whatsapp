# 🚀 Guía Rápida de Inicio

## Instalación Rápida

```bash
# 1. Instalar Poetry (si no lo tienes)
curl -sSL https://install.python-poetry.org | python3 -

# 2. Instalar dependencias
poetry install

# 3. Ejecutar el servicio
poetry run python -m src.whatsapp_service
```

El servicio estará corriendo en: **http://localhost:8000**

## 🧪 Prueba Rápida

### 1. Verificar que funciona:

```bash
curl http://localhost:8000/
```

Deberías ver:
```json
{
  "status": "healthy",
  "service": "WhatsApp Integration Service",
  "timestamp": "2025-10-05T..."
}
```

### 2. Probar webhook verification:

```bash
curl "http://localhost:8000/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=my_verify_token_123&hub.challenge=test123"
```

Deberías ver: `test123`

### 3. Simular mensaje entrante:

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

Verifica los logs en `logs/whatsapp_service_YYYYMMDD.log` - deberías ver el mensaje normalizado.

## 🔑 Configurar WhatsApp Cloud API (GRATIS)

### Paso 1: Crear cuenta en Meta for Developers

1. Ve a: https://developers.facebook.com/
2. Crea una cuenta o inicia sesión
3. Click en "My Apps" → "Create App"
4. Selecciona tipo "Business"
5. Completa el nombre de la app

### Paso 2: Agregar WhatsApp

1. En tu app, busca "WhatsApp" en productos
2. Click "Set up"
3. Sigue el wizard de configuración

### Paso 3: Obtener credenciales

En la página "WhatsApp" → "Getting Started":

1. **Access Token**: Copia el token temporal (24h) o genera uno permanente
2. **Phone Number ID**: Copia el ID del número de prueba
3. **Business Account ID**: Lo encuentras en la configuración

### Paso 4: Actualizar `.env`

```bash
WHATSAPP_ACCESS_TOKEN=tu_token_aqui
WHATSAPP_PHONE_NUMBER_ID=tu_phone_id_aqui
WHATSAPP_VERIFY_TOKEN=mi_token_secreto_123
```

### Paso 5: Agregar número de prueba

En "WhatsApp" → "Getting Started" → "To":
- Agrega tu número de WhatsApp personal
- Recibirás un código de verificación por WhatsApp
- Ahora puedes enviar mensajes a ese número

### Paso 6: Probar envío

```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+549111234567",
    "message": "Hola! Mensaje de prueba",
    "message_type": "text"
  }'
```

¡Deberías recibir el mensaje en tu WhatsApp! 🎉

## 🌐 Exponer webhook públicamente

Para recibir mensajes de WhatsApp, Meta necesita enviar webhooks a tu servidor.

### Opción 1: ngrok (Recomendado)

```bash
# Instalar
brew install ngrok  # macOS
# o descargar de https://ngrok.com/

# Ejecutar
ngrok http 8000
```

Obtendrás una URL como: `https://abc123.ngrok.io`

### Opción 2: localtunnel

```bash
npm install -g localtunnel
lt --port 8000
```

### Configurar en Meta

1. Ve a tu app → WhatsApp → Configuration
2. Click "Edit" en Webhook
3. **Callback URL**: `https://tu-url-publica.com/webhook/whatsapp`
4. **Verify Token**: `my_verify_token_123` (o el que pusiste en `.env`)
5. Click "Verify and Save"
6. Suscríbete a: `messages` y `message_status`

## 📱 Probar flujo completo

1. **Envía un mensaje** desde tu WhatsApp al número de prueba de Meta
2. **Meta enviará un webhook** a tu servidor
3. **Verifica los logs**: `tail -f logs/whatsapp_service_*.log`
4. **Deberías ver** el mensaje normalizado

## 🎯 Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/webhook/whatsapp` | Verificación webhook |
| POST | `/webhook/whatsapp` | Recibir mensajes |
| POST | `/send/whatsapp` | Enviar mensajes |

## 📚 Próximos Pasos

- Lee el `README.md` completo para más detalles
- Importa `POSTMAN_COLLECTION.json` en Postman
- Revisa los logs en `logs/`
- Personaliza la lógica de negocio en `whatsapp_service.py`

## ❓ Problemas Comunes

**Error: "ModuleNotFoundError"**
```bash
poetry install
```

**Error: "Verification token mismatch"**
- Verifica que el token en `.env` coincida con el de Meta

**No recibo webhooks**
- Verifica que ngrok esté corriendo
- Verifica la configuración en Meta
- Revisa los logs

**Error al enviar mensajes**
- Verifica que el número esté agregado como "tester"
- Verifica que el access token sea válido
- El número debe tener formato: `+5491112345678`

## 💡 Tips

- Los tokens temporales expiran en 24h, genera uno permanente
- Puedes enviar hasta 1000 mensajes gratis al mes
- Los números de prueba solo pueden enviar a números agregados como "testers"
- Revisa siempre los logs para debugging

¡Listo! Ya tienes tu servicio de WhatsApp funcionando 🚀

