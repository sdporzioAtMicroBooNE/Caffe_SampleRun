# Caffe_SampleRun
A sample environment to start playing with Caffe on the *hepgpu1* servers at Manchester

---

**VERY IMPORTANT**: This repository will work only on the *hepgpu1* servers since it contains explicit path references. Don't try using it anywhere else (it won't work).

*Also, before getting started*, if you have no idea what Caffe does, or some of the details are lost to you, take a look at this great intuitive short introductions to Multi-Layer Perceptrons and CNN:

[Multi-Layer Perceptrons Tutorial](https://ujjwalkarn.me/2016/08/09/quick-intro-neural-networks/)

[Convolutional Neural Network Tutorial](https://ujjwalkarn.me/2016/08/11/intuitive-explanation-convnets/)

And if you want to know how all that applies to Caffe, please take a look at these short [Caffe Tutorial Slides](https://docs.google.com/presentation/d/1HxGdeq8MPktHaPb-rlmYYQ723iWzq9ur6Gjo71YiG0Y/edit#slide=id.g109e849287_6_515) and at their [Tour](http://caffe.berkeleyvision.org/tutorial/) section.

---

**How to use it:**

Start using it Caffe is a simple as running the following two commands:

```shell
source sourceMe.sh
```

to setup the Caffe environment. You'll get some warning due to LArLite/LArCV trying to re-build the code (and you having no permissions to do it), but just ignore them.

Then to start Caffe, just run:

```shell
./runCaffe.sh
```

And then just wait for the CNN to work its magic.

You might want to do that in a *screen* session, since you probably want Caffe to be running for a *long* time.

Once Caffe has been running for a while, you can start making plots! Just run the following command:

```shell
./generatePlots.sh
```

to convert all the log files in your *LogFiles* directory in accuracy/loss plots (under your *Plots* directory).

Discrimination plots coming soon...

---

**Samples:** 

You can find some signal (*Heavy Sterile Neutrinos*) samples at this path:

```shell
/data/LArCNN/Samples_LArCV/HeavySterileNeutrinos_DecayMuPi_Mass0.3_EventSize50k
```

And some background (*BNB* $\nu_{\mu}$) samples at this path:

```shell
/data/LArCNN/Samples_LArCV/BNB_NuMu_EventSize50k
```

---

**Contacts:**

If you have any query, contact _salvatore.porzio@postgrad.manchester.ac.uk_.