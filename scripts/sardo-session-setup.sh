#!/usr/bin/env bash
# Sardo — sessie-setup voor de cloud-omgeving.
# Draai dit aan het begin van ELKE nieuwe chat in het project "CONTENT: Short-Form editor".
# De cloud reset na elke sessie, dus dit script bouwt alles opnieuw op:
#   1. npm-dependencies
#   2. Chromium headless shell zoeken en HYPERFRAMES_BROWSER_PATH zetten (de eigen download van Hyperframes is geblokkeerd)
#   3. Parakeet v3 (Nederlandse spraak-naar-tekst) via GitHub installeren (huggingface.co is geblokkeerd)
#   4. Korte controle
#
# Gebruik:  source scripts/sardo-session-setup.sh
#   (source, niet bash — dan blijft HYPERFRAMES_BROWSER_PATH in je shell staan)

set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "▸ 1/4 npm install"
npm install --silent >/dev/null 2>&1 && echo "  ok" || echo "  ⚠ npm install gaf een fout"

echo "▸ 2/4 Chromium zoeken"
BROWSER=""
for c in \
  /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell \
  /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell \
  /opt/pw-browsers/chromium-*/chrome-linux*/chrome; do
  [ -x "$c" ] && BROWSER="$c" && break
done
if [ -n "$BROWSER" ]; then
  export HYPERFRAMES_BROWSER_PATH="$BROWSER"
  grep -q HYPERFRAMES_BROWSER_PATH ~/.bashrc 2>/dev/null || echo "export HYPERFRAMES_BROWSER_PATH=\"$BROWSER\"" >> ~/.bashrc
  echo "  ok: $BROWSER"
else
  echo "  ⚠ geen Chromium gevonden — probeer: npx hyperframes browser ensure"
fi

echo "▸ 3/4 Parakeet v3 (Nederlands)"
MODEL_DIR="$HOME/.cache/hyperframes/parakeet/parakeet-tdt-0.6b-v3-int8"
if [ -f "$MODEL_DIR/encoder.int8.onnx" ] && [ -f "$MODEL_DIR/tokens.txt" ]; then
  echo "  staat er al"
else
  mkdir -p "$MODEL_DIR"
  TMP="$(mktemp -d)"
  URL="https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8.tar.bz2"
  echo "  downloaden (~460 MB, duurt 1-3 min)…"
  if curl -sSL --fail -o "$TMP/p.tar.bz2" "$URL"; then
    tar -xjf "$TMP/p.tar.bz2" -C "$TMP"
    SRC="$(find "$TMP" -maxdepth 2 -type d -name 'sherpa-onnx-nemo-parakeet*' | head -1)"
    cp "$SRC"/encoder.int8.onnx "$SRC"/decoder.int8.onnx "$SRC"/joiner.int8.onnx "$SRC"/tokens.txt "$MODEL_DIR"/
    echo "  ok"
  else
    echo "  ⚠ download mislukt — transcriptie werkt niet. Meld dit aan Peter."
  fi
  rm -rf "$TMP"
fi
( cd "$MODEL_DIR" && sha256sum encoder.int8.onnx 2>/dev/null | grep -q acfc2b4456377e15d04f0243af540b7fe7c992f8d898d751cf134c3a55fd2247 ) \
  && echo "  checksum encoder ok" || echo "  ⚠ checksum encoder klopt niet"
# Runtime (sherpa-onnx-node, via npm) installeren. Het model staat er al, dus deze stap
# slaat de geblokkeerde huggingface-download over en controleert alleen.
echo "  runtime installeren…"
timeout 400 npx --yes hyperframes models install parakeet 2>&1 | grep -q "Parakeet installed" \
  && echo "  Parakeet klaar" || echo "  ⚠ Parakeet-runtime niet gelukt — draai: npx hyperframes models install parakeet"

echo "▸ 4/4 controle"
which ffmpeg >/dev/null && echo "  ffmpeg ok" || echo "  ⚠ ffmpeg ontbreekt"
echo
echo "Klaar. Transcriberen:  npx hyperframes transcribe <bestand> --engine parakeet --language nl --json"
