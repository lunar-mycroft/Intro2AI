#Demos:

##Fitting:

```python polyFitDemo.py -file .\DemoData\VvsT.csv -d 2 -x 30```

##kMeans clustering:

```python kmeansDemo.py -file .\DemoData\clusteringDemo.csv -distFunc e -dist 0.75 -centers 2,2 2,4 4,2```

##Neural Net Demo:

```python nnDemo.py```

##Hidden Markov Model

```python hmmDemo.py -n_s 4 -n_e 4 -file .\DemoData\hmmData.csv```

The program will prompt you to enter the most observed sequence.  This is by emission number, with 0 being the lowest.  In the above example, you could use 0,1,2,3 but not 0,1,2,4.

You can rerun the same hmm again with:

```python hmmDemo.py -file .\DemoData\hmmData.csv```