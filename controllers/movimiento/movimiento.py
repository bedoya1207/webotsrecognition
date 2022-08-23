"""movimiento controller."""

# You may need to import some classes of the controller module. Ex:
from controller import Robot
from controller import Camera
from preprocesamiento import analizar
import numpy as np
import cv2 as cv
TIME_STEP = 64
robot = Robot()
camera = robot.getDevice('cam')
camera.enable(TIME_STEP)
camera.recognitionEnable(TIME_STEP)

ds = []
dsNames = ['ds_right', 'ds_left']
for i in range(2):
    ds.append(robot.getDevice(dsNames[i]))
    ds[i].enable(TIME_STEP)
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)
avoidObstacleCounter = 0
contador = 0
while robot.step(TIME_STEP) != -1:
    
    if(len(camera.getRecognitionObjects())>0):
        contador = contador +1
        imagen = camera.getImageArray()
        img = np.array(imagen)
        cv.imwrite("imagen.png",img)
        img = cv.imread("imagen.png")
        img = cv.cvtColor(img,cv.COLOR_RGB2BGR)
        cv.imwrite("imagen.png",img)
        valorP = analizar("paint.png","imagen.png")
        valorC = analizar("can.png","imagen.png")
        valorW = analizar("water.png","imagen.png")        
        if(valorC>valorW and valorC>valorP):
            print("Es una lata")
        else:
            if(valorW>valorC and valorW>valorP):
                print("Es una botella")
            else:
                if(valorP>valorC and valorP>valorW):
                    print("Es un reloj")
    else:
        print("No hay objetos.")
    leftSpeed = 1.0
    rightSpeed = 1.0
    if avoidObstacleCounter > 0:
        avoidObstacleCounter -= 1
        leftSpeed = 1.0
        rightSpeed = -1.0
    else:  # read sensors
        for i in range(2):
            if ds[i].getValue() < 950.0:
                avoidObstacleCounter = 100
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(rightSpeed)
    