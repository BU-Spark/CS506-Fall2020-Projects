"""
    File to define global constants
"""
import tensorflow.keras

MAX_FEATURES = 2000
EMBED_SIZE = 128
RNN_CELL_SIZE = 32
BATCH_SIZE = 128
EPOCHS = 3
METRICS = [
    tensorflow.keras.metrics.TruePositives(name='tp'),
    tensorflow.keras.metrics.FalsePositives(name='fp'),
    tensorflow.keras.metrics.TrueNegatives(name='tn'),
    tensorflow.keras.metrics.FalseNegatives(name='fn'),
    tensorflow.keras.metrics.BinaryAccuracy(name='accuracy'),
    tensorflow.keras.metrics.Precision(name='precision'),
    tensorflow.keras.metrics.Recall(name='recall'),
    tensorflow.keras.metrics.AUC(name='auc'),
]

