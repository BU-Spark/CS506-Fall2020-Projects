import csv
import shutil
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model

print(tf.__version__)
print(os.getcwd())


model = load_model('my_model.h5')#load the trained model

test_datagen = ImageDataGenerator(rescale=1. / 255)

#create an empty 'predict' folder in the same directory and then put your folder of images into it
eval_generator = test_datagen.flow_from_directory("predict",target_size=(224, 224),
                                                  batch_size=1,shuffle=False,seed=42,class_mode=None)

pred = model.predict(eval_generator,verbose=1)

os.mkdir("P")
os.mkdir("NP")

for index, probability in enumerate(pred):

    if (probability[0]>=0.5):

        shutil.move("predict/"+eval_generator.filenames[index], "P")
    else:

        shutil.move("predict/"+eval_generator.filenames[index], "NP")
        


