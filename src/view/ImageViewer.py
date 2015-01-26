'''
Created on Jan 20, 2015

@author: Decoder
'''

#count kung ilan yung gumamit, via text file.
import sys
import os
import string
import time
import RPi.GPIO as GPIO

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
from sys import path
from _functools import partial 
from datetime import datetime

   
def clickable(widget):

    class Filter(QObject):
    
        clicked = pyqtSignal()
        
        def eventFilter(self, obj, event):
        
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True
            
            return False
    
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


class ImageViewer(QWidget):
    '''
    classdocs
    '''
    step = 0
    state = "INIT"
   
    
    OptionImages = [
       "C:/Users/Decoder/Desktop/Kiosk System/Folder/Chrysanthemum.jpg",
       "C:/Users/Decoder/Desktop/Kiosk System/Folder/Desert.jpg", 
       "C:/Users/Decoder/Desktop/Kiosk System/Folder/Hydrangeas.jpg", 
       "C:/Users/Decoder/Desktop/Kiosk System/Folder/Jellyfish.jpg", 
       "C:/Users/Decoder/Desktop/Kiosk System/Folder/Koala.jpg", 
       "C:/Users/Decoder/Desktop/Kiosk System/Folder/Lighthouse.jpg", 
       "C:/Users/Decoder/Desktop/Kiosk System/Folder/Penguins.jpg",           
        ]
    firstOptionPath = "C:/Users/Decoder/Desktop/Kiosk System/Folder/FirstOption"
    secondOptionPath = "C:/Users/Decoder/Desktop/Kiosk System/Folder/SecondOption"
    thirdOptionPath = "C:/Users/Decoder/Desktop/Kiosk System/Folder/ThirdOption"
    fourthOptionPath = "C:/Users/Decoder/Desktop/Kiosk System/Folder/FourthOption"
    fifthOptionPath = "C:/Users/Decoder/Desktop/Kiosk System/Folder/FifthOption"
    sixthOptionPath = "C:/Users/Decoder/Desktop/Kiosk System/Folder/SixthOption"
    seventhOptionPath = "C:/Users/Decoder/Desktop/Kiosk System/Folder/SeventhOption"
    
    #sounds
    announcements = "C:/Users/Decoder/Desktop/Image Resources for Thesis/Announcements.wav"
    activities = "C:/Users/Decoder/Desktop/Image Resources for Thesis/Activities.wav"
    clubActivities = "C:/Users/Decoder/Desktop/Image Resources for Thesis/ClubActivties.wav"
    examinations = "C:/Users/Decoder/Desktop/Image Resources for Thesis/ExaminationSchedule.wav"
    facultyMembers = "C:/Users/Decoder/Desktop/Image Resources for Thesis/FacultyMembers.wav"
    fyi = "C:/Users/Decoder/Desktop/Image Resources for Thesis/fyi.wav"
    schedule = "C:/Users/Decoder/Desktop/Image Resources for Thesis/Schedule.wav"
    
    soundList = [announcements, activities, clubActivities, examinations, facultyMembers, fyi, schedule]
    
    OptionFolders = [
        firstOptionPath,
        secondOptionPath,
        thirdOptionPath,
        fourthOptionPath,
        fifthOptionPath,
        sixthOptionPath,
        seventhOptionPath]
    
    @pyqtSlot()
    def count(self):
        print(str(self.step))
        if(self.step >= len(self.OptionImages)):
            self.step = 0
        self.showImages(self.OptionImages[self.step])
        self.step = self.step + 1
    
    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(ImageViewer, self).__init__()
        #QWidget.__init__(self,  parent)
        self.timer = QTimer()
        self.connect(self.timer, SIGNAL("timeout()"),self, SLOT("count()"))
        self.timer.start(1000)
        self.initGUI()
        #self.checkDirectory("C:/Users/Public/Pictures/Sample Pictures/SecondOption")
        #self.checkIfFolder("C:/Users/Public/Pictures/Sample Pictures/SecondOption")
        self.counter = 0
        self.directory = "MAIN"
        self.subDirectory = 0
        #self.startSlideShow(self.OptionImages)
        self.mainFileCount = []
        self.mainFileList = []
        self.subFileCount = []
        self.subFileList = []
        self.selfFileList = []
        self.mainFileNames = []
        self.subFolderList = []
        self.mainFolderList = []
        self.messageCounter = 0
        
        
    
    def initGUI(self):
        
        self.mainPicture = QLabel()
        self.mainPicture.setAlignment(Qt.AlignCenter)
        #self.mainPicture.setStyleSheet("QWidget{width: 100%; height: 100%; padding:0; margin: 0}")
        #self.mainPicture.setGeometry(QRect(500, 500))
        #self.showImages(self.OptionImages[0])
        #self.playSound(self.soundList[0]) 
        self.moveRight = QLabel("LEFT")
        self.moveRight.setAlignment(Qt.AlignCenter)
        self.moveLeft = QLabel("RIGHT")
        self.moveLeft.setAlignment(Qt.AlignCenter)
        
        
        grid = QGridLayout()
        grid.setSpacing(10)
        #grid.addWidget(self.moveRight, 0, 1)
        grid.addWidget(self.mainPicture, 0, 2)
        #grid.addWidget(self.moveLeft, 0, 3)
        
        self.setLayout(grid)
        #self.setStyleSheet("QWidget{background-color: #000000;}")
        self.showFullScreen()
        #self.show()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Left:
            print (self.directory)
            self.pressEventII("LEFT", self.directory)
        elif event.key() == Qt.Key_Right:
            print (self.directory)
            self.pressEventII("RIGHT", self.directory)
        elif event.key() == Qt.Key_Space:
            self.pressEventII("ENTER", self.directory)
        elif event.key() == Qt.Key_Down:
            seq = (str(self.messageCounter), " Logged at")
            self.logMessage(''.join(seq))
            self.messageCounter = self.messageCounter + 1
        elif event.key() == Qt.Key_Up:
            if(self.state == "INIT"):
                self.timer.stop()
                self.showImages(self.OptionImages[0])
                self.playSound(self.soundList[0])
                self.state = "STOP"
                seq = (str(self.messageCounter), " Logged at")
                self.logMessage(''.join(seq))
                self.messageCounter = self.messageCounter + 1
            else:
                None
            
                
    def showImages(self, path):
        if path:
            image = QtGui.QImage(path)
            pp = QtGui.QPixmap.fromImage(image)
            #image = QPixmap(path)
            self.mainPicture.setPixmap(pp.scaled(self.mainPicture.size(),
                Qt.IgnoreAspectRatio, 
                Qt.FastTransformation))
            
    def pressEventII (self, action, location):
        if(location == "MAIN"):
            print(location)
            if(action == "LEFT"):
                self.counter = self.counter - 1
                if(self.counter < 0):
                    self.counter = (len(self.OptionImages)-1)
                self.showImages(self.OptionImages[self.counter])
                self.playSound(self.soundList[self.counter])
                print("MAIN " + str(self.counter))
            elif(action == "RIGHT"):
                self.counter = self.counter + 1
                if(self.counter > (len(self.OptionImages)-1)):
                    self.counter = 0
                self.showImages(self.OptionImages[self.counter])
                self.playSound(self.soundList[self.counter])
                print("MAIN " + str(self.counter))
            elif(action == "ENTER"):
                self.directory = "SUB"
                
                mainSubDirs, MainfileCounters = self.checkDirectory(self.OptionFolders[self.counter])
                mainFileNames = self.returnFileList(self.OptionFolders[self.counter])
                mainFolder = self.checkIfFolder(self.OptionFolders[self.counter])
                self.mainFolderList = mainFolder
                self.mainFileNames = mainFileNames
                self.mainFileCount = MainfileCounters
                self.mainFileList = mainSubDirs
                self.counter = 0
                self.showImages(self.mainFileList[0] + "/" + self.mainFileNames[0])
                print(self.mainFileList[0] + "/" + self.mainFileNames[0])
                print(self.mainFileNames)
                print(self.mainFolderList)
        elif(location == "SUB"):
            print(location)
            if(action == "LEFT"):
                self.subDirectory = self.subDirectory - 1 
                if(self.subDirectory < 0):
                    self.subDirectory = (self.mainFileCount[0]-1)
                self.showImages(self.mainFolderList[self.subDirectory]+".jpg")
                print self.mainFolderList[self.subDirectory]
                print(self.mainFileList[self.subDirectory] + "/n" + self.mainFileNames[self.subDirectory])  
            elif(action == "RIGHT"):
                self.subDirectory = self.subDirectory + 1
                if(self.subDirectory > (self.mainFileCount[0]-1)):
                    self.subDirectory = 0
                self.showImages(self.mainFolderList[self.subDirectory]+".jpg")
                #self.showImages(self.mainFileList[self.subDirectory] + "/" + self.mainFileNames[self.subDirectory])    
                print self.mainFolderList[self.subDirectory]
                print(self.mainFileList[self.subDirectory] + "/n" + self.mainFileNames[self.subDirectory]) 
            elif(action == "ENTER"):
                #print(self.subDirectory)
                #print(self.mainFolderList[self.subDirectory])
                if(self.subDirectory == 0):
                    print "SJKLAHA"
                    self.counter = 0
                    self.directory = "MAIN"
                    self.showImages(self.OptionImages[0])
                    self.playSound(self.soundList[0])
                else:
                    self.subFileList, self.subFileCount = self.checkDirectory(self.mainFolderList[self.subDirectory])
                    self.selfFileList = self.returnFileList(self.mainFolderList[self.subDirectory])
                    self.subFolderList = self.checkIfFolder(self.mainFolderList[self.subDirectory])
                    self.mainFolderList = self.subFolderList
                    self.mainFileCount = self.subFileCount
                    self.mainFileNames = self.selfFileList
                    self.subDirectory = 0
