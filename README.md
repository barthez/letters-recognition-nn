# BEFEOR RUNNING

Install libraries:

* numpy
* scipy
* matplotlib
* networkx
* ffnet

Works only with Python 2.6 - 2.7

# Create a network

```
./train.py letters_new train letters.pat
```

# Run tests (get plots)

To get plots based on the http://ffnet.sourceforge.net/apidoc.html#ffnet.ffnet.test method, run the app like this:

```
./train.py letters_new_1.net test 10
```

where 10 is the amount of points you want to have "noise".
Noise is added randomly selected by flipping a field 0 <-> 1, a noise level of 10 means that
this operation of chosing a field and performing the flip will be performed 10 times.
