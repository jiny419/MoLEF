import os
from yacs.config import CfgNode as CN

_C = CN()

##############
#### MISC ####
_C.EXPERIMENT_NAME = ""
_C.ENGINE_STAGE = "TRAINER"
_C.LOG_DIRECTORY = ""
_C.VISUALIZATION_DIRECTORY = ""
_C.PATHS_CATALOG = os.path.join(os.path.dirname(__file__), "paths_catalog.py")

##############
#### TEST ####
_C.TEST = CN()
_C.TEST.MODEL = ""

##################
#### Dataset #####

_C.DATASETS = CN()
_C.DATASETS.NUMBER_CLASSES = 200
_C.DATASETS.PORTION_OF_DATA = 1.

_C.DATASETS.TRAIN = ""
_C.DATASETS.TEST = ""
_C.DATASETS.TRAIN_SAMPLES = 0.
_C.DATASETS.TEST_SAMPLES = 0.


##################
#### Sentence #####

_C.SENTENCE = CN()
_C.SENTENCE.MIN_COUNT = 5
_C.SENTENCE.TRAIN_MAX_LENGTH = 30
_C.SENTENCE.TEST_MAX_LENGTH = 30

################
#### MODELS ####

_C.DYNAMIC_FILTER = CN(new_allowed=True)
_C.DYNAMIC_FILTER.TAIL_MODEL = "LSTM"
_C.DYNAMIC_FILTER.POOLING    = "MeanPoolingLayer"
_C.DYNAMIC_FILTER.HEAD_MODEL = "MLP"

_C.REDUCTION = CN()
_C.REDUCTION.INPUT_SIZE = 1024
_C.REDUCTION.OUTPUT_SIZE = 512

_C.LOCALIZATION = CN()
_C.LOCALIZATION.INPUT_SIZE = 512
_C.LOCALIZATION.HIDDEN_SIZE = 256
_C.LOCALIZATION.NUM_LAYERS = 2
_C.LOCALIZATION.BIAS = False
_C.LOCALIZATION.DROPOUT = 0.5
_C.LOCALIZATION.BIDIRECTIONAL = True
_C.LOCALIZATION.BATCH_FIRST = True

_C.CLASSIFICATION = CN()
_C.CLASSIFICATION.INPUT_SIZE = 512
_C.CLASSIFICATION.OUTPUT_SIZE = 1

_C.LOSS = CN()
_C.LOSS.ATTENTION = True
###################
#### OPTIMIZER ####

_C.SOLVER = CN(new_allowed=True)
_C.SOLVER.TYPE = "ADAM"
_C.SOLVER.EPSILON = 0.1

####################
#### EXPERIMENT ####
_C.BATCH_SIZE_TRAIN = 16
_C.BATCH_SIZE_TEST = 16
_C.NUM_WORKERS_TRAIN = 4
_C.NUM_WORKERS_TEST = 4
_C.EPOCHS = 10


####################
##### TSGV ########
_C.max_num_words = 20
_C.max_num_nodes = 20
_C.max_num_frames = 200
_C.d_model = 512
_C.num_heads = 4
_C.batch_size = 64
_C.dropout = 0.2
# _C.word_dim = 300
_C.word_dim = 768 # for tvr
# _C.frame_dim = 500
_C.frame_dim = 3072
_C.num_gcn_layers = 2
_C.num_attn_layers = 2
_C.is_adj = False
_C.iou = [0.1, 0.3, 0.5, 0.7]

