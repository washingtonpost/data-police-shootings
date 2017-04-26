ffmpeg -framerate 20 -start_number 1 -i frames/%d.png -c:v libx264 -r 30 -pix_fmt yuv420p fatalities.mp4
