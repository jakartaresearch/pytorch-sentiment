import os
import os.path
import glob
import torch

from torchsenti.datasets.utils import download_and_extract_archive

class MovieReview():
    
    """
    This README v2.0 (June, 2004) for the v2.0 polarity dataset 
    comes from the URL http://www.cs.cornell.edu/people/pabo/movie-review-data

    """
    
    resources = ('https://drive.google.com/uc?id=1jRR6G0-Di2jWO0jkciCWL1hO8b3tLt0y')
    filename = 'review_polarity.tar.gz'
    
    def __init__(self, root=".", download=False):
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
        """Download the dataset if it doesn't exist in raw_folder already."""

        if self._check_exists():
            return

        os.makedirs(self.raw_folder, exist_ok=True)
        os.makedirs(self.processed_folder, exist_ok=True)

        # download files
        download_and_extract_archive(self.resources, download_root=self.raw_folder, filename=self.filename)

        print('Done!')
    
    def read_txt(self, path):
        with open(path, 'r') as f:
            data = f.read()
            
        return data
    
    @property
    def get_dict(self):
        paths = glob.glob(os.path.join(self.raw_folder, 'txt_sentoken', '*', '*'))
        
        data_dict = {'text': [], 'label': []}
        for path in paths:
            sentiment = path.split('/')[-2]
            review = self.read_txt(path)
            
            data_dict['text'].append(review)
            data_dict['label'].append(sentiment)
        
        return data_dict
    
    def set_split(self):
        data_dict = self.get_dict
        
        X_train= data_dict['text']
        y_train = data_dict['label']
        
        return X_train, y_train