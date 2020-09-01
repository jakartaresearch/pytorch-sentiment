import os
import glob
import torch
from bs4 import BeautifulSoup

from torchsenti.datasets.utils import download_and_extract_archive

class ProsAndCons:
    """
    dataset is from www.cs.uic.edu/~liub/FBS/pros-cons.rar
    """
    
    resources = ('https://www.cs.uic.edu/~liub/FBS/pros-cons.rar')
    
    def __init__(self, root='.', download=False):
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
        filename = self.resources.rpartition('/')[2]
        download_and_extract_archive(self.resources, download_root=self.raw_folder, filename=filename)

        print('Done!')
    
    def parse_bs(self, strings, nametag):
        soup = BeautifulSoup(strings, 'lxml')
        
        text_list = []
        label_list = []
        
        tag_list = soup.find_all(nametag)
        for tag in tag_list:
            text = tag.text
            
            text_list.append(text)
            label_list.append(nametag)
        
        return text_list, label_list
        
    @property
    def get_dict(self):
        data_dict = {'text': [], 'label': []}
        with open(os.path.join(self.raw_folder, 'IntegratedPros.txt'), 'r', encoding='ISO-8859-1') as file:
            data = file.read()
            
            text_list, label_list = self.parse_bs(data, 'pros')
            
            data_dict['text'].extend(text_list)
            data_dict['label'].extend(label_list)
        
        with open(os.path.join(self.raw_folder, 'IntegratedCons.txt'), 'r', encoding='ISO-8859-1') as file:
            data = file.read()
            
            text_list, label_list = self.parse_bs(data, 'cons')
            
            data_dict['text'].extend(text_list)
            data_dict['label'].extend(label_list)
            
        return data_dict