#!/bin/bash
# roda as 3 arquiteturas cliente-servidor (serial/concorrente/pool) para os 3 tamanhos, 2 clientes cada
set -e
cd "$(dirname "$0")"

TAMANHOS=(5 50 500)
declare -A PORTAS=( [serial]=9001 [concorrente]=9002 [pool]=9003 )
ARQS=(serial concorrente pool)

matar_porta() {
  local porta=$1
  local pid=$(netstat -ano | grep "LISTENING" | grep ":$porta " | awk '{print $NF}' | head -1)
  if [ -n "$pid" ]; then
    taskkill //F //PID "$pid" > /dev/null 2>&1 || true
  fi
}

for arq in "${ARQS[@]}"; do
  porta=${PORTAS[$arq]}
  for mb in "${TAMANHOS[@]}"; do
    echo "=== $arq - ${mb}MB ==="
    TAMANHO_MB=$mb node_modules/.bin/tsx "src/$arq/server.ts" &
    sleep 1.5

    TAMANHO_MB=$mb node_modules/.bin/tsx "src/$arq/client.ts" 1 &
    C1=$!
    TAMANHO_MB=$mb node_modules/.bin/tsx "src/$arq/client.ts" 2 &
    C2=$!
    wait $C1 $C2

    matar_porta $porta
    sleep 0.5
  done
done

echo "=== concluido ==="
cat resultados.csv
