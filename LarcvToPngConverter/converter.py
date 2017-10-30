import sys
import pickle
import caffe
import os
from ROOT import larcv
from array import array
from os.path import exists
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family']='serif'
plt.rcParams['font.weight']='light'
plt.rcParams['font.size']=14
figsize = (40,21)

def Warning(string):
    START_W = '\033[1;33m'
    END_W = '\033[0m'
    print START_W + string + END_W

def PrintFlush(string):
    sys.stdout.write('\r'+'\033[K'+string)
    sys.stdout.flush()

def FromSsv(filename,dtype='str'):
    with open(filename,'rb') as fileIn:
        data = []
        lines = fileIn.read().split('\n')[:-1]
        nColumns = len(lines[0].split(' '))
        if nColumns>1:
            for i in range(nColumns):
                if dtype=='int': data.append([int(line.split(' ')[i]) for line in lines])
                if dtype=='float': data.append([float(line.split(' ')[i]) for line in lines])
                if dtype=='str': data.append([str(line.split(' ')[i]) for line in lines])
        else:
            for line in lines:
                if dtype=='int': data.append(int(line))
                if dtype=='float': data.append(float(line))
                if dtype=='str': data.append(str(line))
    return data

def GenerateEnvironment():
	if not os.path.exists('Plots'):
		print 'Creating directory %s/Plots' %(os.getcwd())
		os.makedirs('Plots')
	if not os.path.exists('Plots/PlaneY'):
		print 'Creating directory %s/Plots/PlaneY' %(os.getcwd())
		os.makedirs('Plots/PlaneY')

def SaveEventDisplays(nEvent,nRows,nCols,imageVector):
	img0 = []
	img1 = []
	img2 = []

	for i in range(nRows):
		img0.append([])
		img1.append([])
		img2.append([])
		for j in range(nCols):
			img0[i].append(imageVector[0][i*nCols + j])
			img1[i].append(imageVector[1][i*nCols + j])
			img2[i].append(imageVector[2][i*nCols + j])
	        
	f, (ax1, ax2, ax3) = plt.subplots(3,1, sharex=True, figsize=figsize)
	ax1.imshow(img0, cmap='YlGnBu_r')
	ax1.set_title('U Plane')
	ax2.imshow(img1, cmap='YlGnBu_r')
	ax2.set_title('V Plane')
	ax3.imshow(img2, cmap='YlGnBu_r')
	ax3.set_title('Y Plane')
	f.suptitle('Event %i' %(nEvent))
	nameFig = 'Plots/event_%i.png' %(nEvent)
	f.savefig(nameFig)
	Warning('Saved figure %s.' %(nameFig))
	plt.close('all')
	f2 = plt.figure(figsize=(15,15))
	plt.imshow(img2, cmap='YlGnBu_r')
	plt.title('Event %i | Y Plane Only' %(nEvent))
	nameFig = 'Plots/PlaneY/yonly_event_%i.png' %(nEvent)
	plt.savefig(nameFig)
	Warning('Saved figure %s.' %(nameFig))
	plt.close('all')

def SelectListEvents(eventList,boundLeft,boundRight):
	shortList = []
	for score,event in zip(eventList[0],eventList[1]):
		if float(score) > boundLeft and float(score) < boundRight:
			shortList.append(int(event))
	return shortList

def GenerateImages(inputRootFile,inputEventList,boundLeft,boundRight):
	outName = 'empty.root'
	eventList = FromSsv(inputEventList,dtype='str')
	shortList = SelectListEvents(eventList,boundLeft,boundRight)
	nListEvents = len(shortList)
	Warning("%i events selected from %i (in selection [%.2f,%.2f])" %(nListEvents,len(eventList[0]),boundLeft,boundRight))
	evProcessed = 0

	# Initialization
	iom = larcv.IOManager(2)
	iom.add_in_file(inputRootFile)
	iom.set_out_file(outName)
	iom.initialize()

	# Execution
	for k in xrange(iom.get_n_entries()):
		if (k%100==0): PrintFlush('%i of %i entries analyzed.' %(k,iom.get_n_entries()))
		iom.read_entry(k)
		imData = iom.get_data(larcv.kProductImage2D,'tpc')
		eventNumber = int(iom.event_id().event())
		if eventNumber in shortList:
			evProcessed += 1
			print "\nFound event %i from list... [%i more to find]" %(eventNumber,nListEvents-evProcessed)
			imageVector = []
			ev = int(iom.event_id().event())
			nRows = int(imData.Image2DArray().at(0).meta().rows())
			nCols = int(imData.Image2DArray().at(0).meta().cols())
			imageVector.append(imData.Image2DArray().at(0).as_vector())
			imageVector.append(imData.Image2DArray().at(1).as_vector())
			imageVector.append(imData.Image2DArray().at(2).as_vector())
			SaveEventDisplays(ev,nRows,nCols,imageVector)
		iom.clear_entry()

	# Finalization
	iom.finalize()
	iom.reset()
	os.remove(outName)

# Main execution
if len(sys.argv)!=3:
	raise Exception("Must provide 4 arguments! [input Root file, input event list, left boundary, right boundary]\ne.g.: python converter.py larcv_Signal_Constrain_4.root sampleList.txt 0.6 0.9")
inputRootFile =  sys.argv[1]
inputEventList = sys.argv[2]
boundLeft = float(sys.argv[3])
boundRight = float(sys.argv[4])
# inputRootFile = '/data/LArCNN/Samples_LArCV/HeavySterileNeutrinos_DecayMuPi_Mass0.3_EventSize50k/Testing/larcv_Signal_Constrain_4.root'
# inputEventList = 'abby.txt'
# boundLeft = 0.0
# boundRight = 0.062
GenerateEnvironment()
GenerateImages(inputRootFile,inputEventList, boundLeft, boundRight)
