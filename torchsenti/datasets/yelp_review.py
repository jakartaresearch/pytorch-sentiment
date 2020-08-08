import os
import os.path
import glob
import shutil
import pandas as pd
import torch
import json
from torchsenti.datasets.utils import download_and_extract_archive
from tqdm import tqdm

class YelpReview:
    """ Yelp Review <https://drive.google.com/uc?id=1Ii9WF1Onh66wMHZKtGi55gw2dZ3m1Drd> 
    Mirror Link Dataset
    
    Args:
        root (string): Root directory of dataset where ``YelpReview/raw/*.json`` exist.
        
        processed (bool): If True = Download, extract, preprocessing dataset. 
        If False = Download and extract original dataset only
        
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
    
    """
    
    resources = ("https://drive.google.com/uc?id=1Ii9WF1Onh66wMHZKtGi55gw2dZ3m1Drd")
    
    def __init__(self, root, processed=False, download=False):
        self.root = root
        self.processed = processed
        self.download = download
        
        if self.download == True and os.path.exists(os.path.join(self.root, self.__class__.__name__)):
            raise RuntimeError('Already have the dataset')
                        
        if self.download:
            print('Download the dataset')
            os.makedirs(self.raw_folder, exist_ok=True)
            self.download_data()

        if self.processed:
            print('Get Processed Dataset !')
            os.makedirs(self.processed_folder, exist_ok=True)
            self.preprocessing_data()

        else :
            print('Get Raw Dataset !')

        if self.processed:
            if not self._check_exists_processed():
                raise RuntimeError('Processed Dataset not found.' +
                                   ' You can use download=True to download it')
        else:
            if not self._check_exists_raw():
                    raise RuntimeError('Raw Dataset not found.' +
                                       ' You can use download=True to download it')

    
    @property
    def raw_folder(self):
        return os.path.join(self.root, self.__class__.__name__, 'raw')
    
    @property
    def processed_folder(self):
        return os.path.join(self.root, self.__class__.__name__, 'processed')

    def _check_exists_raw(self):
        return (os.path.exists(self.raw_folder))
    
    def _check_exists_processed(self):
        return (os.path.exists(self.processed_folder))

    def download_data(self):
        """Download the YelpReview data if it doesn't exist in raw_folder already."""
        
        # download files
        filename = 'yelp_review.zip'
        download_and_extract_archive(self.resources, download_root=self.raw_folder, filename=filename)

        print('Done!')
        
            
    def preprocessing_data(self):
        """ Preprocessing *.json file """
        
        if os.path.exists(os.path.join(self.processed_folder, 'yelp_review.json')):
            print('yelp_review.json is already owned')
            return
        
        data_file = glob.glob(self.raw_folder+'/*.json')[0]
        
        processed_dict = []
        with open(data_file, 'r') as f:
            for line in tqdm(f):
                data = json.loads(line)
                # initializing Remove keys 
                rem_list = ['review_id', 'user_id', 'business_id', 'date'] 
                # Using pop() + list comprehension 
                # Remove multiple keys from dictionary 
                [data.pop(key) for key in rem_list]

                processed_dict.append(data)

        with open(os.path.join(self.processed_folder, 'yelp_review.json'), 'w') as fp:
            json.dump(processed_dict, fp)
                            
        print('Total reviews : ', len(processed_dict))
        print('Processed Done !')
        shutil.rmtree(self.raw_folder)
        
        
    def split_dataset(self, train_size, random_state):
        """
        Args :
            train_size : size of train data (between 0 and 1)
            random_state : seed value
        
        return X_train, y_train, X_test, y_test in DataFrame format
        """
        
        dataframe = pd.read_csv(os.path.join(self.processed_folder, 'yelp_review.json'))
        
        train = dataframe.sample(frac=train_size, random_state=random_state)
        test = dataframe.drop(train.index)
        
        X_train = train.Content
        y_train = train.iloc[:, 3:]
        
        X_test = test.Content
        y_test = test.iloc[:, 3:]
        
        return X_train, y_train, X_test, y_test