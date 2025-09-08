#!/bin/bash
# Script para poblar la base de datos de QueenMusic API
# Requiere que el servidor Flask esté corriendo en localhost:5000

API_URL="http://localhost:5000/songs"

songs=(
  '{"name":"Bohemian Rhapsody","album":"A Night at the Opera","year":1975}'
  '{"name":"We Will Rock You","album":"News of the World","year":1977}'
  '{"name":"We Are the Champions","album":"News of the World","year":1977}'
  '{"name":"Somebody to Love","album":"A Day at the Races","year":1976}'
  '{"name":"Don’t Stop Me Now","album":"Jazz","year":1978}'
  '{"name":"Another One Bites the Dust","album":"The Game","year":1980}'
  '{"name":"Radio Ga Ga","album":"The Works","year":1984}'
  '{"name":"Under Pressure","album":"Hot Space","year":1982}'
  '{"name":"Killer Queen","album":"Sheer Heart Attack","year":1974}'
  '{"name":"I Want to Break Free","album":"The Works","year":1984}'
)

echo "🚀 Insertando canciones en la API $API_URL"
for song in "${songs[@]}"; do
  echo "➡️  Insertando: $song"
  curl -s -X POST "$API_URL" \
       -H "Content-Type: application/json" \
       -d "$song"
  echo -e "\n---"
done

echo "✅ Carga completada."