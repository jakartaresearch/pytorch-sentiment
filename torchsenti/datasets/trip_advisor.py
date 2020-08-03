import os
import os.path
import glob
import shutil
import pandas as pd
import torch
from torchsenti.datasets.utils import download_and_extract_archive

class TripAdvisor:
    """ Trip Advisor <http://times.cs.uiuc.edu/~wang296/Data/> Dataset
    
    Args:
        root (string): Root directory of dataset where ``TripAdvisor/raw/*.dat`` exist.
        
        processed (bool): If True = Download, extract, combine to one .csv file. 
        If False = Download and extract original dataset only
        
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
    
    """
    
    resources = ("http://times.cs.uiuc.edu/~wang296/Data/LARA/TripAdvisor/Review_Texts.zip")
    dataset_file = 'dataset.pt'
    
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

        data_file = self.dataset_file

    
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
        """Download the TripAdvisor data if it doesn't exist in raw_folder already."""
        
        # download files
        filename = self.resources.rpartition('/')[2]
        download_and_extract_archive(self.resources, download_root=self.raw_folder, filename=filename)

        print('Done!')
        
            
    def convert_data(self):
        """Convert *.dat file to .csv file"""
        
        data_file = glob.glob(self.raw_folder+'/*.dat')
        
        if len(data_file) == 0:
            raise RuntimeError('*.dat file not found')
        
        use_features = ['<Author>', '<Content>', '<Date>', '<No. Reader>', '<No. Helpful>',
                        '<Overall>', '<Value>', '<Rooms>', '<Location>', '<Cleanliness>',
                        '<Check in / front desk>', '<Service>', '<Business service>']
        
        # read *.dat
        all_dat_file = []
        for file in data_file:
            datContent = [i.strip() for i in open(file).readlines()][4:]
            all_dat_file.append(datContent)
        
        # Combine all *.dat
        reviews = []
        review = []

        for datContent in all_dat_file:
            for dat in datContent:
                if dat == '':
                    reviews.append(review)
                    review = []
                else :
                    for feat in use_features:
                        if feat in dat:
                            review.append(dat.split('>')[1])
                            
        print('Total reviews : ', len(reviews))
        
        col = ['Author','Content','Date','No.Reader','No.Helpful','Overall',
               'Value','Rooms','Location','Cleanliness','Check in front desk',
               'Service','Business service']

        df = pd.DataFrame(reviews, columns=col)
        
        df.to_csv(self.processed_folder+'/Trip Advisor Dataset.csv', index=False)
        
        print('Processed Done !')
        shutil.rmtree(self.raw_folder)