#!/bin/bash
sleep 3
export HYPERFRAMES_BROWSER_PATH=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell | head -1)
cd "$(dirname "$0")/A"
mkdir -p renders
npx hyperframes render --quality standard --fps 25 --output renders/final.mp4 > renders/render.log 2>&1
echo DONE >> renders/render.log
