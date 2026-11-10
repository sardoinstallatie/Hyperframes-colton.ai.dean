#!/bin/bash
sleep 3
cd /home/claude/hyperframes-colton.ai.dean/video-projects/2026-11-08-d19-funda-berg-en-dal
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
npx hyperframes render --quality standard --fps 25 --output renders/final-A-v3.mp4 > work/render.log 2>&1
echo "EXIT $?" >> work/render.log
