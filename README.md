# bids_neuropoly
Python package that deals with BIDS structure for filtering data (specific to NeuroPoly developments)

## API Installation

Recommended installation of stable version is using PyPI and `pip`:
~~~
pip install bids-neuropoly
~~~

But you can also install the development version:
~~~
git clone https://github.com/neuropoly/bids_neuropoly.git
cd bids_neuropoly
pip install -e .
~~~

## Convert Dicom to BIDS-compatible Nifti dataset
Installation:
~~~
git clone https://github.com/neuropoly/bids_neuropoly.git
cd bids_neuropoly
pip install -r scripts/requirements.txt
~~~

Usage:
~~~
python scripts/convert_dcm2nii.py -d /Users/julien/Desktop/DICOM -s sub-03 -o /Users/julien/bids_dataset
~~~
