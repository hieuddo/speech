# HMM ASR for Pickup Objects in AI2Thor

## Overview
### Requirement
  * python3
  * required libraries are in `requirements.txt`

### Data
  * Normal data is in `normal_train` folder
  * Data with noise-reduction is in `train` folder

### Pretrained model
  * All pretrained models are in `model` folder  
  * `hmm.pk` is currently the best which is trained with noise-reduction data

### How to use
  * run ```pip install -r requirements.txt``` to install required libraries
  * run ```python main.py``` to run the program