
# Class contains all camera properties required to carry out surveillance.
# This will ensure that the changes made are applied from there on for all the images captured.
class cameraProperties :

    def __init__(self, threshold, sensitivity, forceCaptureTime, width, height, diskSpace) :

        self.threshold = threshold # Threshold (how much a pixel has to change by to be marked as "changed")
        self.sensitivity = sensitivity # Sensitivity (how many changed pixels before capturing an image)
        self.forceCapture = True # ForceCapture (whether to force an image to be captured every forceCaptureTime seconds)
        self.forceCaptureTime = forceCaptureTime
        self.saveWidth = width
        self.saveHeight = height
        self.diskSpace = diskSpace
        self.brightness = 50 #Ranges from 1 to 100. Default brightness : 50


    def getThreshold(self) :

        return self.threshold

    def  getSensitivity(self) :

        return self.sensitivity

    def getSaveWidthAndHeight(self) :

        return self.saveWidth, self.saveHeight

    def getDiskSpaceToReserve(self) :

        return self.diskSpace

    def setBrightness(self, brightness) :

        self.brightness = brightness

    def getBrightness(self) :

        return self.brightness

    def increaseBrightness(self, increment=5) :

        self.brightness = self.brightness + increment

    def checkForceCapture(self) :

        return self.forceCapture

    def setForceCapture(self, bool_val) :

        self.forceCapture = bool_val

    def getForceCaptureTime(self) :

        return self.forceCaptureTime
