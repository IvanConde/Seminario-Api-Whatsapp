# 📚 Ejemplos de Uso

## Tabla de Contenidos

1. [Ejemplos con cURL](#ejemplos-con-curl)
2. [Ejemplos con Python](#ejemplos-con-python)
3. [Ejemplos con JavaScript](#ejemplos-con-javascript)
4. [Ejemplos con Postman](#ejemplos-con-postman)
5. [Casos de Uso Comunes](#casos-de-uso-comunes)

---

## Ejemplos con cURL

### 1. Health Check

```bash
curl http://localhost:8000/
```

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "WhatsApp Integration Service",
  "timestamp": "2025-10-05T12:00:00.000000"
}
```

---

### 2. Verificar Webhook (GET)

```bash
curl "http://localhost:8000/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=my_verify_token_123&hub.challenge=test_challenge_123"
```

**Respuesta:**
```
test_challenge_123
```

---

### 3. Enviar Mensaje de Texto Simple

```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+5491112345678",
    "message": "Hola! Este es un mensaje de prueba.",
    "message_type": "text"
  }'
```

**Respuesta:**
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

---

### 4. Enviar Mensaje con Emojis

```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+5491112345678",
    "message": "¡Hola! 👋\n\n✅ Tu pedido está listo\n📦 Código: #12345\n🚚 Llegará mañana",
    "message_type": "text"
  }'
```

---

### 5. Enviar Imagen

```bash
curl -X POST "http://localhost:8000/send/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+5491112345678",
    "message": "Aquí está el producto que solicitaste",
    "message_type": "image",
    "media_url": "https://picsum.photos/400/300"
  }'
```

---

### 6. Simular Mensaje Entrante (Webhook)

```bash
curl -X POST "http://localhost:8000/webhook/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "object": "whatsapp_business_account",
    "entry": [{
      "id": "123456789",
      "changes": [{
        "value": {
          "messaging_product": "whatsapp",
          "metadata": {
            "display_phone_number": "15551234567",
            "phone_number_id": "PHONE_NUMBER_ID"
          },
          "contacts": [{
            "profile": {
              "name": "Juan Pérez"
            },
            "wa_id": "5491112345678"
          }],
          "messages": [{
            "from": "5491112345678",
            "id": "wamid.test123",
            "timestamp": "1633024800",
            "text": {
              "body": "Hola, necesito información sobre mis pedidos"
            },
            "type": "text"
          }]
        },
        "field": "messages"
      }]
    }]
  }'
```

---

## Ejemplos con Python

### 1. Cliente Simple

```python
import requests

BASE_URL = "http://localhost:8000"

def send_whatsapp_message(to: str, message: str):
    """Envía un mensaje de WhatsApp."""
    response = requests.post(
        f"{BASE_URL}/send/whatsapp",
        json={
            "to": to,
            "message": message,
            "message_type": "text"
        }
    )
    return response.json()

# Uso
result = send_whatsapp_message("+5491112345678", "Hola desde Python!")
print(result)
```

---

### 2. Cliente con Manejo de Errores

```python
import requests
from typing import Dict, Optional

class WhatsAppClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def send_text(self, to: str, message: str) -> Dict:
        """Envía un mensaje de texto."""
        try:
            response = requests.post(
                f"{self.base_url}/send/whatsapp",
                json={
                    "to": to,
                    "message": message,
                    "message_type": "text"
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_image(self, to: str, image_url: str, caption: str = "") -> Dict:
        """Envía una imagen."""
        try:
            response = requests.post(
                f"{self.base_url}/send/whatsapp",
                json={
                    "to": to,
                    "message": caption,
                    "message_type": "image",
                    "media_url": image_url
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def health_check(self) -> bool:
        """Verifica que el servicio esté funcionando."""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False

# Uso
client = WhatsAppClient()

if client.health_check():
    print("✅ Servicio funcionando")
    
    # Enviar texto
    result = client.send_text("+5491112345678", "Hola desde Python!")
    if result.get("success"):
        print(f"✅ Mensaje enviado: {result['message_id']}")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    # Enviar imagen
    result = client.send_image(
        "+5491112345678",
        "https://picsum.photos/400/300",
        "Aquí está la imagen"
    )
    if result.get("success"):
        print(f"✅ Imagen enviada: {result['message_id']}")
else:
    print("❌ Servicio no disponible")
```

---

### 3. Bot de Respuesta Automática

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

WHATSAPP_SERVICE_URL = "http://localhost:8000"

def send_whatsapp(to: str, message: str):
    """Envía un mensaje de WhatsApp."""
    requests.post(
        f"{WHATSAPP_SERVICE_URL}/send/whatsapp",
        json={
            "to": to,
            "message": message,
            "message_type": "text"
        }
    )

@app.route("/webhook/whatsapp", methods=["POST"])
def webhook():
    """Recibe webhooks y responde automáticamente."""
    data = request.json
    
    # Procesar mensajes entrantes
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            
            for message in value.get("messages", []):
                sender = message.get("from")
                text = message.get("text", {}).get("body", "")
                
                # Lógica de respuesta
                if "hola" in text.lower():
                    response = "¡Hola! ¿En qué puedo ayudarte?"
                elif "precio" in text.lower():
                    response = "Nuestros precios van desde $100 a $500"
                elif "horario" in text.lower():
                    response = "Atendemos de Lunes a Viernes, 9am a 6pm"
                else:
                    response = "Gracias por tu mensaje. Un agente te responderá pronto."
                
                # Enviar respuesta
                send_whatsapp(f"+{sender}", response)
    
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=5000)
```

---

## Ejemplos con JavaScript

### 1. Cliente con Fetch (Browser)

```javascript
class WhatsAppClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async sendText(to, message) {
    try {
      const response = await fetch(`${this.baseUrl}/send/whatsapp`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          to: to,
          message: message,
          message_type: 'text'
        })
      });
      
      return await response.json();
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async sendImage(to, imageUrl, caption = '') {
    try {
      const response = await fetch(`${this.baseUrl}/send/whatsapp`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          to: to,
          message: caption,
          message_type: 'image',
          media_url: imageUrl
        })
      });
      
      return await response.json();
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async healthCheck() {
    try {
      const response = await fetch(`${this.baseUrl}/`);
      return response.ok;
    } catch {
      return false;
    }
  }
}

// Uso
const client = new WhatsAppClient();

// Enviar mensaje
client.sendText('+5491112345678', 'Hola desde JavaScript!')
  .then(result => {
    if (result.success) {
      console.log('✅ Mensaje enviado:', result.message_id);
    } else {
      console.error('❌ Error:', result.error);
    }
  });
```

---

### 2. Cliente con Axios (Node.js)

```javascript
const axios = require('axios');

class WhatsAppClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.client = axios.create({
      baseURL: baseUrl,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  async sendText(to, message) {
    try {
      const response = await this.client.post('/send/whatsapp', {
        to: to,
        message: message,
        message_type: 'text'
      });
      return response.data;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async sendImage(to, imageUrl, caption = '') {
    try {
      const response = await this.client.post('/send/whatsapp', {
        to: to,
        message: caption,
        message_type: 'image',
        media_url: imageUrl
      });
      return response.data;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async healthCheck() {
    try {
      const response = await this.client.get('/');
      return response.status === 200;
    } catch {
      return false;
    }
  }
}

// Uso
(async () => {
  const client = new WhatsAppClient();
  
  if (await client.healthCheck()) {
    console.log('✅ Servicio funcionando');
    
    const result = await client.sendText('+5491112345678', 'Hola desde Node.js!');
    if (result.success) {
      console.log('✅ Mensaje enviado:', result.message_id);
    } else {
      console.error('❌ Error:', result.error);
    }
  } else {
    console.error('❌ Servicio no disponible');
  }
})();
```

---

### 3. Servidor Express con Webhook

```javascript
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

const WHATSAPP_SERVICE_URL = 'http://localhost:8000';

async function sendWhatsApp(to, message) {
  try {
    await axios.post(`${WHATSAPP_SERVICE_URL}/send/whatsapp`, {
      to: to,
      message: message,
      message_type: 'text'
    });
  } catch (error) {
    console.error('Error enviando mensaje:', error.message);
  }
}

app.post('/webhook/whatsapp', async (req, res) => {
  const data = req.body;
  
  // Procesar mensajes entrantes
  for (const entry of data.entry || []) {
    for (const change of entry.changes || []) {
      const value = change.value || {};
      
      for (const message of value.messages || []) {
        const sender = message.from;
        const text = message.text?.body || '';
        
        console.log(`Mensaje de ${sender}: ${text}`);
        
        // Lógica de respuesta
        let response;
        if (text.toLowerCase().includes('hola')) {
          response = '¡Hola! ¿En qué puedo ayudarte?';
        } else if (text.toLowerCase().includes('precio')) {
          response = 'Nuestros precios van desde $100 a $500';
        } else {
          response = 'Gracias por tu mensaje. Te responderemos pronto.';
        }
        
        // Enviar respuesta
        await sendWhatsApp(`+${sender}`, response);
      }
    }
  }
  
  res.json({ status: 'ok' });
});

app.listen(5000, () => {
  console.log('Servidor escuchando en puerto 5000');
});
```

---

## Ejemplos con Postman

### Importar Colección

1. Abre Postman
2. Click en "Import"
3. Selecciona el archivo `POSTMAN_COLLECTION.json`
4. La colección aparecerá con todos los endpoints

### Variables de Entorno en Postman

```json
{
  "base_url": "http://localhost:8000",
  "test_phone": "+5491112345678",
  "verify_token": "my_verify_token_123"
}
```

---

## Casos de Uso Comunes

### 1. Notificaciones de Pedidos

```python
def notify_order_status(phone: str, order_id: str, status: str):
    """Notifica el estado de un pedido."""
    messages = {
        "pending": f"📦 Tu pedido #{order_id} está siendo preparado",
        "shipped": f"🚚 Tu pedido #{order_id} ha sido enviado",
        "delivered": f"✅ Tu pedido #{order_id} ha sido entregado"
    }
    
    message = messages.get(status, f"Estado de pedido #{order_id}: {status}")
    
    return send_whatsapp_message(phone, message)

# Uso
notify_order_status("+5491112345678", "12345", "shipped")
```

---

### 2. Recordatorios de Citas

```python
from datetime import datetime, timedelta

def send_appointment_reminder(phone: str, appointment_date: datetime, doctor: str):
    """Envía recordatorio de cita médica."""
    message = f"""
🏥 Recordatorio de Cita

📅 Fecha: {appointment_date.strftime('%d/%m/%Y')}
🕐 Hora: {appointment_date.strftime('%H:%M')}
👨‍⚕️ Doctor: {doctor}

Por favor, llega 10 minutos antes.
Para cancelar, responde CANCELAR.
    """.strip()
    
    return send_whatsapp_message(phone, message)

# Uso
appointment = datetime.now() + timedelta(days=1)
send_appointment_reminder("+5491112345678", appointment, "Dr. García")
```

---

### 3. Alertas de Seguridad

```python
def send_security_alert(phone: str, event: str, location: str):
    """Envía alerta de seguridad."""
    message = f"""
🚨 ALERTA DE SEGURIDAD

⚠️ Evento: {event}
📍 Ubicación: {location}
🕐 Hora: {datetime.now().strftime('%H:%M:%S')}

Si no fuiste tú, responde URGENTE.
    """.strip()
    
    return send_whatsapp_message(phone, message)

# Uso
send_security_alert("+5491112345678", "Inicio de sesión desde nuevo dispositivo", "Buenos Aires, Argentina")
```

---

### 4. Confirmaciones de Pago

```python
def send_payment_confirmation(phone: str, amount: float, reference: str):
    """Envía confirmación de pago."""
    message = f"""
✅ Pago Confirmado

💰 Monto: ${amount:.2f}
🔢 Referencia: {reference}
📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}

Gracias por tu pago.
    """.strip()
    
    return send_whatsapp_message(phone, message)

# Uso
send_payment_confirmation("+5491112345678", 1500.00, "PAY-12345")
```

---

### 5. Encuestas de Satisfacción

```python
def send_satisfaction_survey(phone: str, order_id: str):
    """Envía encuesta de satisfacción."""
    message = f"""
📊 Encuesta de Satisfacción

¿Cómo calificarías tu experiencia con el pedido #{order_id}?

Responde con un número del 1 al 5:
⭐ 1 - Muy mala
⭐⭐ 2 - Mala
⭐⭐⭐ 3 - Regular
⭐⭐⭐⭐ 4 - Buena
⭐⭐⭐⭐⭐ 5 - Excelente
    """.strip()
    
    return send_whatsapp_message(phone, message)

# Uso
send_satisfaction_survey("+5491112345678", "12345")
```

---

### 6. Envío Masivo (con Rate Limiting)

```python
import time
from typing import List

def send_bulk_messages(recipients: List[str], message: str, delay: float = 1.0):
    """Envía mensajes a múltiples destinatarios con delay."""
    results = []
    
    for i, phone in enumerate(recipients, 1):
        print(f"Enviando {i}/{len(recipients)} a {phone}...")
        
        result = send_whatsapp_message(phone, message)
        results.append({
            "phone": phone,
            "success": result.get("success", False),
            "message_id": result.get("message_id")
        })
        
        # Delay para evitar rate limiting
        if i < len(recipients):
            time.sleep(delay)
    
    return results

# Uso
recipients = [
    "+5491112345678",
    "+5491187654321",
    "+5491198765432"
]

message = "🎉 ¡Oferta especial! 50% de descuento este fin de semana."

results = send_bulk_messages(recipients, message, delay=2.0)

# Resumen
successful = sum(1 for r in results if r["success"])
print(f"\n✅ Enviados: {successful}/{len(recipients)}")
```

---

## Tips y Mejores Prácticas

### 1. Manejo de Rate Limits

```python
import time
from functools import wraps

def rate_limit(max_per_minute=60):
    """Decorator para limitar rate de envío."""
    min_interval = 60.0 / max_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        
        return wrapper
    return decorator

@rate_limit(max_per_minute=30)
def send_message_safe(phone, message):
    """Envía mensaje con rate limiting."""
    return send_whatsapp_message(phone, message)
```

---

### 2. Retry con Backoff Exponencial

```python
import time
from typing import Callable, Any

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0
) -> Any:
    """Reintenta una función con backoff exponencial."""
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            print(f"Intento {attempt + 1} falló: {e}. Reintentando en {delay}s...")
            time.sleep(delay)
            delay *= backoff_factor

# Uso
result = retry_with_backoff(
    lambda: send_whatsapp_message("+5491112345678", "Hola"),
    max_retries=3
)
```

---

Estos ejemplos cubren los casos de uso más comunes. Adapta según tus necesidades específicas.

