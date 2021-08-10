# -*- coding: utf-8 -*-
"""Submission-MachineLearningPemula-KlasifikasiGambar.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/130-Tl0nJurkdin9Oe_HmbjLGB2enStCN

# Dicoding Submission Belajar Mahcine Learning Untuk Pemula
## Nama : Winarto
"""

# Commented out IPython magic to ensure Python compatibility.
# import Dependencies
import zipfile, os
from google.colab import files

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image

# %matplotlib inline

# prepare data  
!wget --no-check-certificate \
  https://dicodingacademy.blob.core.windows.net/picodiploma/ml_pemula_academy/rockpaperscissors.zip \
  -O /tmp/rockpaperscissors.zip

# extract file
local_zip = '/tmp/rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/tmp')
zip_ref.close()

# Agumentasi gambar menggunakan ImageDataGenerator dengan ukuran validation set 0.4 atau 40% dari keseluruhan data
train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=20,
                                   horizontal_flip=True,
                                   shear_range=0.2,
                                   fill_mode='wrap',
                                   validation_split=0.4
                                   )

# Menghasilkan kumpulan data dari hasil augmentasi gambar menggunakan method flow_from_directory

train_generator = train_datagen.flow_from_directory(
    '/tmp/rockpaperscissors/rps-cv-images', # menentukan target path
    target_size=(150, 150), 
    batch_size=32,
    shuffle=True, 
    class_mode='categorical', # karena data klasifikasinya lebih dari 2 maka menggunakan class_mode = 'categorical'
    # memberikan parameter subset karena pada saat augmentasi gambar kita juga sudah mengaktifkan validation_split
    subset='training', 
)

validation_generator = train_datagen.flow_from_directory(
    '/tmp/rockpaperscissors/rps-cv-images',
    target_size=(150, 150),
    batch_size=32,
    shuffle=True, 
    class_mode='categorical',
    subset='validation' 
)

# Membuat model menggunakan mode Sequential
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

# Panggil fungsi compile 
model.compile(loss='categorical_crossentropy', # 'categiorical_crossentropy' dipilih karena klasifikasinya lebih dari 2
              optimizer=tf.optimizers.Adam(), 
              metrics=['accuracy'])

# Latih Model
model.fit(train_generator,
          steps_per_epoch=25,
          epochs=20,
          validation_data = validation_generator,
          validation_steps=5,
          verbose=2)

# Evaluasi Model Loss dan Accuracy
model_score = model.evaluate(validation_generator, steps=20)
print('Loss : ', model_score[0])
print('Accuracy : ', model_score[1])

# Fungsi PredictImage
def predictImage(upload_image):
  for fn in upload_image.keys():

    path = fn
    img = image.load_img(path, target_size=(150,150))
    imgplot = plt.imshow(img)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
  
    images = np.vstack([x])
    classes = model.predict(images, batch_size=10)
    
    print(fn)
    print(classes)
    if classes[0][0] == 1:
      print('Kertas')
    elif classes[0][1] == 1:
      print('Batu')
    elif classes[0][2] == 1:
      print('Gunting')
    else:
      print('Tidak Tahu')

# Panggil method Upload
uploaded = files.upload()

# Panggil Method PredictImage
predictImage(uploaded)