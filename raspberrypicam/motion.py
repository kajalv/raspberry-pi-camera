from __future__ import division

import time
import os
import subprocess
import datetime

import picamera
import picamera.array
import numpy as np
import mail_motion

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class CaptureHandler:
    def __init__(self, camera, post_capture_callback=None):
        self.camera = camera
        self.callback = post_capture_callback
        self.detected = False
        self.working = False
        self.i = 0

    def motion_detected(self):
        if not self.working:
            self.detected = True

    def pulse(self):
        if self.detected:
            print "Motion detected, capturing environment"
            self.working = True
            self.detected = False
            self.i += 1

            path = "captures/%s/" % datetime.datetime.now().isoformat()

            os.makedirs(path)

	    self.camera.start_preview()

            for x in range(1, 16):
                filename = "detected-%02d.jpg" % x
                self.camera.capture(path + filename, use_video_port=True)
                print "Captured " + filename

            montage_file = path + 'snapshot.jpg'
            subprocess.call("montage -border 0 -background none -geometry 240x180 " + path + "* " + montage_file, shell=True)

	    self.camera.stop_preview()

            print "Finished capturing"

	    mail_motion.mail_motion_send()

        if self.callback:
            self.callback(montage_file)

        self.working = False


class VectorAnalyser(picamera.array.PiMotionAnalysis):
    def __init__(self, camera, handler):
        super(VectorAnalyser, self).__init__(camera)
        self.handler = handler
        self.first = True

    def analyse(self, a):
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
        ).clip(0, 255).astype(np.uint8)
        if (a > 60).sum() > 50:
            # Ignore the first detection
            if self.first:
                self.first = False
                return
            self.handler.motion_detected()


class MotionDetector:

    def __init__(self, verbose=False, post_capture_callback=None):
        self.verbose = verbose
        self.post_capture_callback = post_capture_callback

    def __print(self, str):
        if self.verbose:
            print str

    def start(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (1280, 960)
            camera.framerate = 10

            self.__print('Booting camera and loading dependencies')
            handler = CaptureHandler(camera, self.post_capture_callback)

            time.sleep(2)

            try:
                self.__print('Surveillance Enabled :')
                camera.start_recording(
                    '/dev/null', format='h264',
                    motion_output=VectorAnalyser(camera, handler)
                )

                while True:
                    handler.pulse()
                    time.sleep(1)
            finally:
                camera.stop_recording()
                self.__print('Camera going offline ...')
