#!/bin/bash
sleep 3
cd /home/claude/hyperframes-colton.ai.dean/video-projects/2026-11-08-d00-funda-leeuwarden
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
npx hyperframes render --quality "$1" --fps 25 --output "renders/$2" > "renders/$2.log" 2>&1
echo "EXIT $?" >> "renders/$2.log"
