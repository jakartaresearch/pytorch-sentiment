import sys
import os.path as path
from setuptools import setup, find_packages
from torchsenti import __version__

here = path.abspath(path.dirname(__file__))

sys.path.insert(0, path.join(here, 'torchsenti'))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='torchsenti',
    version=__version__,
    description='A Sentiment Analysis Library for Research on top of PyTorch',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Ruben Stefanus, Andreas Chandra, and Andhika Setia Pratama',
    author_email='researchjair@gmail.com',
    url='https://github.com/jakartaresearch/pytorch-sentiment',
    keywords=['sentiment-analysis', 'pytorch', 'deep-learning', 'machine-learning'],
    install_requires=[
        'torch>=1.4.0,<1.6.0',
    ],
    include_package_data=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)