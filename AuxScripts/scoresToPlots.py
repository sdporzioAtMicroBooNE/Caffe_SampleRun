import matplotlib
matplotlib.use('Agg')
import pickle
import numpy as np

from matplotlib import pyplot as plt

pickleFile = []
labelPlot = []
c = []

def discriminator(pickleFile,labelPlot,norm,c):
    f = pickleFile
    pkl = np.load(f)
    data = np.array(pkl.values)
    integral = np.sum(data)

#print data
#print type(data), type(data[0])
    hist,bin_edges = np.histogram(data,bins=100,range=(0,1))
#print bin_edges
    cut_bin_edges = bin_edges[:-1]
#print len(cut_bin_edges), len(hist);
    plt.step(cut_bin_edges,(hist/float(integral))*norm,label=labelPlot,color=c)
    plt.gca().set_ylim(bottom=0)
    plt.xlim(0,1)
    plt.ylim(0,1)


pickleFile.append('/hepgpu1-data3/akeats/Run_j_parameters/sigtrain_scores_2000its.pkl')
pickleFile.append('/hepgpu1-data3/akeats/Run_j_parameters/sigtrain_scores_4000its.pkl')
pickleFile.append('/hepgpu1-data3/akeats/Run_j_parameters/sigtrain_scores_6000its.pkl')
pickleFile.append('/hepgpu1-data3/akeats/Run_j_parameters/bkgtrain_scores_2000its.pk\
l')
pickleFile.append('/hepgpu1-data3/akeats/Run_j_parameters/bkgtrain_scores_4000its.pk\
l')
pickleFile.append('/hepgpu1-data3/akeats/Run_j_parameters/bkgtrain_scores_6000its.pk\
l')


labelPlot.append('signal 2000 iterations')
labelPlot.append('signal 4000 iterations')
labelPlot.append('signal 6000 iterations')
labelPlot.append('background 2000 iterations')
labelPlot.append('background 4000 iterations')
labelPlot.append('background 6000 iterations')
c.append('red')
c.append('blue')
c.append('green')
c.append('red')
c.append('blue')
c.append('green')


for i in range(6):
    discriminator(pickleFile[i],labelPlot[i],1,c[i])


plt.title("Discriminator Plot")
plt.xlabel("Discriminator")
plt.ylabel("Number of events")
plt.legend()
plt.savefig('/hepgpu1-data3/akeats/CaffeRun_HSN/Plots/discriminator_train_bkg_2000_4000_6000its.png')
plt.show()
plt.clf()


