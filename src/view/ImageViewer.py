'''
Created on Jan 20, 2015

@author: Decoder
'''
import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sys import path
from PyQt4 import QtGui
from _functools import partial

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
    OptionImages = [
       "C:/Users/Decoder/Desktop/Image Resources for Thesis/pc1.jpg",
       "C:/Users/Decoder/Desktop/Image Resources for Thesis/pc2.jpg",
       "C:/Users/Decoder/Desktop/Image Resources for Thesis/bike.jpg",
       "C:/Users/Decoder/Desktop/Image Resources for Thesis/pencil.jpg",
       "C:/Users/Decoder/Desktop/Image Resources for Thesis/smile.jpg",
       "C:/Users/Decoder/Desktop/Image Resources for Thesis/stocks.jpg"           
        ]
    firstSetImages = [
       "C:/Users/Decoder/Desktop/Image Resources for Thesis/stocks.jpg"
        ]
    secondSetImages = [
        "C:/Users/Decoder/Desktop/Image Resources for Thesis/smile.jpg"
        ]
    thirdSetImages = [
        "C:/Users/Decoder/Desktop/Image Resources for Thesis/pencil.jpg"
        ]
    fourthSetImages = [
        "C:/Users/Decoder/Desktop/Image Resources for Thesis/bike.jpg"
        ]
    fifthSetImages = [
        "C:/Users/Decoder/Desktop/Image Resources for Thesis/pc2.jpg"
        ]
    sixthSetImages = [
        "C:/Users/Decoder/Desktop/Image Resources for Thesis/pc1.jpg",
        "C:/Users/Decoder/Desktop/Image Resources for Thesis/pc2.jpg"
        ]
    seventhSetImages = []
    ImageBundle = [firstSetImages, secondSetImages, thirdSetImages, fourthSetImages, fifthSetImages, sixthSetImages, seventhSetImages]
    

    
    def __init__(self):
        '''
        Constructor
        '''
        super(ImageViewer, self).__init__()
        self.initGUI()
        self.counter = 0
        self.directory = "MAIN"
        self.subDirectory = 0
        
    
    def initGUI(self):
        
        self.mainPicture = QLabel()
        self.mainPicture.setAlignment(Qt.AlignCenter)
        #self.mainPicture.setStyleSheet("QWidget{padding-right: 500px; padding-left: 500px}")
        #self.mainPicture.setGeometry(QRect(500, 500))
        self.moveRight = QLabel("LEFT")
        self.moveRight.setAlignment(Qt.AlignCenter)
        self.moveLeft = QLabel("RIGHT")
        self.moveLeft.setAlignment(Qt.AlignCenter)
        
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.moveRight, 0, 1)
        #grid.addWidget(self.mainPicture, 0, 2)
        grid.addWidget(self.moveLeft, 0, 3)
        
        self.setLayout(grid)
        #self.setStyleSheet("QWidget{background-color: #000000;}")
        #self.showFullScreen()
        self.show()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Left:
            #print("LEFT")
            self.pressEvent("LEFT", self.counter)
            #print(self.directory)
        elif event.key() == Qt.Key_Right:
            #print("RIGHT")
            self.pressEvent("RIGHT", self.counter)
            #print(self.directory)
        elif event.key() == Qt.Key_Space:
            print("COUNTER: " + str(self.counter))
            #print(str(len(self.ImageBundle[self.counter])))
            self.directory = "ENTER"
            #self.pageLocation = self.counter
            self.pressEvent("ENTER", self.counter)
            #print(self.ImageBundle[self.counter][0])
            self.showImages(self.ImageBundle[self.counter][0])
            self.counter = 0
            
            
            
            
    def nextImage(self, imageList):
        if imageList:
            if self.counter == len(imageList):
                self.counter = 0
                #add code for showing image path
                
    def showImages(self, path):
        if path:
            image = QPixmap(path)
            self.mainPicture.setPixmap(image.scaled(self.mainPicture.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation))
            
    def pressEvent(self, objSource, pageLocation):
#         print objSource
#         print self.directory
        #self.directory = pageLocation
        if(objSource == "RIGHT"):
            print ("MAIN PAGELOCATION: "+ str(pageLocation))
            if(self.directory == "MAIN"):
                self.counter = self.counter + 1
                #print(str(len(self.OptionImages)))
                if(self.counter > (len(self.OptionImages)-1)):
                    self.counter = 0
                self.showImages(self.OptionImages[self.counter])
                #print("RIGHT: " + str(self.counter))
            elif(self.directory == "ENTER"):
                #self.showImages(self.ImageBundle[self.counter[self.counter]])
                #print(self.ImageBundle[pageLocation][self.counter])
                #print(len(self.ImageBundle[pageLocation]))
                self.counter = self.counter + 1
                print(self.counter)
#                 if(self.counter > (len(self.ImageBundle[pageLocation])-1)):
#                     self.counter = 0
        elif (objSource == "LEFT"):
            print ("MAIN PAGELOCATION: "+ str(pageLocation))
            if (self.directory == "MAIN"):
                self.counter = self.counter - 1
                if(self.counter < 0):
                    self.counter = (len(self.OptionImages)-1)
                self.showImages(self.OptionImages[self.counter])
                    #print("LEFT: " + str(self.counter))
            elif(self.directory == "ENTER"):
                #num = int(pageLocation)
                #self.counter = 0
                #self.showImages(self.ImageBundle[self.counter[self.counter]])
                #print(len(self.ImageBundle[pageLocation]))
                self.counter = self.counter - 1
                print(self.counter)
                #print(len(self.ImageBundle[self.counter]))
            
      
    
        