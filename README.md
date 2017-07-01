# Raspberry Pi Home Security System

This module aims to create a simple surveillance system with the help of a Raspberry Pi device. The system can be monitored and controlled remotely using an Android smartphone.

The module has been tested on a Raspberry Pi device with an attached PiCamera, and with the Android application running on a Samsung Galaxy S3 smartphone. To use the module, the Python camera module files must be transferred to the Pi.

## Functional Details

There are two modes of functioning of the system. One PiCam can run only one of the two modes at a time, so two cameras will be required to run both modes simultaneously.

- Explicit mode

  - In this mode, the user explicitly launches the helper Android application on his/her smartphone and issues a command to take a picture. The picture is taken and emailed back to the user, and can be seen on the smartphone.


- Motion detection mode

  - In this mode, the camera takes a series of pictures when it detects motion that passes a configured threshold. A montage of all the photos is created and emailed to the user, and can be seen on his/her smartphone.

## Implementation Details

- Raspberry Pi modules

  - The remote connection to the Raspberry Pi from the Android application is achieved with the help of Weaved: https://www.weaved.com/raspberry-pi-remote-connection/
  - Modules are written to launch the pi camera, take pictures, generate a montage, and email a picture back to the configured email ID.


- Android application

  - The helper Android application written in Java helps to control the system remotely. It is to be launched manually by the user whenever desired. The application implements a speech-to-text (STT) module which uses a Voice Recognition API to process spoken commands given by the user.