#                 print(self.mainFileList)
#                 print(self.mainFileCount)
                    print(self.mainFileList[0] + "/" + self.mainFileNames[0])
                    self.showImages(self.mainFolderList[self.subDirectory]+".jpg")
                    print(self.mainFolderList)
                    print(self.mainFileNames)
            
    def checkDirectory(self, path):
        rootList = []
        fileCountList = []
        for root, sub, files in os.walk(path):
            fileCounter = 0
            if(os.path.isdir(path)):
               for fileName in files:
                   if(fileName.endswith('jpg') or fileName.endswith('JPG')):
                       fileCounter = fileCounter + 1
                       #print("fileName: " + fileName)
               rootDir = string.replace(root, "//", "/")
               rootList.append(rootDir)
               fileCountList.append(fileCounter)
#         print rootList
#         print fileCountList
        return rootList, fileCountList
    
    def checkIfFolder(self, path):
        folderList = []
        for fileNames in os.listdir(path):
            if(os.path.isdir(path + "/" +fileNames)):
                folderList.append(path + "/" + fileNames)
        return folderList
    
    def returnFileList(self, path):
        fileNameList = []
        for fileNames in os.listdir(path):
            if fileNames.endswith('jpg') or fileNames.endswith('JPG'):
                fileNameList.append(fileNames)
        return fileNameList
    
    def playSound(self, path):
        QSound.play(path)
        
    def logMessage(self, message):
        path = "C:/Users/Decoder/Desktop/Kiosk System/Folder/logs.txt"
        if(os.path.exists(path)):
            logFile = open(path, "ab")
            seq = (message, " :", str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), "\n")
            logFile.write(''.join(seq))
            logFile.close()
        else:
            logFile = open(path, "w")
            seq = (message, " :", str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), "\n")
            logFile.write(''.join(seq))
            logFile.close()
            
    def ultrasonicSensor(self, trigger, echo):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(trigger, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)
        GPIO.output(trigger, False)
        time.sleep(2)
        GPIO.output(trigger, True)
        time.sleep(0.00001)
        GPIO.output(trigger, False)
        #start = time.time()
        while GPIO.input(echo) == 0:
            start = time.time()
        while GPIO.input(echo) == 1:
            stop = time.time()
        elapsed = stop - start
        distance = elapsed * 17150 #distance returned is in centimeter
        distance = distance / 2
        return distance
        GPIO.cleanup()
        
    def passiveInfraSensor(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)
        try:
            time.sleep(2)
            while True:
                if GPIO.input(pin):
                    return True
                time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
        