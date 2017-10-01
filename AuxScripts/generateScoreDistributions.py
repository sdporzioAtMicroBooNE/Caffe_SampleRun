import sys
import numpy as np
import pandas as pd
import caffe
from ROOT import larcv
from time import sleep, time
from math import floor

if len(sys.argv) < 2:
  print "Error! Need to provide prototxt and h5 files!"
  exit()

prototxtFile = sys.argv[1]
h5File = sys.argv[2]

#iteration = int(sys.argv[1])

t0 = time()
print 'Step1';
#net = caffe.Net("sig_prototxt/jhewes_vgg16b_sig_{}.prototxt".format(iteration),
               # "vgg16b_iter_100.caffemodel.h5",
              #  caffe.TEST)
net = caffe.Net(prototxtFile,
               h5File,
                caffe.TEST)
print 'Step2';
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

t = time()
print "Checkpoint 1: Done initialising network. Timestamp is {}".format(t-t0)

#f = open('evt_lists/sig_eventlist_{}.txt'.format(iteration),'w')
addName = h5File.split('.')[0]
f = open('ScoreFiles/eventtlist_%s.txt' %(addName),'w')
print 'step3';
for i in xrange(n_evts):
  myio.read_entry(i)
  d = myio.get_data(0)
  run    = d.run()
  subrun = d.subrun()
  event  = d.event()
  f.write("{} {} {}\n".format(run,subrun,event))
f.close()

t = time()
print "Checkpoint 2: Done writing event numbers to file. Timestamp is {}".format(t-t0)

scores = []
batch_counter = 0
evts_per_batch = 20
max_batch = floor(n_evts/evts_per_batch)

DIV = 100

while batch_counter < int(max_batch):

  t = time()
  print "Processing batch {} of {}. Timestamp is {}".format(batch_counter+1,max_batch,t-t0)
  net.forward()
  while filler.thread_running():
    sleep(0.001)
  #print net.blobs;
  for a in net.blobs["softmax"].data:
  #for a in net.blobs["fc6"].data:
    scores.append(float(a[0]))
  batch_counter += 1

  if batch_counter % DIV ==0:
    res = pd.Series(scores)
#res.to_pickle("data/sig_scores_{}.pkl".format(iteration))
    res.to_pickle("ScoreFiles/scores_%s.pkl" %addName)

t = time()
print "Checkpoint 3: Done writing scores to file. Timestamp is {}".format(t-t0)

