import os
import os.path
import torch
from torchsenti.datasets.utils import download_and_extract_archive

class TripAdvisor:
    """ Trip Advisor <http://times.cs.uiuc.edu/~wang296/Data/> Dataset
    
    Args:
        root (string): Root directory of dataset where ``TripAdvisor/raw/*.dat`` exist.
            
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
    
    """
    
    resources = ("http://times.cs.uiuc.edu/~wang296/Data/LARA/TripAdvisor/Review_Texts.zip")
    dataset_file = 'dataset.pt'
    
    def __init__(self, root, download=False):
        self.root = root
        self.download = download
        
        if self.download:
            self.download_data()

        if not self._check_exists():
            raise RuntimeError('Dataset not found.' +
                               ' You can use download=True to download it')

        data_file = self.dataset_file
        
    
    @property
    def raw_folder(self):
        return os.path.join(self.root, self.__class__.__name__, 'raw')
    
    @property
    def processed_folder(self):
        return os.path.join(self.root, self.__class__.__name__, 'processed')

    def _check_exists(self):
        return (os.path.exists(self.raw_folder))

    def download_data(self):
        """Download the TripAdvisor data if it doesn't exist in raw_folder already."""

        if self._check_exists():
            return

        os.makedirs(self.raw_folder, exist_ok=True)
        os.makedirs(self.processed_folder, exist_ok=True)

        # download files
        filename = self.resources.rpartition('/')[2]
        download_and_extract_archive(self.resources, download_root=self.raw_folder, filename=filename)

        print('Done!')
            
