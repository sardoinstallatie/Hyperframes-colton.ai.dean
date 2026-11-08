#!/bin/bash
sleep 3
cd /home/claude/hyperframes-colton.ai.dean/video-projects/2026-11-08-d00-funda-rheden
export HYPERFRAMES_BROWSER_PATH=/usr/bin/google-chrome
npx hyperframes render --quality standard --fps 25 --output renders/final-A.mp4 > work/render.log 2>&1
echo "EXIT $?" >> work/render.log
