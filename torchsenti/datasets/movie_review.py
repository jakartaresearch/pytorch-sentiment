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
    
    resources = ('http://www.cs.cornell.edu/people/pabo/movie-review-data/review_polarity.tar.gz')
    
    def __init__(self, root, download=False):
        self.root = root
        self.download = download

        if self.download:
            self.download_data()

        if not self._check_exists():
            raise RuntimeError('Dataset not found.' +
                               ' You can use download=True to download it')
    
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
    
    