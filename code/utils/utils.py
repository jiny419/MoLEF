import copy
import time
import nltk
import json
from gensim.models import KeyedVectors
import h5py
import numpy as np
from torch import nn

def clones(module, N):
    return nn.ModuleList([copy.deepcopy(module) for _ in range(N)])

""" Vid and text features helpers """
def load_feature(filename, dataset='Activitynet'):
    if dataset in ['Activitynet', 'Tacos', 'Charades', 'Didemo', 'Youcook2', 'Tvr', 'Msrvtt']:
        return np.load(filename).astype(np.float32)
    return None

def load_json(file_path, verbose=True):
    if verbose:
        print("Load json file from {}".format(file_path))
    return json.load(open(file_path, "r"))

def load_word2vec(filename, binary=True):
    word2vec = KeyedVectors.load_word2vec_format(filename, binary=binary)
    return word2vec

def tokenize(sentence, word2vec):
    punctuations = ['.', '?', ',', '', '(', ')']
    raw_text = sentence.lower()
    words = nltk.word_tokenize(raw_text)
    words = [word for word in words if word not in punctuations]
    return [word for word in words if word in word2vec]

def generate_anchors(dataset='Activitynet'):
    if dataset == 'Activitynet':
        widths = np.array([16, 32, 64, 96, 128, 160, 192])
        center = 7.5
        start = center - 0.5 * (widths - 1)
        end = center + 0.5 * (widths - 1)
    elif dataset == 'Tacos':
        widths = np.array([8, 16, 32, 64])#np.array([6, 18, 32])
        center = 7.5
        start = center - 0.125 * (widths - 1)
        end = center + 0.125 * (widths - 1)
    elif dataset == 'Didemo':
        widths = np.array([8, 16, 32, 64])#np.array([6, 18, 32])
        center = 7.5
        start = center - 0.125 * (widths - 1)
        end = center + 0.125 * (widths - 1)
    elif dataset == 'Charades':
        widths = np.array([16, 24, 32, 40])#np.array([6, 18, 32])
        center = 7.5
        start = center - 0.125 * (widths - 1)
        end = center + 0.125 * (widths - 1)
    elif dataset == 'Youcook2' :
        widths = np.array([8, 16, 32, 64])
        center = 7.5
        start = center - 0.125 * (widths - 1)
        end = center + 0.125 * (widths - 1)    
    elif dataset == 'Msrvtt':
        widths = np.array([16, 32, 64, 96, 128, 160, 192])
        center = 7.5
        start = center - 0.5 * (widths - 1)
        end = center + 0.5 * (widths - 1)
    elif dataset == 'Tvr' :
        widths = np.array([16, 32, 64, 96, 128, 160, 192])
        center = 7.5
        start = center - 0.5 * (widths - 1)
        end = center + 0.5 * (widths - 1)

    else:
        return None
    return np.stack([start, end], -1)

class CountMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = np.zeros([2, 4],dtype=np.float32)
        self.count = 0

    def update(self, val, n=1):
        self.val += val
        self.count += n

class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


class TimeMeter(object):
    """Computes the average occurrence of some event per second"""

    def __init__(self, init=0):
        self.reset(init)

    def reset(self, init=0):
        self.init = init
        self.start = time.time()
        self.n = 0

    def update(self, val=1):
        self.n += val

    @property
    def avg(self):
        return self.n / self.elapsed_time

    @property
    def elapsed_time(self):
        return self.init + (time.time() - self.start)


class StopwatchMeter(object):
    """Computes the sum/avg duration of some event in seconds"""

    def __init__(self):
        self.reset()

    def start(self):
        self.start_time = time.time()

    def stop(self, n=1):
        if self.start_time is not None:
            delta = time.time() - self.start_time
            self.sum += delta
            self.n += n
            self.start_time = None

    def reset(self):
        self.sum = 0
        self.n = 0
        self.start_time = None

    @property
    def avg(self):
        return self.sum / self.n

# for recording log time 
class Timer:
    DEFAULT_TIME_FORMAT_DATE_TIME = "%Y/%m/%d %H:%M:%S"
    DEFAULT_TIME_FORMAT = ["%03dms", "%02ds", "%02dm", "%02dh"]

    def __init__(self):
        self.start = time.time() * 1000

    def get_current(self):
        return self.get_time_hhmmss(self.start)

    def reset(self):
        self.start = time.time() * 1000

    def get_time_since_start(self, format=None):
        return self.get_time_hhmmss(self.start, format)

    def unix_time_since_start(self, in_seconds=True):
        gap = time.time() * 1000 - self.start

        if in_seconds:
            gap = gap // 1000

        # Prevent 0 division errors
        if gap == 0:
            gap = 1
        return gap

    def get_time_hhmmss(self, start=None, end=None, gap=None, format=None):
        """
        Calculates time since `start` and formats as a string.
        """
        if start is None and gap is None:

            if format is None:
                format = self.DEFAULT_TIME_FORMAT_DATE_TIME

            return time.strftime(format)

        if end is None:
            end = time.time() * 1000
        if gap is None:
            gap = end - start

        s, ms = divmod(gap, 1000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)

        if format is None:
            format = self.DEFAULT_TIME_FORMAT

        items = [ms, s, m, h]
        assert len(items) == len(format), "Format length should be same as items"

        time_str = ""
        for idx, item in enumerate(items):
            if item != 0:
                time_str = format[idx] % item + " " + time_str

        # Means no more time is left.
        if len(time_str) == 0:
            time_str = "0ms"

        return time_str.strip()
