# -*- coding: utf-8 -*-

import cv2
import numpy as np
import Tkinter as tk
import tkFont
import json
import time
import sys
from os import listdir, path, makedirs, remove
from PIL import Image
from PIL import ImageTk
import utils_tool 
import imgProcess_tool

class jump_detect():
    def __init__(self, arg_savePath, arg_saveParaPath):
        self._savePath= arg_savePath
        self._backgroundName= self._savePath+'background_0.jpg'
        self._saveParaPath= arg_saveParaPath
        self._fgbg = cv2.BackgroundSubtractorMOG()
        self._threshold_graylevel=128
        self._threshold_size= 20
        self._backgroundframe= False 

    def set_threshold_graylevel(self, arg_threshold):
        self._threshold_graylevel= arg_threshold

    def set_threshold_size(self, arg_threshold):
        self._threshold_size= arg_threshold

    def store_all_para(self):
        data= dict()
        data["plastic_thrshd_gray"] = self._threshold_graylevel
        data["plastic_thrshd_size"] = self._threshold_size
        with open(self.saveParaPath+"Para.json" , 'w') as out:
            json.dump(data , out)
            print "Para set"


    def set_background(self, arg_frame):
        #self.palstic_golden = arg_frame
        # make sure output dir exists
        #if(not path.isdir(self._saveParaPath)):
        #    makedirs(self._saveParaPath)

        #tmp= cv2.cvtColor(arg_frame, cv2.COLOR_RGB2BGR)
        self._backgroundframe= arg_frame 
        #cv2.imwrite(self._saveParaPath+self._backgroundName,arg_frame)

    def check_background(self):
        if path.isfile(self._saveParaPath+self._backgroundName):
            return True
        else:
            return False

    #def start_detect(self, arg_frame):
        #result = self.get_contour(arg_frame, True, )

    def get_contour(self, arg_frame, arg_export_index, arg_export_path='Debug/', arg_export_filename= 'debug0'):

        #golden= cv2.imread(self._saveParaPath+self._backgroundName)
        
        subtractedImg = cv2.subtract(arg_frame, self._backgroundframe)
        #subtractedImg = cv2.subtract(self._backgroundframe, arg_frame)
        '''
        tmp = cv2.normalize(subtractedImg, alpha=0, beta=255, norm_type=cv2.cv.CV_MINMAX, dtype=cv2.cv.CV_8UC3)
        cv2.imwrite("Debug/Subtracted.png" ,tmp)
        #print "Subtracted saved"
        '''
        subtractedImg = cv2.cvtColor(subtractedImg, cv2.COLOR_RGB2GRAY)
        #print "threshold=", self._threshold_graylevel

        #ret , thresholdedImg = cv2.threshold(subtractedImg, self._threhold_graylevel, 255, cv2.THRESH_BINARY)
        #thresholdedImg= imgProcess_tool.binarialization(subtractedImg, 0, 50) 
        thresholdedImg= imgProcess_tool.binarialization(subtractedImg, 1) 
        #thresholdedImg= imgProcess_tool.binarialization(subtractedImg, 2) 
        #cv2.imwrite("./debug/Thresholded.jpg" , thresholdedImg)
        #print "thresholdedImg saved"

        result = cv2.cvtColor(thresholdedImg, cv2.COLOR_GRAY2RGB)
        ctrs, hier = cv2.findContours(thresholdedImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #print "ctrs #:" , len(ctrs)

        ctrs = filter(lambda x : cv2.contourArea(x) > self._threshold_size , ctrs)
        #print "ctrs sized #:" , len(ctrs)
        #self.found_ctr.config(text = str(len(ctrs)))

        #rects = [[cv2.boundingRect(ctr) , ctr] for ctr in ctrs]
        #print rects
        #for rect , cntr in rects:
        for ctr in ctrs:
        #result = im_rgb.copy()
            #print im_rgb
            rect = cv2.minAreaRect(ctr)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(result, [box], 0, (128, 255, 0), 3)
            #print im_rgb
        if arg_export_index:
            cv2.imwrite(arg_export_path+ arg_export_filename+'.jpg', result)
        #cv2.imshow("Results" , result) ; cv2.waitKey(0) ; cv2.destroyAllWindows()
        #print "Plastic compare success"
	return result

if __name__== '__main__':
    date= time.strftime('%m-%d')
    debugFolder= 'Debug/'+date+'/' 
    outputFolder= 'Data/'+date+'/'
    utils_tool.check_path(debugFolder) 
    utils_tool.check_path(outputFolder)

    cam_id= int(sys.argv[1])
    cap = cv2.VideoCapture(cam_id)
    thrValue_size= int(sys.argv[2])

    detector= jump_detect(debugFolder, 'Paras/')
    backgroundframe= cv2.imread(outputFolder+'background_0.jpg')
    detector.set_background(backgroundframe)
    detector.set_threshold_size(thrValue_size)
    index=0 
    while cap.isOpened():
        t1= time.time()
	ret , frame = cap.read()
        print '---------\nCapture time: ',time.time()- t1 

	#gray_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
        #print '*** gray_frame.shape: ', gray_frame.shape
        #'''
        print 'image shape: ', frame.shape
        display= detector.get_contour(frame.copy(), False)
        print 'Process time: ',time.time()- t1 
        cv2.imshow("Live" , display )
	'''
        cv2.imshow("Live" , frame)
	#'''
        key = cv2.waitKey(1) & 0xFF 

        if key == ord('q'):
            break
        elif key == ord('s'):
            index= index+1
            cv2.imwrite(outputFolder+"frame_{0}.jpg".format(index) , display)
        elif key == ord('a'):
            cv2.imwrite(outputFolder+'background_0.jpg', frame.copy())
            pass 
