import sys
import numpy as np
import pandas as pd
import caffe
from ROOT import larcv
from time import sleep, time
from math import floor

# Load file paths from arguments and save current timestamp
if len(sys.argv) < 2:
  print "Error! Need to provide prototxt and h5 files!"
  exit()
prototxtFile = sys.argv[1]
h5File = sys.argv[2]
t0 = time()

# Load the network
print 'Step1. Loading the caffe network'
#net = caffe.Net("sig_prototxt/jhewes_vgg16b_sig_{}.prototxt".format(iteration),"vgg16b_iter_100.caffemodel.h5",caffe.TEST)
net = caffe.Net(prototxtFile,h5File,caffe.TEST)
t = time()
print "Checkpoint 1: Done initialising network. Step time: %.1f" %(t-t0); t0 = t

# Load LArCV sample events
print 'Step2. Loading events.'
caffe.set_mode_gpu()
caffe.set_device(0)

if not larcv.ThreadFillerFactory.exist_filler("DataFiller"):
  print '\033[93mFiller',self._filler_name,'does not exist...\033[00m'
  exit(1)

filler = larcv.ThreadFillerFactory.get_filler("DataFiller")
n_evts = filler.get_n_entries()
filler.set_random_access(False)

myio = larcv.IOManager(0)
for f in filler.pd().io().file_list():
  myio.add_in_file(f)
myio.initialize()

n_evts = 5
for i in xrange(n_evts):
  myio.read_entry(i)
  d = myio.get_data(0)

t = time()
print "Checkpoint 2: Done loading events. Step time: %.1f" %(t-t0); t0 = t


# Extract data
print 'Step3. Loading data from each event.'
# Opening output files
addName = h5File.split('/')[-1].split('.')[0]
scores = []
run = []
subrun = []
event = []
batch_counter = 0
evts_per_batch = 1
max_batch = floor(n_evts/evts_per_batch)

while batch_counter < max_batch:
  t = time()
  print "Processing batch {} of {}. Timestamp is {}".format(int(batch_counter+1),int(max_batch),t-t0)
  net.forward()
  while filler.thread_running():
    sleep(0.001)
  for i,a in enumerate(net.blobs["softmax"].data):
    c_run = int(filler.processed_events()[i].run())
    c_subrun = int(filler.processed_events()[i].subrun())
    c_event = int(filler.processed_events()[i].event())
    print i, a
    scores.append(float(a[0]))
    run.append(c_run)
    subrun.append(c_subrun)
    event.append(c_event)
  batch_counter += 1

f2 = open('ScoreFiles/scorelist_%s.txt' %addName,'w')
for i in range (len(event)):
    f2.write("{} {} {} {}\n".format(run,subrun,event,scores))
f2.close()

t = time()
print "Checkpoint 2: Done loading events. Step time: %.1f" %(t-t0); t0 = t

