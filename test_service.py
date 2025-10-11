#!/usr/bin/env python3
"""Script de prueba rápida para verificar que el servicio funciona."""

import sys
import time
import requests
from subprocess import Popen, PIPE
import signal

def test_service():
    """Prueba básica del servicio."""
    print("🧪 Iniciando pruebas del servicio WhatsApp Integration...\n")
    
    # Iniciar el servicio
    print("1️⃣  Iniciando servicio...")
    process = Popen(
        ["poetry", "run", "python", "-m", "src.whatsapp_service"],
        stdout=PIPE,
        stderr=PIPE,
        text=True
    )
    
    # Esperar a que el servicio inicie
    time.sleep(3)
    
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: Health Check
        print("\n2️⃣  Probando Health Check...")
        response = requests.get(f"{base_url}/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("   ✅ Health Check OK")
        print(f"   📊 Response: {data}")
        
        # Test 2: Webhook Verification
        print("\n3️⃣  Probando Webhook Verification...")
        response = requests.get(
            f"{base_url}/webhook/whatsapp",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "my_verify_token_123",
                "hub.challenge": "test_challenge_123"
            }
        )
        assert response.status_code == 200
        assert response.text == "test_challenge_123"
        print("   ✅ Webhook Verification OK")
        
        # Test 3: Webhook Verification - Token incorrecto
        print("\n4️⃣  Probando Webhook Verification con token incorrecto...")
        response = requests.get(
            f"{base_url}/webhook/whatsapp",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "wrong_token",
                "hub.challenge": "test_challenge_123"
            }
        )
        assert response.status_code == 403
        print("   ✅ Rechazo de token incorrecto OK")
        
        # Test 4: Recibir mensaje
        print("\n5️⃣  Probando recepción de mensaje...")
        webhook_payload = {
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
                            "text": {"body": "Hola, mensaje de prueba"},
                            "type": "text"
                        }]
                    },
                    "field": "messages"
                }]
            }]
        }
        response = requests.post(f"{base_url}/webhook/whatsapp", json=webhook_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        print("   ✅ Recepción de mensaje OK")
        print("   📨 Mensaje normalizado guardado en logs")
        
        # Test 5: Enviar mensaje (fallará sin credenciales reales, pero probamos el endpoint)
        print("\n6️⃣  Probando endpoint de envío de mensaje...")
        send_payload = {
            "to": "+5491112345678",
            "message": "Mensaje de prueba",
            "message_type": "text"
        }
        response = requests.post(f"{base_url}/send/whatsapp", json=send_payload)
        assert response.status_code == 200
        data = response.json()
        # Con credenciales demo, esperamos que falle
        print("   ✅ Endpoint de envío responde correctamente")
        print(f"   📊 Response: {data}")
        
        print("\n" + "="*60)
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("="*60)
        print("\n📝 Verifica los logs en: logs/whatsapp_service_*.log")
        print("\n💡 Para usar el servicio con WhatsApp real:")
        print("   1. Configura las credenciales en .env")
        print("   2. Lee QUICKSTART.md para más detalles")
        print("   3. Usa ngrok para exponer el webhook")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ Error en prueba: {e}")
        return False
    except requests.exceptions.ConnectionError:
        print("\n❌ No se pudo conectar al servicio. ¿Está corriendo?")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False
    finally:
        # Detener el servicio
        print("\n7️⃣  Deteniendo servicio...")
        process.send_signal(signal.SIGINT)
        process.wait(timeout=5)
        print("   ✅ Servicio detenido\n")

if __name__ == "__main__":
    success = test_service()
    sys.exit(0 if success else 1)

