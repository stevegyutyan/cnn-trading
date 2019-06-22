from read_data import ReadData
from pipeline import PipeLine 
from strategies.training import TrainProcedureKeras
from preprocessing import PreprocessingProcedure1D, TrainingPreprocessingProcedure1D, TrainingPreprocessingProcedure1DBinary, GramMatrixPreprocessing


from strategies.neural_net import KerasLinear1D, KerasLinear1DSoftMax, ImageConvVGG16
from strategies.predicate import PredicateProcedureKeras
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
K.set_session(sess)





def train_pipeline():
    saved_model_path = "../models/saved_model_2.h5"
    data_path = '../data/bitstampUSD_1-min_data_2012-01-01_to_2019-03-13.csv',
    PipeLine(
        data_path,
        ReadData(),
        TrainingPreprocessingProcedure1D(),
        TrainProcedureKeras(
            KerasLinear1D(
                saved_model_path=saved_model_path,
            ),
            use_early_stop=False
        )
    ).execute()

def train_pipeline_gram_binary():
    saved_model_path = "../models/saved_model_gram.h5"
    data_path = '../data/bitstampUSD_1-min_data_2012-01-01_to_2019-03-13.csv',
    PipeLine(
        data_path,
        ReadData(),
        GramMatrixPreprocessing(),
        TrainProcedureKeras(
            ImageConvVGG16(),
            use_early_stop=True,
        )
    ).execute()


def train_pipeline_binary():
    saved_model_path = "../models/saved_model_binary.h5"
    data_path = '../data/bitstampUSD_1-min_data_2012-01-01_to_2019-03-13.csv',
    PipeLine(
        data_path,
        ReadData(),
        TrainingPreprocessingProcedure1DBinary(),
        TrainProcedureKeras(
            KerasLinear1DSoftMax(
                saved_model_path=saved_model_path,
            ),
            use_early_stop=False,
        )
    ).execute()


def backtest_pipeline():
    data_path = 'data/bitstampUSD_1-min_data_2012-01-01_to_2019-03-13.csv',
    saved_model_path = "models/saved_model.h5"
    PipeLine(
        data_path,
        ReadData,
        PreprocessingProcedure1D(),
        PredicateProcedureKeras(
            KerasLinear1D(
                saved_model_path=saved_model_path,
                model=open(saved_model_path, "rb")
            )
        )
    ).execute()
