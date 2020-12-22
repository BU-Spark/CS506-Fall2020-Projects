import os

from modules.utilities import *
from modules.constants import *

import nltk
import numpy as np
import pandas as pd

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from sklearn.metrics import classification_report


def main():
    nltk.download('stopwords')
    nltk.download('wordnet')

    # get the positive training reviews
    positive_training = get_imdb_reviews(os.getcwd() + '/aclImdb/train/pos/')
    tmp = [int(e) for e in '1'*len(positive_training)]
    df_pos = pd.DataFrame({
        'Reviews': positive_training,
        'Class': tmp
    }).astype({'Reviews': str})

    # get the negative training reviews
    negative_training = get_imdb_reviews(os.getcwd() + '/aclImdb/train/neg/')
    tmp = [int(e) for e in '0' * len(negative_training)]
    df_neg = pd.DataFrame({
        'Reviews': negative_training,
        'Class': tmp
    }).astype({'Reviews': str})

    # shuffled training dataframe of pos + negative reviews
    df_training = pd.concat([df_pos, df_neg], axis=0).sample(frac=1)

    df_training['Reviews'] = df_training['Reviews'].apply(lambda x: clean_text(x))

    # entire dataset of iMDB (cleaned + pos + neg)
    print(df_training.head())

    # max_length = int(df_training['Reviews'].apply(lambda x: len(x.split(" "))).max())

    tokenizer = Tokenizer(num_words=MAX_FEATURES, split=' ')
    tokenizer.fit_on_texts(df_training['Reviews'])
    list_tokenized_train = tokenizer.texts_to_sequences(df_training['Reviews'])

    X_train = pad_sequences(list_tokenized_train)
    y_train = df_training['Class']

    # build LSTM model
    # First implementation of BiLSTM w/ Attention
    model = build_bidirectional_lstm(N=np.array(X_train).shape[1],
                                     max_features=MAX_FEATURES,
                                     embed_size=EMBED_SIZE,
                                     is_attention=True)

    # summarize layers
    print(model.summary())

    history = model.fit(X_train,
                        y_train,
                        batch_size=BATCH_SIZE,
                        epochs=EPOCHS,
                        validation_split=0.1)

    # Loading the test dataset, and repeating the processing steps
    positive_testing = get_imdb_reviews(os.getcwd() + '/aclImdb/test/pos/')
    tmp = [int(e) for e in '1'*len(positive_testing)]
    df_pos = pd.DataFrame({
        'Reviews': positive_testing,
        'Class': tmp
    }).astype({'Reviews': str})

    # get the negative training reviews
    negative_testing = get_imdb_reviews(os.getcwd() + '/aclImdb/test/neg/')
    tmp = [int(e) for e in '0' * len(negative_testing)]
    df_neg = pd.DataFrame({
        'Reviews': negative_testing,
        'Class': tmp
    }).astype({'Reviews': str})

    # shuffled training dataframe of pos + negative reviews
    df_testing = pd.concat([df_pos, df_neg], axis=0).sample(frac=1)

    df_testing['Reviews'] = df_testing['Reviews'].apply(lambda x: clean_text(x))
    df_testing.head()

    # max_length = int(df_testing['Reviews'].apply(lambda x: len(x.split(" "))).mean())

    tokenizer.fit_on_texts(df_testing['Reviews'])
    list_tokenized_test = tokenizer.texts_to_sequences(df_testing['Reviews'])
    X_test = pad_sequences(list_tokenized_test)
    y_test = df_testing['Class']

    # Making predictions on our model
    prediction = model.predict(X_test)
    y_pred = (prediction > 0.5)

    # plot the confusion matrix
    plot_confusion_matrix(y_test, y_pred)

    # print the classification report
    print(classification_report(y_test, y_pred))

    # plot the model history metrics
    plot_model_metrics(history)

    # plot the ROC curve
    plot_roc_curve(y_test, y_pred)


if __name__ == '__main__':
    main()
