from motion import MotionDetector

# This is the motion detection mode.

def startMotionDet() :
    motion = MotionDetector(verbose=True)
    motion.start()
