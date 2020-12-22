# Parking lot classifier

## File descriptions

### ParkingLotClassifier.ipynb

contains the explainations and visualizations of the parking lot classifier

### my_model.h5

the weights for the trained CNN model

### pklotClassifier.py

script to create the model with the trained weights and classifies images into the two classes: Parking lots and none Parking lots

  execution instructions:

  Tensor flow version 2.3.1 

  1. create an empty 'predict' folder

  2. Put a folder of all the images into this 'predict' folder, so the 'predict' folder will contain a folder of images.

  3. Run the pklotClassifier.py and it will create a 'P' and a 'NP' folder, which contains corresponding images. Basically the script will move the images from the predict directory into their classified folder.
