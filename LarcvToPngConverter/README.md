# Image converter
Converts LArCV root file into png images that can be viewed.

It needs a root file containing the LArCV data, a list file containing a score (assigned by the CNN) and an event ID (separated by a space) and the boundaries on the score that must be placed (e.g. 0.8 and 0.9 will create images for events with a CNN score between 0.8 and 0.9).

Sample use:

```
python converter.py [input Root file] [input event list] [left boundary] [right boundary]
```

e.g.:
```
python converter.py larcv_Signal_Constrain_4.root sampleList.txt 0.6 0.9
```