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
        
        self.data = self.get_dict
        
        

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
    
    def _iter_path(self, path_list):
        data_dict = {'text': [], 'label': []}
        for path in path_list:
            content = self._read_txt(path)
            label = path.split('/')[-2]
            
            data_dict['text'].append(content)
            data_dict['label'].append(label)
            
        return data_dict
    
    @property
    def get_dict(self):
        """
        listing all path and read the file
        """
        train_pos = glob.glob(os.path.join(self.raw_folder, 'aclImdb', 'train', 'pos', '*'))
        train_neg = glob.glob(os.path.join(self.raw_folder, 'aclImdb', 'train', 'neg', '*'))
        test_pos = glob.glob(os.path.join(self.raw_folder, 'aclImdb', 'test', 'pos', '*'))
        test_neg = glob.glob(os.path.join(self.raw_folder, 'aclImdb', 'test', 'neg', '*'))
        
        data = self._iter_path(train_pos + train_neg + test_pos + test_neg)
        
        return data
    
    def split_dataset(self):
        """
        split data set into X_train, X_test, y_train, y_test
        """
        
        train_pos = glob.glob(os.path.join(self.raw_folder, 'aclImdb', 'train', 'pos', '*'))
        train_neg = glob.glob(os.path.join(self.raw_folder, 'aclImdb', 'train', 'neg', '*'))
        test_pos = glob.glob(os.path.join(self.raw_folder, 'aclImdb', 'test', 'pos', '*'))
        test_neg = glob.glob(os.path.join(self.raw_folder, 'aclImdb', 'test', 'neg', '*'))
        
        train = self._iter_path(train_pos+test_neg)
        X_train, y_train = train['text'], train['label']
        test = self._iter_path(train_neg+test_neg)
        X_test, y_test = test['text'], test['label']
        
        return X_train, X_test, y_train, y_tetst
        