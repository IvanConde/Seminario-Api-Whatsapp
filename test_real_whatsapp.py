#!/usr/bin/env python3
"""Script para probar el servicio con credenciales reales de WhatsApp."""

import requests
import time

BASE_URL = "http://localhost:8000"

# Tu número de WhatsApp (el que agregaste como tester)
TEST_PHONE = "+541139090008"  # Cambia esto a tu número real si es diferente

def test_health():
    """Prueba health check."""
    print("🔍 Probando Health Check...")
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        print("✅ Servicio funcionando correctamente")
        return True
    else:
        print("❌ Servicio no responde")
        return False

def test_send_text():
    """Prueba envío de mensaje de texto."""
    print(f"\n📤 Enviando mensaje de texto a {TEST_PHONE}...")
    
    response = requests.post(
        f"{BASE_URL}/send/whatsapp",
        json={
            "to": TEST_PHONE,
            "message": "¡Hola! Este es un mensaje de prueba desde el servicio de WhatsApp Integration 🚀",
            "message_type": "text"
        }
    )
    
    result = response.json()
    
    if result.get("success"):
        print(f"✅ Mensaje enviado exitosamente!")
        print(f"📱 Message ID: {result.get('message_id')}")
        print(f"\n🎉 Revisa tu WhatsApp ({TEST_PHONE}) - deberías haber recibido el mensaje!")
        return True
    else:
        print(f"❌ Error al enviar mensaje:")
        print(f"   Error: {result.get('error')}")
        if result.get('details'):
            print(f"   Detalles: {result.get('details')}")
        return False

def test_send_image():
    """Prueba envío de imagen."""
    print(f"\n🖼️  Enviando imagen a {TEST_PHONE}...")
    
    response = requests.post(
        f"{BASE_URL}/send/whatsapp",
        json={
            "to": TEST_PHONE,
            "message": "Aquí está una imagen de prueba desde el servicio 📸",
            "message_type": "image",
            "media_url": "https://picsum.photos/400/300"
        }
    )
    
    result = response.json()
    
    if result.get("success"):
        print(f"✅ Imagen enviada exitosamente!")
        print(f"📱 Message ID: {result.get('message_id')}")
        print(f"\n🎉 Revisa tu WhatsApp - deberías haber recibido la imagen!")
        return True
    else:
        print(f"❌ Error al enviar imagen:")
        print(f"   Error: {result.get('error')}")
        return False

def test_send_with_emojis():
    """Prueba mensaje con emojis y formato."""
    print(f"\n✨ Enviando mensaje con emojis a {TEST_PHONE}...")
    
    message = """¡Hola! 👋

✅ Tu servicio de WhatsApp está funcionando perfectamente
🚀 Puedes enviar mensajes
📸 Puedes enviar imágenes
💬 Sistema de logs activo
🎉 ¡Todo listo para usar!

Equipo 1 - TP Seminario"""
    
    response = requests.post(
        f"{BASE_URL}/send/whatsapp",
        json={
            "to": TEST_PHONE,
            "message": message,
            "message_type": "text"
        }
    )
    
    result = response.json()
    
    if result.get("success"):
        print(f"✅ Mensaje con emojis enviado!")
        print(f"📱 Message ID: {result.get('message_id')}")
        return True
    else:
        print(f"❌ Error: {result.get('error')}")
        return False

def main():
    """Ejecuta todas las pruebas."""
    print("=" * 70)
    print("🧪 PRUEBAS DEL SERVICIO WHATSAPP INTEGRATION - CON CREDENCIALES REALES")
    print("=" * 70)
    print()
    
    # Verificar que el servicio esté corriendo
    if not test_health():
        print("\n❌ El servicio no está corriendo.")
        print("   Ejecuta: ./run.sh")
        return
    
    print("\n" + "=" * 70)
    print("📱 IMPORTANTE: Asegúrate de que el número esté agregado como 'tester'")
    print(f"   Número configurado: {TEST_PHONE}")
    print("=" * 70)
    
    input("\nPresiona ENTER para continuar...")
    
    # Prueba 1: Mensaje simple
    success1 = test_send_text()
    time.sleep(2)
    
    # Prueba 2: Mensaje con emojis
    success2 = test_send_with_emojis()
    time.sleep(2)
    
    # Prueba 3: Imagen
    success3 = test_send_image()
    
    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 70)
    print(f"Mensaje de texto: {'✅ OK' if success1 else '❌ FALLÓ'}")
    print(f"Mensaje con emojis: {'✅ OK' if success2 else '❌ FALLÓ'}")
    print(f"Envío de imagen: {'✅ OK' if success3 else '❌ FALLÓ'}")
    
    if success1 and success2 and success3:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("✅ Tu servicio de WhatsApp está completamente funcional")
    else:
        print("\n⚠️  Algunas pruebas fallaron")
        print("💡 Verifica:")
        print("   - Que el número esté agregado como 'tester' en Meta")
        print("   - Que las credenciales en .env sean correctas")
        print("   - Los logs en: logs/whatsapp_service_*.log")
    
    print("\n📝 Logs del servicio:")
    print(f"   tail -f logs/whatsapp_service_*.log")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Pruebas canceladas por el usuario")
    except requests.exceptions.ConnectionError:
        print("\n\n❌ No se pudo conectar al servicio")
        print("   ¿Está corriendo? Ejecuta: ./run.sh")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
