# -*- coding: utf-8 -*-
"""Model Sistem Rekomendasi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G7mJBt_YiPKhXa4ErvMq8ze8QEPu4h0s

Import kaggle untuk mengambil data
"""

!pip install -q kaggle

"""Masukkan file json yang berisi username dan key"""

from google.colab import files
files.upload()

"""Downloading private datasets via API"""

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!ls ~/.kaggle

!kaggle datasets download -d shubhammehta21/movie-lens-small-latest-dataset

"""Melakukan import library yang digunakan"""

import os
import zipfile
import numpy as np
import pandas as pd
import nltk
import keras
import tensorflow as tf
import seaborn as sns
import matplotlib.pyplot as plt

from keras import layers
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from keras.models import Model
from tensorflow.keras.optimizers import Adam
from keras.layers import Add, Activation, Lambda, BatchNormalization, Concatenate, Dropout, Input, Embedding, Dot, Reshape, Dense, Flatten

import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import Callback, ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping, ReduceLROnPlateau

"""Ekstraksi data"""

local_zip = '/content/movie-lens-small-latest-dataset.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/content')
zip_ref.close()

"""Membuat dataframe"""

movie_df = pd.read_csv('/content/movies.csv')
rating_df = pd.read_csv('/content/ratings.csv')
tags_df = pd.read_csv('/content/tags.csv')

"""Menampilkan informasi data dari file 'movies.csv'"""

movie_df

"""Menampilkan detail informasi data dari file 'movies.csv'"""

movie_df.info()

"""Memeriksa missing value pada dataset dari file 'movies.csv'"""

movie_df.isnull().sum()

"""Menghapus kolom yang tidak diperlukan pada file 'ratings.csv'"""

rating_df = rating_df.drop(['timestamp'], axis = 1)
rating_df

"""Menampilkan informasi dari file 'ratings.csv'"""

rating_df.info()

"""Memeriksa missing value pada dataset dari file 'ratings.csv'"""

rating_df.isnull().sum()

"""Menampilkan informasi data dari file 'tags.csv'"""

tags_df

"""Menampilkan detail informasi dari file 'tags.csv'"""

tags_df.info()

"""Memeriksa missing value pada dataset dari file 'tags.csv'"""

tags_df.isnull().sum()

"""Menampilkan informasi data dari file 'ratings.csv'"""

rating_df.info()

"""Menggabungkan dataframe ratings dan movies"""

new_movie_df = rating_df.merge(movie_df, how = 'inner', on = 'movieId')
new_movie_df.tail()

"""Melakukan normalisasi pada kolom rating"""

minRating = min(rating_df['rating'])
maxRating = max(rating_df['rating'])
rating_df['rating'] = rating_df["rating"].apply(lambda x : (x - minRating) / (maxRating - minRating)).values.astype(np.float32)
AvgRating = np.mean(rating_df['rating'])

"""Menampilkan rata-rata rating"""

print('Rata-rata Rating : ', AvgRating)

"""Memberikan id baru pada setiap baris pada dataframe"""

# membuat unique value dari userId
userIds = rating_df["userId"].unique().tolist()
encodedUser = {x : i for i,
               x in enumerate(userIds)}

encodedtouser = {i : x for i,
                 x in enumerate(userIds)}

# membuat kolom user dari generate nilai userId
rating_df["user"] = rating_df["userId"].map(encodedUser)
nUsers = len(encodedUser)

# membuat kolom user dari generate movieId
movieIds = rating_df["movieId"].unique().tolist()
firstMovieEncoder = {x : i for i,
                     x in enumerate(movieIds)}

movieEncoder = {i : x for i,
                x in enumerate(movieIds)}

rating_df["movie"] = rating_df["movieId"].map(firstMovieEncoder)
nMovie = len(firstMovieEncoder)

"""Menampilkan data"""

rating_df

"""Menampilkan data"""

print("Num of users : {}".format(nUsers))
print("Num of movie : {}".format(nMovie))

print("Min rating : {}".format(min(rating_df['rating'])))
print("Max rating : {}".format(max(rating_df['rating'])))

"""Membagi jumlah data untuk training dan testing"""

# mengacak sample data
rating_df = rating_df.sample(frac = 1, random_state = 73)

X = rating_df[['user', 'movie']].values
Y = rating_df["rating"]

# membagi data
test_size = 200000
train_indices = rating_df.shape[0] - test_size
X_train, X_test, Y_train, Y_test = (X[:train_indices], X[train_indices:], Y[:train_indices], Y[train_indices:])

# membagi data untuk modelling
X_train_array = [X_train[:, 0], X_train[:, 1]]
X_test_array = [X_test[:, 0], X_test[:, 1]]

"""Embedding layer"""

