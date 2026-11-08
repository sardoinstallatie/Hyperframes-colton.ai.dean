cd "$HOME/mnt/Documents/videos/raw/_work/0123" || exit 1
SRC="$HOME/mnt/Documents/videos/raw/DJI_20261108161109_0123_D.MP4"
cut() { ffmpeg -y -v error -ss $(python3 -c "print(max(0,$1-1))") -i "$SRC" -ss $(python3 -c "print(min(1,$1))") -t $(python3 -c "print(round($2-$1,3))") -vf "scale=1080:1920,fps=25,setsar=1" -af "aresample=48000" -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 $3 2>>cut.log; }



cut 317.00 319.82 q20.mp4
FILES="p00 p01 p02 p03 p04 p05 p06 p07 p08 p09 p10 p11 p12 q13 q14 p15 q16 p19 q20 p21 p22 p23 p24 p25 p26 p27"
IN=""; FC=""; i=0
for f in $FILES; do
  IN="$IN -i $f.mp4"
  D=$(ffprobe -v error -select_streams v -show_entries stream=duration -of csv=p=0 $f.mp4)
  FC="$FC[$i:v]setpts=PTS-STARTPTS[v$i];[$i:a]atrim=0:$D,asetpts=PTS-STARTPTS,apad=whole_dur=$D,afade=t=in:d=0.012,afade=t=out:st=$(python3 -c "print(round($D-0.02,3))"):d=0.02[a$i];"
  i=$((i+1))
done
CC=""; for j in $(seq 0 $((i-1))); do CC="$CC[v$j][a$j]"; done
FC="$FC${CC}concat=n=$i:v=1:a=1[v][a]"
ffmpeg -y -v error $IN -filter_complex "$FC" -map "[v]" -map "[a]" -r 25 -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart source.mp4 2>>cut.log
ffprobe -v error -show_entries stream=codec_type,duration -of csv=p=0 source.mp4
ls -la source.mp4; md5sum source.mp4
