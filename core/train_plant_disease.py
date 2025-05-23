# -*- coding: utf-8 -*-
"""Train_plant_disease.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1njOpHa31i_vnKZzlGgcGFKXX5gh47dxe

## Importing Libraries
"""

# from google.colab import drive
# drive.mount('/content/drive')

import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

"""#### Dataset Link: https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset

## Data Preprocessing

### Training Image Preprocessing
"""

training_set = tf.keras.utils.image_dataset_from_directory(
    '/content/drive/MyDrive/Colab Notebooks/Chat Bot/aicrop/Rice-diseases-Data-Set/Dataset',
    labels="inferred",
    label_mode="categorical",
    class_names=None,
    color_mode="rgb",
    batch_size=32,
    image_size=(128, 128),
    shuffle=True,
    seed=None,
    validation_split=None,
    subset=None,
    interpolation="bilinear",
    follow_links=False,
    crop_to_aspect_ratio=False,
)

"""### Validation Image Preprocessing"""

validation_set = tf.keras.utils.image_dataset_from_directory(
    '/content/drive/MyDrive/Colab Notebooks/Chat Bot/aicrop/Rice-diseases-Data-Set/Dataset',
    labels="inferred",
    label_mode="categorical",
    class_names=None,
    color_mode="rgb",
    batch_size=32,
    image_size=(128, 128),
    shuffle=True,
    seed=None,
    validation_split=None,
    subset=None,
    interpolation="bilinear",
    follow_links=False,
    crop_to_aspect_ratio=False,
)

training_set

for x,y in training_set:
    print(x,x.shape)
    print(y,y.shape)
    break

"""### To avoid Overshooting
1. Choose small learning rate default 0.001 we are taking 0.0001
2. There may be chance of Underfitting, so increase number of neuron
3. Add more Convolution layer to extract more feature from images there may be possibilty that model unable to capture relevant feature or model is confusing due to lack of feature so feed with more feature

## Building Model
"""

from tensorflow.keras.layers import Dense,Conv2D,MaxPool2D,Flatten,Dropout
from tensorflow.keras.models import Sequential

model = Sequential([
    tf.keras.layers.Input(shape=(128, 128, 3)), #define the input shape here.
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    # ... rest of your layers
])

## Building Convolution Layer

model.add(Conv2D(filters=32,kernel_size=3,padding='same',activation='relu',input_shape=[128,128,3]))
model.add(Conv2D(filters=32,kernel_size=3,activation='relu'))
model.add(MaxPool2D(pool_size=2,strides=2))

model.add(Conv2D(filters=64,kernel_size=3,padding='same',activation='relu'))
model.add(Conv2D(filters=64,kernel_size=3,activation='relu'))
model.add(MaxPool2D(pool_size=2,strides=2))

model.add(Conv2D(filters=128,kernel_size=3,padding='same',activation='relu'))
model.add(Conv2D(filters=128,kernel_size=3,activation='relu'))
model.add(MaxPool2D(pool_size=2,strides=2))

model.add(Conv2D(filters=256,kernel_size=3,padding='same',activation='relu'))
model.add(Conv2D(filters=256,kernel_size=3,activation='relu'))
#model.add(MaxPool2D(pool_size=2,strides=2))

model.add(Dropout(0.25)) # To avoid Overfitting

model.add(Flatten())

model.add(Dense(units=1500,activation='relu'))

model.add(Dropout(0.4))

#Output Layer
model.add(Dense(units=3,activation='softmax'))

"""### Compiling Model"""

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

"""### Model Training"""

training_history = model.fit(x=training_set, validation_data=validation_set, epochs=10)

"""## Model Evaluation"""

#Model Evaluation on Training set
train_loss,train_acc = model.evaluate(training_set)

print(train_loss,train_acc)

#Model on Validation set
val_loss,val_acc = model.evaluate(validation_set)

print(val_loss,val_acc)



"""### Saving Model"""

model.save("/content/drive/MyDrive/Colab Notebooks/Chat Bot/aicrop/trained_model.keras")

training_history.history

#Recording History in json
import json
with open("training_hist.json","w") as f:
    json.dump(training_history.history,f)



training_history.history['val_accuracy']

"""### Accuracy Visualization"""

epochs = [i for i in range(1,11)]
plt.plot(epochs,training_history.history['accuracy'],color='red',label='Training Accuracy')
plt.plot(epochs,training_history.history['val_accuracy'],color='blue',label='Validation Accuracy')
plt.xlabel("No. of Epochs")
plt.ylabel("Accuracy Result")
plt.title("Visualization of Accuracy Result")
plt.legend()
plt.show()



"""### Some other metrics for model evaluation"""

class_name = validation_set.class_names
class_name



test_set = tf.keras.utils.image_dataset_from_directory(
    '/content/drive/MyDrive/Colab Notebooks/Chat Bot/aicrop/Rice-diseases-Data-Set/Dataset',
    labels="inferred",
    label_mode="categorical",
    class_names=None,
    color_mode="rgb",
    batch_size=32,
    image_size=(128, 128),
    shuffle=False,
    seed=None,
    validation_split=None,
    subset=None,
    interpolation="bilinear",
    follow_links=False,
    crop_to_aspect_ratio=False,
)

y_pred = model.predict(test_set)
y_pred,y_pred.shape

predicted_categories = tf.argmax(y_pred,axis=1)

predicted_categories

true_categories = tf.concat([y for x,y in test_set],axis=0)
true_categories

Y_true = tf.argmax(true_categories,axis=1)
Y_true



"""![image.png](attachment:f464cbcc-5d6b-4f32-835c-9aabe0f9c5d4.png)"""



from sklearn.metrics import classification_report,confusion_matrix

print(classification_report(Y_true,predicted_categories,target_names=class_name))

cm = confusion_matrix(Y_true,predicted_categories)
cm



"""### Confusion Matrix Visualization"""

plt.figure(figsize=(40,40))
sns.heatmap(cm,annot=True,annot_kws={'size':10})
plt.xlabel("Predicted Class",fontsize=20)
plt.ylabel("Actual Class",fontsize=20)
plt.title("Plant Disease Prediction Confusion Matrix",fontsize=25)
plt.show()