def model_preparation():
    user = Input(name = 'user', shape = [1])
    user_embedding = Embedding(name = 'user_embedding', input_dim = nUsers, output_dim = 128)(user)

    movie = Input(name = 'movie', shape = [1])
    movie_embed = Embedding(name = 'movie_embedding', input_dim = nMovie, output_dim = 128)(movie)
    
    # model menggunakan layer dot
    x = Dot(name = 'dot_product', normalize = True, axes = 2)([user_embedding, movie_embed])
    x = Flatten()(x)
        
    x = Dense(1, kernel_initializer = 'he_normal')(x)
    x = BatchNormalization()(x)
    x = Activation("sigmoid")(x)
    
    model = Model(inputs = [user, movie], outputs = x)
    model.compile(loss = 'binary_crossentropy', 
                  metrics = ["mse", tf.keras.metrics.Precision(), tf.keras.metrics.Recall()],
                  optimizer = 'Adam')
    
    return model

"""Menampilkan model"""

model = model_preparation()
model.summary()

"""Melakukan training model embedding"""

best_model = ModelCheckpoint(filepath = './weight.h5',
                             save_weights_only = True,
                             monitor = 'val_loss',
                             mode = 'min',
                             save_best_only = True)

early_stopping = EarlyStopping(patience = 1, 
                               monitor = 'mse', 
                               mode = 'min', 
                               restore_best_weights = True)

my_callbacks = [best_model,
                early_stopping]

"""Melakukan training model"""

hist = model.fit(x = X_train_array,
                 y = Y_train,
                 validation_data = (X_test_array, Y_test),
                 epochs = 30,
                 batch_size = 64,
                 verbose = 1,
                 callbacks = my_callbacks)

"""Menampilkan plot loss"""

plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Loss Train', 'Loss Test'], loc = 'upper right')
plt.show

"""Menampilkan plot mse"""

plt.plot(hist.history['mse'])
plt.plot(hist.history['val_mse'])
plt.ylabel('MSE')
plt.xlabel('Epoch')
plt.legend(['MSE Train', 'MSE Test'], loc = 'upper right')
plt.show

"""Menampilkan plot recall"""

plt.plot(hist.history['recall'])
plt.plot(hist.history['val_recall'])
plt.ylabel('Recall')
plt.xlabel('Epoch')
plt.legend(['Recall Train', 'Recall Test'], loc = 'upper right')
plt.show

"""Menampilkan plot Precission"""

plt.plot(hist.history['precision'])
plt.plot(hist.history['val_precision'])
plt.ylabel('Precision')
plt.xlabel('Epoch')
plt.legend(['Precision Train', 'Precision Test'], loc = 'upper right')
plt.show

"""Melakukan load weight model"""

def load_weight(name, model):
    weights = model.get_layer(name).get_weights()[0]
    weights = weights / np.linalg.norm(weights, axis = 1).reshape((-1, 1))
    return weights
    
movie_weights = load_weight('movie_embedding', model)
user_weights = load_weight('user_embedding', model)

"""Mencari MovieId berdasarkan judul"""

def movie_data(movie):
    if isinstance(movie, int):
        return movie_df[movie_df.movieId == movie]
    if isinstance(anime, str):
        return movie_df[movie_df.title == movie]

"""Melakukan collaborative filtering"""

rating_by_user = rating_df.groupby('userId').size()
random_user = rating_by_user[rating_by_user < 1000].sample(1, random_state = None).index[0]

# memasukkan id user secara random
print('User ID : ', random_user)
top_movie_user = new_movie_df.groupby('userId').get_group(random_user)
top_movie_user[['rating', 'title', 'genres']].sort_values(by = 'rating', ascending = False)

"""Mencari kemiripan user"""

def get_similar_users(tempId, n = 10):
      index = tempId
      weights = user_weights
      dists = np.dot(weights, weights[encodedUser.get(index)])
      sortedDists = np.argsort(dists)
      n += 1
      closest = sortedDists[-n:]
      print('User that similar to user #{}'.format(tempId))
      
      SimilarArr = []
      
      for close in closest:
          similarity = dists[closest]

          if isinstance(tempId, int):
              SimilarArr.append({"similar_users" : encodeusertouser.get(close), "similarity" : similarity})

      Frame = pd.DataFrame(SimilarArr)
      return Frame

"""Menampilkan list rekomendasi movie berdasarkan aktivitas tontonan movie user"""

def get_user_movie_preference(userId, plot = False, temp = 1):
  
  # menentukan batas rating terendah movie
  lowest_rating = np.percentile(rating_df[rating_df.userId == userId].rating, 75)
  rating_df[rating_df.userId == userId] = rating_df[rating_df.userId == userId][rating_df[rating_df.userId == userId].rating >= lowest_rating]
  top_movie_refference = (rating_df[rating_df.userId == userId].sort_values(by = "rating", ascending = False).movieId.values)
  
  user_pref_df = movie_df[movie_df["movieId"].isin(top_movie_refference)]
  user_pref_df = user_pref_df[["movieId","title", "genres"]]
  
  if temp != 0:
      print("User #{} Sudah Menilai {} film dengan peringkat rata-rata = {:.1f}/5.0".format(
        userId, len(rating_df[rating_df.userId==userId]),
        rating_df[rating_df.userId==userId]['rating'].mean()*5,
      ))
      print('Genre film yang direkomendasikan untuk User : ')

  return user_pref_df

"""Menampilkan 8 rekomendasi movie"""

reff_user = get_user_movie_preference(random_user, plot = True)
reff_user = pd.DataFrame(reff_user)
reff_user.head(8)