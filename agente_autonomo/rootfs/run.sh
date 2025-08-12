#!/usr/bin/with-contenv bashio
set -e

echo "🔧 Agente Autônomo HA iniciando..."

ACCESS_TOKEN=$(bashio::config 'access_token')
HASS_URL=$(bashio::config 'hass_url')

if [ -z "$ACCESS_TOKEN" ]; then
  echo "❌ ACCESS_TOKEN (Options › access_token) não definido. Abortando."
  exit 1
fi

export ACCESS_TOKEN
export HASS_URL

exec python3 /opt/agent/ha_agent_autonomo.py
