"""This script contains paths that are referenced in genre_gender_app.py
for running locally. genre_gender_app.py should call app_dir_aws.py for 
deployment on aws."""

#reference the datetime used to title the data
now = '2020-07-07-09-58'

# import the data
path_X_train = './wiki-kaggle_X_train_{}.csv'.format(now)
path_y_train = './wiki-kaggle_y_train_{}.csv'.format(now)
path_X_test = './wiki-kaggle_X_test_{}.csv'.format(now)
path_y_test = './wiki-kaggle_y_test_{}.csv'.format(now)

path_genre_list = './genre_list_{}.csv'.format(now)

