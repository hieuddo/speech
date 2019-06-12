# HMM ASR for Pickup Objects in AI2Thor

Youtube Demo: [Click here](https://www.youtube.com/watch?v=lZ1yOTgKsh8) and [here](https://www.youtube.com/watch?v=wIjFdRnOMnE)

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
  * run ```python app.py``` to run the program with interface, ```python main.py``` to go directly into AI2Thor enviroment

## Training phases
### Phase 1
  * HMM with 10 normal records data
  * Model performs poor accuracy

### Phase 2
  * HMM with 20 normal records data including noise-contained records
  * Model performs poor accuracy

### Phase 3
  * HMM with 30 normal records data
  * Input record for detect is noise-reduced
  * Accuracy improves

### Phase 4
  * Use noise-reduction for all training data
  * HMM with 30 noise-removed records
  * Input record is split by slience and detected part by part
    * Model only detect if there is input sound, otherwise the device keep recording
    * Once record can include multiple words, record is split into parts by the silence between words
    * Detect part by part to predict multiple words
  * Accuracy is nearly 100%