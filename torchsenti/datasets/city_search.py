import os
import os.path
import glob
import shutil
import pandas as pd
from tqdm import tqdm
import xml.etree.ElementTree as ET
import torch
from torchsenti.datasets.utils import download_and_extract_archive

class CitySearch:
    """ City Search Data <http://spidr-ursa.rutgers.edu/datasets/> Dataset
    
    Args:
        root (string): Root directory of dataset where ``CitySearch/raw/*`` exist.
        
        processed (bool): If True = Download, extract, combine to one .csv file. 
        If False = Download and extract original dataset only
        
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
    
    """
    
    resources = ("http://spidr-ursa.rutgers.edu/datasets/citysearch_data.zip")
    
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
            self.convert_data()
            data, target = self.load_dataset()
            self.data = data
            self.target = target

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
        """Download the CitySearch data if it doesn't exist in raw_folder already."""
        
        # download files
        filename = self.resources.rpartition('/')[2]
        download_and_extract_archive(self.resources, download_root=self.raw_folder, filename=filename)
        
        # Remove *.pos and *.cnk files
        file_pos = glob.glob(os.path.join(self.raw_folder,'citysearch_data', '*.pos'))
        file_cnk = glob.glob(os.path.join(self.raw_folder,'citysearch_data', '*.cnk'))
        
        for f in file_pos:
            os.remove(f)
        for f in file_cnk:
            os.remove(f)

        print('Done!')
        
            
    def convert_data(self):
        """Convert *.xml file to .csv file"""
        
        if os.path.exists(os.path.join(self.processed_folder, 'City Search Dataset.csv')):
            print('City Search Dataset.csv is already owned')
            return
        
        data_file = glob.glob(self.raw_folder+'/citysearch_data/*')
        
        column_names = ["Title", "Body", "Rating", "Pros", "Cons"]
        df = pd.DataFrame(columns = column_names)
        
        i = 0

        for file in data_file :
            tree = ET.parse(file)
            root = tree.getroot()
            reviews = root.find('Reviews')

            for child in reviews:
                new_row = {'Title':child.find('Title').text, 
                           'Body':child.find('Body').text,
                           'Rating':child.find('Rating').text,
                           'Pros':child.find('Pros').text, 
                           'Cons':child.find('Cons').text}
                df.loc[i] = new_row
                i += 1
                            
        print('Total reviews : ', len(df))
        
        df = df.replace(to_replace ="\n      ", value ="")
        df.to_csv(self.processed_folder+'/City Search Dataset.csv', index=False)
        
        print('Processed Done !')
        shutil.rmtree(self.raw_folder)
    
    
    def load_dataset(self):
        dataframe = pd.read_csv(os.path.join(self.processed_folder, 'City Search Dataset.csv'))
        data = dataframe[['Title','Body','Pros','Cons']]
        target = dataframe[['Rating']]
        return data, target
    
    def split_dataset(self, train_size, random_state):
        """
        Args :
            train_size : size of train data (between 0 and 1)
            random_state : seed value
        
        return X_train, y_train, X_test, y_test in DataFrame format
        """
        
        dataframe = pd.read_csv(os.path.join(self.processed_folder, 'City Search Dataset.csv'))
        
        train = dataframe.sample(frac=train_size, random_state=random_state)
        test = dataframe.drop(train.index)
        
        X_train = train[['Title','Body','Pros','Cons']]
        y_train = train[['Rating']]
        
        X_test = test[['Title','Body','Pros','Cons']]
        y_test = test[['Rating']]
        
        return X_train, y_train, X_test, y_test