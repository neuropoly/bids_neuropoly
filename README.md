# bids_neuropoly
Python package that deals with BIDS structure for filtering data (specific to NeuroPoly developments)

## Installation
~~~
git clone https://github.com/neuropoly/bids_neuropoly.git
cd bids_neuropoly
pip install -e .
~~~

## Convert Dicom to BIDS-compatible Nifti dataset
Example:
~~~
python scripts/convert_dcm2nii.py -d /Users/julien/Desktop/DICOM -s sub-03 -o /Users/julien/bids_dataset
~~~
