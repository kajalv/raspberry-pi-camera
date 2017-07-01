import time
import picamera
import camProperties
import mail_android
from datetime import datetime


properties = camProperties.cameraProperties(10, 20, (15 * 60), 1280, 960, (40 * 1024 * 1024))

def captureImage() :

    #tim = datetime.now()
    filename = "captured-image.jpg" #capture-%04d%02d%02d-%02d%02d%02d.jpg % (tim.year, tim.month, tim.day, tim.hour, tim.minute, tim.second)

    with picamera.PiCamera() as camera :

        width, height = properties.getSaveWidthAndHeight()
        camera.resolution = (width, height)
        camera.brightness = properties.getBrightness()
        camera.start_preview()
        time.sleep(2)
        camera.capture(filename)
        mail_android.mail_android_send()

def do_command(cmd) :

    # For the purpose of testing, only a few commands are enabled.
    # This can be improved to interpret commands in a more robust manner instead of the explicit statements below.

    if cmd == "take picture" :
        captureImage()

    elif cmd == "increase brightness" :
        properties.increaseBrightness()

    # Command is increase brightness (someNumber)
    elif (len(cmd.split(" ")) == 3) and ("increase" in cmd.split(" ")) and ("brightness" in cmd.split(" ")) :
        properties.increaseBrightness(int(cmd.split(" ")[2]))

    elif cmd == "testing query" :
	print cmd + " is working."

    # Command is set brightness (someNumber)
    elif "set brightness" in cmd and (len(cmd.split(" ")) == 3) :
        properties.setBrightness(int(cmd.split(" ")[2]))

    else :
	print "Invalid command!"

    print "Command is " + cmd
