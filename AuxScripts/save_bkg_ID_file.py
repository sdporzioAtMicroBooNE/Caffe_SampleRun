import sys
import numpy as np
import pandas as pd
import caffe
from ROOT import larcv
from time import sleep, time
from math import floor

#if len(sys.argv) < 2:
  #print "Error! You must provide the run number as an argument. Exiting..."
  #exit(1)

#iteration = int(sys.argv[1])

t0 = time()
print 'Step1';
#net = caffe.Net("sig_prototxt/jhewes_vgg16b_sig_{}.prototxt".format(iteration),
               # "vgg16b_iter_100.caffemodel.h5",
              #  caffe.TEST)
net = caffe.Net("/hepgpu1-data3/akeats/CaffeRun_HSN/Settings/test_bkg.prototxt",
               "/hepgpu1-data3/akeats/CaffeRun_HSN/vgg16b_iter_7000.caffemodel.h5",
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
f = open('bkgtest_eventlist_7000its_ID.txt','w')
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
event_ID = []
batch_counter = 0
#evts_per_batch = 20
evts_per_batch = 1
max_batch = floor(n_evts/evts_per_batch)

DIV = 100

while batch_counter < max_batch:

  t = time()
  print "Processing batch {} of {}. Timestamp is {}".format(batch_counter+1,max_batch,t-t0)
  net.forward()
  while filler.thread_running():
    sleep(0.001)
  for i,a in enumerate(net.blobs["softmax"].data):
    c_run = int(filler.processed_events()[i].run())
    c_subrun = int(filler.processed_events()[i].subrun())
    c_event = int(filler.processed_events()[i].event())
  #for a in net.blobs["fc6"].data:
    scores.append(float(a[0]))
    event_ID.append(c_event)
    print c_event, a[0]
  batch_counter += 1


if len(scores) == len(event_ID):
  dataset = dict()
  dataset["scores"] = scores
  dataset["event_ID"] = event_ID

  if batch_counter % DIV ==0:
    res = pd.DataFrame(dataset)
#res.to_pickle("data/sig_scores_{}.pkl".format(iteration))
    res.to_pickle("bkgtest_scores_7000its_ID.pkl")

  f2 = open('bkgtest_eventlist_7000its_IDrange.txt','w')
  for i in range (len(dataset["event_ID"])):
    if dataset["scores"][i]>0.9:
      s = dataset["scores"][i]
      e = dataset["event_ID"][i]
      f2.write("{} {}\n".format(s,e))
    if dataset["scores"][i]<0.1:
      s = dataset["scores"][i]
      e = dataset["event_ID"][i]
      f2.write("{} {}\n".format(s,e))
    if dataset["scores"][i]>0.45 and dataset["scores"][i]<0.55:
      s = dataset["scores"][i] 
      e = dataset["event_ID"][i]
      f2.write("{} {}\n".format(s,e))
  f2.close()


t = time()
print "Checkpoint 3: Done writing scores to file. Timestamp is {}".format(t-t0)

