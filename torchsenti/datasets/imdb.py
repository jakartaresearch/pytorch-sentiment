import os
import os.path
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
    dataset_file = 'aclImdb_v1.pt'

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