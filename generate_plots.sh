#!/bin/bash

for name in bfgs cg genetic momentum rprop tnc
do ./train.py network11042012_$name.net test 10 >> /dev/null
    echo "Plots for network11032012_$name.net generated!"
done


