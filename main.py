from pyimagesearch.keyclipwriter import KeyClipWriter
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

from upload import upload
from menu import Menu

mn = Menu()

print("[INFO] Esquentando a câmera")
vs = VideoStream(usePiCamera=mn.parametros['camera'] > 0).start()
time.sleep(2.0)

kcw = KeyClipWriter(mn.parametros['buffer'])
consecFrames = 0 #conta o numero de frames que não contém um evento de interesse

while True:

    #pega o frame atual, redimensiona
    frame = vs.read()
    frame = imutils.resize(frame, width = mn.parametros['resolucao_w'])
    updateConsecFrames = True

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'): #finaliza o monitoramento
        break
    
    if key == ord('x'): #evento que aciona a região de interesse
        print("Botão Pressionado...efetuando a gravação, aguarde alguns segundos\n")
        consecFrames=0

        if not kcw.recording:
            timestamp = datetime.datetime.now()
            p = "{}/{}.avi".format('output', timestamp.strftime("%d-%m-%Y-%H:%M:%S"))
            kcw.start(p, cv2.VideoWriter_fourcc(*mn.parametros['codec']),mn.parametros['fps'])
    
    if updateConsecFrames:
        consecFrames += 1

    kcw.update(frame)

    if kcw.recording and consecFrames == mn.parametros['buffer']:
        kcw.finish()

if kcw.recording:
    kcw.finish()

cv2.destroyAllWindows()
vs.stop()

up = upload()
if mn.enviar_drive() and up.internet():
    up.uparVideos('output')
else:
    print("[INFO] O computador não possui internet neste momento, o arquivo será salvo no disco")
    mn.__init__()



