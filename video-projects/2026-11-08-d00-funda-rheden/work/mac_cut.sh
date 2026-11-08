set -e
cd $HOME/mnt/Documents/videos/raw
SRC=DJI_20261108153835_0119_D.MP4
mkdir -p _work/0119/seg
[ -s _work/0119/seg/s00.mp4 ] || ffmpeg -y -v error -ss 44.240 -t 4.845 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s00.mp4
[ -s _work/0119/seg/s01.mp4 ] || ffmpeg -y -v error -ss 3.360 -t 6.809 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s01.mp4
[ -s _work/0119/seg/s02.mp4 ] || ffmpeg -y -v error -ss 27.000 -t 3.189 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s02.mp4
[ -s _work/0119/seg/s03.mp4 ] || ffmpeg -y -v error -ss 59.630 -t 6.820 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s03.mp4
[ -s _work/0119/seg/s04.mp4 ] || ffmpeg -y -v error -ss 75.150 -t 3.100 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s04.mp4
[ -s _work/0119/seg/s05.mp4 ] || ffmpeg -y -v error -ss 85.870 -t 4.776 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s05.mp4
[ -s _work/0119/seg/s06.mp4 ] || ffmpeg -y -v error -ss 94.710 -t 3.747 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s06.mp4
[ -s _work/0119/seg/s07.mp4 ] || ffmpeg -y -v error -ss 109.230 -t 4.220 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s07.mp4
[ -s _work/0119/seg/s08.mp4 ] || ffmpeg -y -v error -ss 122.980 -t 4.632 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s08.mp4
[ -s _work/0119/seg/s09.mp4 ] || ffmpeg -y -v error -ss 144.100 -t 9.531 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s09.mp4
[ -s _work/0119/seg/s10.mp4 ] || ffmpeg -y -v error -ss 172.420 -t 9.182 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s10.mp4
[ -s _work/0119/seg/s11.mp4 ] || ffmpeg -y -v error -ss 187.010 -t 2.658 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s11.mp4
[ -s _work/0119/seg/s12.mp4 ] || ffmpeg -y -v error -ss 279.460 -t 8.682 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s12.mp4
[ -s _work/0119/seg/s13.mp4 ] || ffmpeg -y -v error -ss 292.020 -t 5.257 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s13.mp4
[ -s _work/0119/seg/s14.mp4 ] || ffmpeg -y -v error -ss 304.930 -t 5.920 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s14.mp4
[ -s _work/0119/seg/s15.mp4 ] || ffmpeg -y -v error -ss 321.250 -t 7.178 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s15.mp4
[ -s _work/0119/seg/s16.mp4 ] || ffmpeg -y -v error -ss 356.850 -t 5.800 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s16.mp4
[ -s _work/0119/seg/s17.mp4 ] || ffmpeg -y -v error -ss 367.680 -t 4.334 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s17.mp4
[ -s _work/0119/seg/s18.mp4 ] || ffmpeg -y -v error -ss 375.520 -t 9.450 -i $SRC -vf scale=1080:-2 -r 25 -c:v libx264 -preset ultrafast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart _work/0119/seg/s18.mp4
