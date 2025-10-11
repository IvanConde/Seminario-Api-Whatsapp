# 🚀 EMPIEZA AQUÍ - Tu servicio está listo!

## ✅ Credenciales Configuradas

Tu archivo `.env` ya está configurado con:
- ✅ Access Token de WhatsApp
- ✅ Phone Number ID: `788982084305600`
- ✅ Número de prueba: `+1 555 636 1287`
- ✅ Tu número: `+541139090008`

---

## 🎯 Inicio en 3 pasos

### Paso 1: Iniciar el servicio

```bash
./run.sh
```

### Paso 2: Probar que funciona (en otra terminal)

```bash
curl http://localhost:8000/
```

Deberías ver:
```json
{
  "status": "healthy",
  "service": "WhatsApp Integration Service",
  ...
}
```

### Paso 3: Enviar tu primer mensaje

```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+541139090008",
    "message": "¡Funciona! 🎉",
    "message_type": "text"
  }'
```

**¡Revisa tu WhatsApp! Deberías recibir el mensaje.**

---

## 🧪 Pruebas Automáticas

Una vez que el servicio esté corriendo, ejecuta en otra terminal:

```bash
poetry run python test_real_whatsapp.py
```

Este script enviará automáticamente:
- ✅ Un mensaje de texto
- ✅ Un mensaje con emojis
- ✅ Una imagen

---

## 📱 Números Configurados

**Número de prueba de Meta (desde):**
- `+1 555 636 1287`
- Phone Number ID: `788982084305600`

**Tu número (para recibir):**
- `+541139090008`

**⚠️ IMPORTANTE:** Asegúrate de que `+541139090008` esté agregado como "tester" en tu cuenta de Meta. Si no:
1. Ve a https://developers.facebook.com/
2. Tu App → WhatsApp → Getting Started
3. En "Send and receive messages" → "To"
4. Agrega tu número y verifica el código

---

## 🎯 Ejemplos de Uso

### Enviar mensaje simple

```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+541139090008",
    "message": "Hola desde el servicio!",
    "message_type": "text"
  }'
```

### Enviar mensaje con emojis

```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+541139090008",
    "message": "✅ Pedido confirmado\n📦 Código: #12345\n🚚 Llegará mañana",
    "message_type": "text"
  }'
```

### Enviar imagen

```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+541139090008",
    "message": "Aquí está tu producto",
    "message_type": "image",
    "media_url": "https://picsum.photos/400/300"
  }'
```

---

## 🔍 Ver Logs

```bash
# Ver logs en tiempo real
tail -f logs/whatsapp_service_*.log

# Ver todos los mensajes normalizados
cat logs/whatsapp_service_*.log | grep "Normalized message"

# Ver mensajes enviados
cat logs/whatsapp_service_*.log | grep "Message sent successfully"
```

---

## 🌐 Para Recibir Mensajes (Webhook)

Para que tu servicio reciba mensajes desde WhatsApp, necesitas exponerlo públicamente:

### Opción 1: ngrok (recomendado)

```bash
# En una nueva terminal
ngrok http 8000
```

Obtendrás una URL como: `https://abc123.ngrok.io`

### Configurar en Meta

1. Ve a https://developers.facebook.com/
2. Tu App → WhatsApp → Configuration
3. Click "Edit" en Webhook
4. **Callback URL**: `https://abc123.ngrok.io/webhook/whatsapp`
5. **Verify Token**: `my_verify_token_123`
6. Click "Verify and Save"
7. Suscríbete a: `messages` y `message_status`

**Ahora envía un mensaje desde tu WhatsApp al número de prueba y lo recibirás en tu servidor!**

---

## 📊 Endpoints Disponibles

| URL | Método | Descripción |
|-----|--------|-------------|
| `http://localhost:8000/` | GET | Health check |
| `http://localhost:8000/webhook/whatsapp` | GET | Verificación webhook |
| `http://localhost:8000/webhook/whatsapp` | POST | Recibir mensajes |
| `http://localhost:8000/send/whatsapp` | POST | Enviar mensajes |
| `http://localhost:8000/docs` | GET | Documentación Swagger |

---

## 🐛 Problemas Comunes

### "Error: Invalid access token"

El token expira cada 24 horas. Para obtener uno nuevo:
1. Ve a https://developers.facebook.com/
2. Tu App → WhatsApp → Getting Started
3. Copia el nuevo "Temporary access token"
4. Actualiza el archivo `.env`
5. Reinicia el servicio

### "Error: Recipient phone number not valid"

El número debe estar agregado como "tester" en Meta:
1. Ve a tu App en Meta
2. WhatsApp → Getting Started
3. En "To" agrega el número `+541139090008`
4. Verifica el código que recibirás por WhatsApp

### No recibo el mensaje

1. Verifica que el servicio esté corriendo: `curl http://localhost:8000/`
2. Verifica los logs: `tail -f logs/whatsapp_service_*.log`
3. Verifica que el número esté como "tester"
4. Verifica que el token no haya expirado

---

## 🎓 Para la Demo/Entrega

### Demo Rápida (5 minutos)

1. **Mostrar que el servicio funciona:**
   ```bash
   curl http://localhost:8000/
   ```

2. **Enviar un mensaje:**
   ```bash
   curl -X POST "http://localhost:8000/send/whatsapp" \
     -H "Content-Type: application/json" \
     -d '{"to": "+541139090008", "message": "Demo TP Seminario", "message_type": "text"}'
   ```

3. **Mostrar el mensaje recibido en tu WhatsApp**

4. **Mostrar los logs:**
   ```bash
   tail logs/whatsapp_service_*.log
   ```

5. **Simular mensaje entrante:**
   ```bash
   curl -X POST "http://localhost:8000/webhook/whatsapp" \
     -H "Content-Type: application/json" \
     -d '{
       "object": "whatsapp_business_account",
       "entry": [{
         "changes": [{
           "value": {
             "messages": [{
               "from": "541139090008",
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

6. **Mostrar mensaje normalizado en logs:**
   ```bash
   cat logs/whatsapp_service_*.log | grep "Normalized message" | tail -1
   ```

---

## 📚 Más Información

| Archivo | Descripción |
|---------|-------------|
| `LEEME_PRIMERO.md` | Guía general de inicio |
| `README.md` | Documentación completa |
| `EJEMPLOS.md` | Ejemplos de código |
| `DOCUMENTACION_ENDPOINTS.md` | Referencia de API |
| `ARQUITECTURA.md` | Diagramas del sistema |

---

## ✅ Checklist

- [ ] Servicio iniciado (`./run.sh`)
- [ ] Health check funcionando
- [ ] Mensaje enviado exitosamente
- [ ] Mensaje recibido en WhatsApp
- [ ] Logs verificados
- [ ] (Opcional) Webhook configurado con ngrok

---

## 🎉 ¡Listo!

Tu servicio de WhatsApp está **100% funcional** y listo para usar.

**Próximos pasos:**
1. Ejecuta `./run.sh`
2. En otra terminal: `poetry run python test_real_whatsapp.py`
3. Revisa tu WhatsApp

**Para la demo:**
- Lee `RESUMEN_PROYECTO.md`
- Ejecuta los ejemplos de arriba
- Muestra los logs

---

**¿Dudas?** Revisa `README.md` o `DOCUMENTACION_ENDPOINTS.md`

**¡Éxito con el TP!** 🚀
