#!/bin/bash

# Script para ejecutar el servicio de WhatsApp

echo "🚀 Iniciando servicio de WhatsApp Integration..."
echo ""

# Verificar que Poetry esté instalado
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry no está instalado."
    echo "Instálalo con: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Verificar que las dependencias estén instaladas
if [ ! -d ".venv" ] && [ ! -f "poetry.lock" ]; then
    echo "📦 Instalando dependencias..."
    poetry install
    echo ""
fi

# Verificar que exista el archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado. Usando valores por defecto."
    echo "Para configurar WhatsApp Cloud API, edita el archivo .env"
    echo ""
fi

# Crear directorio de logs si no existe
mkdir -p logs

echo "✅ Servicio iniciado en: http://localhost:8000"
echo "📝 Logs en: logs/whatsapp_service_$(date +%Y%m%d).log"
echo ""
echo "Endpoints disponibles:"
echo "  - GET  http://localhost:8000/              (Health check)"
echo "  - GET  http://localhost:8000/webhook/whatsapp  (Webhook verification)"
echo "  - POST http://localhost:8000/webhook/whatsapp  (Receive messages)"
echo "  - POST http://localhost:8000/send/whatsapp     (Send messages)"
echo ""
echo "Presiona Ctrl+C para detener el servicio"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Ejecutar el servicio
poetry run python -m src.whatsapp_service

