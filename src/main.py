'''
Created on Jan 20, 2015

@author: Decoder
'''
import sys
from PyQt4 import QtGui
from view.ImageViewer import ImageViewer


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    play = ImageViewer()
    sys.exit(app.exec_())