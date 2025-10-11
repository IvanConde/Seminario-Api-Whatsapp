# 🚀 LÉEME PRIMERO - Inicio Rápido

## ¿Qué es esto?

Este es un **servicio completo de integración con WhatsApp** usando la API gratuita de Meta (WhatsApp Cloud API). El proyecto está listo para usar y cumple con todos los requisitos del TP Seminario - Equipo 1.

---

## ⚡ Inicio en 3 pasos

### 1️⃣ Instalar dependencias

```bash
poetry install
```

### 2️⃣ Ejecutar el servicio

```bash
./run.sh
```

O también:

```bash
poetry run python -m src.whatsapp_service
```

### 3️⃣ Probar que funciona

Abre otra terminal y ejecuta:

```bash
curl http://localhost:8000/
```

Deberías ver:
```json
{
  "status": "healthy",
  "service": "WhatsApp Integration Service",
  "timestamp": "..."
}
```

✅ **¡Listo! El servicio está funcionando.**

---

## 🧪 Pruebas Rápidas

### Probar webhook verification:

```bash
curl "http://localhost:8000/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=my_verify_token_123&hub.challenge=test123"
```

Deberías ver: `test123`

### Simular mensaje entrante:

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
          "messages": [{
            "from": "5491112345678",
            "id": "wamid.test",
            "timestamp": "1633024800",
            "text": {"body": "Hola"},
            "type": "text"
          }]
        }
      }]
    }]
  }'
```

Revisa los logs: `cat logs/whatsapp_service_*.log`

Verás el mensaje normalizado en formato estándar.

---

## 📱 Conectar con WhatsApp Real (GRATIS)

### Paso 1: Crear cuenta en Meta

1. Ve a: **https://developers.facebook.com/**
2. Crea una cuenta (es gratis)
3. Crea una App de tipo "Business"

### Paso 2: Configurar WhatsApp

1. En tu app, busca "WhatsApp" → "Set up"
2. En "Getting Started", verás:
   - **Access Token** (cópialo)
   - **Phone Number ID** (cópialo)
   - Un **número de prueba** gratis

### Paso 3: Actualizar credenciales

Edita el archivo `.env`:

```bash
WHATSAPP_ACCESS_TOKEN=tu_token_aqui
WHATSAPP_PHONE_NUMBER_ID=tu_phone_id_aqui
WHATSAPP_VERIFY_TOKEN=mi_token_secreto_123
```

### Paso 4: Agregar tu número

En Meta, agrega tu número de WhatsApp personal como "tester":
- Recibirás un código de verificación
- Ahora puedes enviar mensajes a ese número

### Paso 5: Probar envío

```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+5491112345678",
    "message": "¡Hola! Mensaje de prueba",
    "message_type": "text"
  }'
```

**¡Deberías recibir el mensaje en tu WhatsApp!** 🎉

### Paso 6: Recibir mensajes (webhook)

Para recibir mensajes, necesitas exponer tu servidor:

```bash
# Instalar ngrok
brew install ngrok  # macOS
# o descargar de https://ngrok.com/

# Ejecutar
ngrok http 8000
```

Obtendrás una URL como: `https://abc123.ngrok.io`

Luego en Meta:
1. WhatsApp → Configuration → Webhook
2. **Callback URL**: `https://abc123.ngrok.io/webhook/whatsapp`
3. **Verify Token**: `my_verify_token_123`
4. Suscríbete a: `messages` y `message_status`

**Ahora envía un mensaje al número de prueba de Meta y lo recibirás en tu servidor!**

---

## 📚 Documentación Completa

| Archivo | Descripción |
|---------|-------------|
| `README.md` | Documentación completa del proyecto |
| `QUICKSTART.md` | Guía rápida de inicio |
| `DOCUMENTACION_ENDPOINTS.md` | Detalles de todos los endpoints |
| `documentacon.md` | Resumen de entregables |
| `POSTMAN_COLLECTION.json` | Colección para importar en Postman |

---

## 🎯 Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/webhook/whatsapp` | GET | Verificación webhook (Meta) |
| `/webhook/whatsapp` | POST | Recibir mensajes |
| `/send/whatsapp` | POST | Enviar mensajes |
| `/docs` | GET | Documentación interactiva |

---

## 📊 Estructura del Código

```
src/
├── whatsapp_service.py    ← Servicio principal (FastAPI)
├── whatsapp_client.py     ← Cliente para enviar mensajes
├── models.py              ← Modelos de datos
├── config.py              ← Configuración
└── logger.py              ← Sistema de logs
```

---

## 🔥 Características Principales

✅ **Webhook receptor** - Recibe mensajes de WhatsApp  
✅ **Validación de token** - Seguridad con Meta  
✅ **Normalización** - Formato estándar para todos los mensajes  
✅ **Envío de mensajes** - Texto e imágenes  
✅ **Logs completos** - Archivo y consola  
✅ **Manejo de errores** - Robusto y detallado  
✅ **100% GRATIS** - WhatsApp Cloud API free tier  
✅ **Poetry** - Gestión de dependencias  
✅ **Tests** - Automatizados  
✅ **Documentación** - Completa con ejemplos  

---

## 💡 Tips Importantes

1. **Token temporal expira en 24h** - Genera uno permanente en Meta
2. **Formato de números**: Siempre con código de país: `+5491112345678`
3. **Logs**: Revisa `logs/whatsapp_service_*.log` para debugging
4. **Números de prueba**: Solo puedes enviar a números agregados como "testers"
5. **Free tier**: 1,000 conversaciones gratis por mes

---

## ❓ ¿Problemas?

### No puedo instalar Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Error: "ModuleNotFoundError"

```bash
poetry install
```

### El servicio no inicia

Verifica que el puerto 8000 esté libre:

```bash
lsof -i :8000
```

### No recibo mensajes

1. ¿Está ngrok corriendo?
2. ¿Configuraste el webhook en Meta?
3. ¿El verify_token coincide?

---

## 🎓 Para el TP

**Archivos principales a revisar:**

1. `src/whatsapp_service.py` - Implementación del webhook y endpoints
2. `documentacon.md` - Resumen de entregables
3. `DOCUMENTACION_ENDPOINTS.md` - Documentación de API
4. `POSTMAN_COLLECTION.json` - Pruebas con Postman

**Demostración:**

1. Ejecuta: `./run.sh`
2. Muestra el health check
3. Simula un mensaje entrante (curl)
4. Muestra los logs con el mensaje normalizado
5. (Opcional) Envía un mensaje real si tienes credenciales

---

## 📞 Soporte

- **WhatsApp Cloud API**: https://developers.facebook.com/docs/whatsapp/cloud-api
- **FastAPI**: https://fastapi.tiangolo.com/
- **Poetry**: https://python-poetry.org/

---

## ✅ Checklist de Entrega

- [x] Webhook receptor (`/webhook/whatsapp`)
- [x] Validación de token de Meta
- [x] Normalización a formato estándar
- [x] Endpoint de envío (`/send/whatsapp`)
- [x] Soporte texto e imágenes
- [x] Logs (archivo y consola)
- [x] Manejo de errores
- [x] Documentación completa
- [x] Ejemplos de request/response
- [x] Postman/cURL de prueba
- [x] Poetry para dependencias
- [x] API gratuita

---

**¡Todo listo para usar!** 🚀

Para más detalles, lee `README.md` o `QUICKSTART.md`

