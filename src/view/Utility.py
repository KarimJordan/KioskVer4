'''
Created on Jan 20, 2015

@author: Decoder
'''
def isExtensionSupported(fileName):
    #Checks to see if image is supported
    if fileName.endswith('PNG') or fileName.endswith('png') or fileName.endswith('JPG') or fileName.endswit('jpg'):
        return True