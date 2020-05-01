# Multi-Planet: using multiproccesing with Vplanet

This program, dubbed 'Multi-Planet' works in conjuction with the Vpsace and Vplanet code found [here on Github](https://github.com/VirtualPlanetaryLaboratory/vplanet). 

In the vplanet-multiprocess directory, there is a file called `vspace_list`. This file is where you put the ***full path*** to where your vspace files are located, so multi-planet knows where they are. It does not matter if the vspace file is for parameter sweeps or Monte Carlo satistical runs, multi-planet works reguardless.

multi-planet takes 2 arguments: The directory where you would like the vplanet files to be generated, and the number of cores (I reccomend using a small amount unless you have avery fast PC that can handle lots of computation power). After listing the vspace files in the `vspace_list` file, write the following command in the command line: 

```
python vplanet-multiprocess.py [Project Directory] [number of cores]
```
