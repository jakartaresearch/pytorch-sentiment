import os
import os.path
import glob
import torch
from torchsenti.datasets.utils import download_and_extract_archive

class IMDB:

    """
    IMDB: Large Movie Review Dataset
    http://ai.stanford.edu/~amaas/data/sentiment/index.html

    This is a dataset for binary sentiment classification containing substantially more data than previous benchmark datasets. 
    We provide a set of 25,000 highly polar movie reviews for training, and 25,000 for testing. 
    There is additional unlabeled data for use as well. Raw text and already processed bag of words formats are provided. 
    See the README file contained in the release for more details. 
    """

    resources = ("http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz")

    def __init__(self, root, download=False):
        self.root = root
        self.download = download

        if self.download:
            self.download_data()

        if not self._check_exists():
            raise RuntimeError('Dataset not found.' +
                               ' You can use download=True to download it')
        
        self.data = self._formating_data()

    @property
    def raw_folder(self):
        return os.path.join(self.root, self.__class__.__name__, 'raw')
    
    @property
    def processed_folder(self):
        return os.path.join(self.root, self.__class__.__name__, 'processed')

    def _check_exists(self):
        return (os.path.exists(self.raw_folder))

    def download_data(self):
        """Download the IMDB data if it doesn't exist in raw_folder already."""

        if self._check_exists():
            return

        os.makedirs(self.raw_folder, exist_ok=True)
        os.makedirs(self.processed_folder, exist_ok=True)

        # download files
        filename = self.resources.rpartition('/')[2]
        download_and_extract_archive(self.resources, download_root=self.raw_folder, filename=filename)

        print('Done!')
        
    def _read_txt(self, path):
        with open(path, 'r') as file:
            text = file.read()
            
        return text
    
    def _formating_data(self):
        train_pos_path_files = glob.glob(os.path.join(self.root, "IMDB/raw/aclImdb/train/pos/*"))
        train_neg_path_files = glob.glob(os.path.join(self.root, "IMDB/raw/aclImdb/train/neg/*"))
        
        test_pos_path_files = glob.glob(os.path.join(self.root, "IMDB/raw/aclImdb/test/pos/*"))
        test_neg_path_files = glob.glob(os.path.join(self.root, "IMDB/raw/aclImdb/test/neg/*"))
        
        train_pos_corpus = [self._read_txt(path) for path in train_pos_path_files[:5]]
        train_pos_label = ['positive'] * len(train_pos_corpus)
        train_neg_corpus = [self._read_txt(path) for path in train_neg_path_files[:5]]
        train_neg_label = ['negative'] * len(train_neg_corpus)
        
        X_train = train_pos_corpus + train_neg_corpus
        y_train = train_pos_label + train_neg_label
        
        test_pos_corpus = [self._read_txt(path) for path in test_pos_path_files[:5]]
        test_pos_label = ['postive'] * len(test_pos_corpus)
        test_neg_corpus = [self._read_txt(path) for path in test_neg_path_files[:5]]
        test_neg_label = ['negative'] * len(test_neg_corpus)
        
        X_test = test_pos_corpus + test_neg_corpus
        y_test = test_pos_label + test_neg_label
        
        return X_train, X_test, y_train, y_test
        
        