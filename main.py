from pyimagesearch.keyclipwriter import KeyClipWriter
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

from upload import upload

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to output video file")
ap.add_argument("-p", "--picamera", type=str, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=20,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="MJPG",
	help="codec of output video")
ap.add_argument("-b", "--bufferSize", type=int, default=32,
    help="buffer size of video clip writter")
#um buffer size maior pega uma quantidade maior de minutos antes e depois do evento
args = vars(ap.parse_args())

print("[INFO] Esquentando a câmera")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
#vs = VideoStream('rtsp://admin:cemig2019@192.168.2.126:554/').start()
time.sleep(2.0)

kcw = KeyClipWriter(bufSize=args["bufferSize"])
consecFrames = 0 #conta o numero de frames que não contém um evento de interesse

while True:
    
    #pega o frame atual, redimensiona
    frame = vs.read()
    frame = imutils.resize(frame, width = 900)
    updateConsecFrames = True

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == ord('x'):
        print("Botão Pressionado")
        consecFrames = 0

        if not kcw.recording:
            timestamp = datetime.datetime.now()
            p = "{}/{}.avi".format(args["output"], timestamp.strftime("%d/%m/%Y-%H:%M:%S"))
            kcw.start(p, cv2.VideoWriter_fourcc(*args["codec"]),args["fps"])
    

    if updateConsecFrames:
        consecFrames += 1

    kcw.update(frame)

    if kcw.recording and consecFrames == args["bufferSize"]:
        kcw.finish()



if kcw.recording:
    kcw.finish()

cv2.destroyAllWindows()
vs.stop()
upload().uparVideos('output')