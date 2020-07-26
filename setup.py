from setuptools import setup, find_packages
from version import VERSION

here = path.abspath(path.dirname(__file__))

sys.path.insert(0, path.join(here, 'torchmeta'))

setup(
    name='torchsenti',
    version=VERSION,
    description='Sentiment Analysis Library for Researcher with PyTorch',
    license='MIT',
    author='Andreas Chandra, Ruben Stefanus, and Andhika Setia Pratama',
    author_email='andestjen@gmail.com',
    url='https://github.com/jakartaresearch/pytorch-sentiment',
    keywords=['sentiment-analysis', 'pytorch', 'deep-learning', 'machine-learning'],
    packages=find_packages(exclude=['docs', 'tests', 'examples']),
    install_requires=[
        'torch>=1.4.0,<1.6.0',
    ],
    package_data={'torchsenti': ['torchsenti/datasets/assets/*']},
    include_package_data=False,
    classifiers=[
        'Development Status :: 0.0.1 - Development/Alpha',
        'Topic :: Natural Language Processing :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)