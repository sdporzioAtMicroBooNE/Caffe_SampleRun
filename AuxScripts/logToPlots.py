import sys
import matplotlib
import os
import subprocess
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from time import sleep

def make_plots(logfile,it,it_av,acc,acc_av,loss):
  fileName = logfile.split('/')[1].split('.')[0]
  plt.plot(it,acc,label="Accuracy")
  plt.plot(it_av,acc_av,color="r",label="Accuracy (5000its mean)")
  plt.title("Neural net training accuracy")
  plt.xlabel("Iterations")
  plt.ylabel("Accuracy")
  plt.legend()
  plt.savefig('Plots/accuracy_%s.png' %(fileName))
  plt.clf()
  plt.plot(it,loss)
  plt.title("Neural net training loss")
  plt.xlabel("Iterations")
  plt.ylabel("Loss")
  axes = plt.gca()
  axes.set_ylim([0,10])
  plt.savefig('Plots/loss_%s.png' %(fileName))
  plt.clf()

if len(sys.argv) < 2:
  print "Error! Need to provide log file as argument."
  exit()

logfile = sys.argv[1]
if len(sys.argv)>2:
  maxIter = int(sys.argv[2])
else: maxIter = -1


def makedata(logfile,maxIter):
  iteration = 0
  f = open(logfile)
  line = f.readline()

  it = []
  acc = []
  it_av = []
  acc_av = []
  loss = []

  acc_mean = 0
  n_its = 50

  nLine = 0
  while line:
    # Go on until Iteration is in line, exit if end of file
    while "Iteration {0:}".format(iteration) not in line:
      line = f.readline()
      nLine += 1
      if not line:
        return it,it_av,acc,acc_av,loss

    # Determine loss
    it.append(iteration)
    if len(line.split(' '))>8:
      loss.append(float(line.split(' ')[8].strip()))
    else:
      print "Something happened to the file..."

    # Move to next line, exit if end of file
    line = f.readline()
    nLine += 1
    if not line:
      return it,it_av,acc,acc_av,loss

    # Determine accuracy
    if len(line.split(' '))>14:
      this_acc = float(line.split(' ')[14].strip())
      acc.append(this_acc)
      acc_mean += this_acc
      if iteration+1 % n_its == 0:
        acc_mean /= n_its
        it_av.append(iteration)
        acc_av.append(float(acc_mean))
        acc_mean = 0
    else: 
      print "Something happened to the file..."

    # Move to next line, exit if end of file
    line = f.readline()
    nLine += 1
    if not line:
      print "Stopping at line %i" %(nLine)
      return it,it_av,acc,acc_av,loss

    print 'Processing iteration %i' %(iteration)
    iteration += 1
    if iteration==maxIter:
      return it,it_av,acc,acc_av,loss

it,it_av,acc,acc_av,loss = makedata(logfile,maxIter)
make_plots(logfile,it,it_av,acc,acc_av,loss)




