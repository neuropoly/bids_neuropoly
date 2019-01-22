# bids_neuropoly
Python package that deals with BIDS structure for filtering data (specific to NeuroPoly developments)

## Installation
~~~
https://github.com/neuropoly/bids_neuropoly.git
cd bids_neuropoly
pip install -e .
~~~

## Convert Dicom to BIDS-compatible Nifti dataset
Example:
~~~
python scripts/convert_dcm2nii.py -d /Users/julien/Desktop/DICOM -s sub-03 -o /Users/julien/bids_dataset
~~~

## Example using the API


```python
from bids_neuropoly import bids
```


```python
ds = bids.BIDS("./bids_unf_sct_ver1")
```


```python
ds
```




    DatasetDescription: SCT_dataset/unf_sct_ver1




```python
ds.participants
```




    Participants: 16




```python
ds.as_dataframe().tail()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>absolute_path</th>
      <th>data_type</th>
      <th>dataset_root</th>
      <th>modality</th>
      <th>subject_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>45</th>
      <td>/Users/perone/Devel/bids_neuropoly/tests/bids_...</td>
      <td>dwi</td>
      <td>/Users/perone/Devel/bids_neuropoly/tests/bids_...</td>
      <td>dwi</td>
      <td>sub-007</td>
    </tr>
    <tr>
      <th>46</th>
      <td>/Users/perone/Devel/bids_neuropoly/tests/bids_...</td>
      <td>anat</td>
      <td>/Users/perone/Devel/bids_neuropoly/tests/bids_...</td>
      <td>T2w</td>
      <td>sub-007</td>
    </tr>
    <tr>
      <th>47</th>
      <td>/Users/perone/Devel/bids_neuropoly/tests/bids_...</td>
      <td>anat</td>
      <td>/Users/perone/Devel/bids_neuropoly/tests/bids_...</td>
      <td>T1w</td>
      <td>sub-007</td>
    </tr>
    <tr>
      <th>48</th>
      <td>/Users/perone/Devel/bids_neuropoly/tests/bids_...</td>
      <td>anat</td>
      <td>/Users/perone/Devel/bids_neuropoly/tests/bids_...</td>
      <td>acq-MTon_MTR</td>
      <td>sub-007</td>
    </tr>
    <tr>
      <th>49</th>
      <td>/Users/perone/Devel/bids_neuropoly/tests/bids_...</td>
      <td>anat</td>
      <td>/Users/perone/Devel/bids_neuropoly/tests/bids_...</td>
      <td>acq-MToff_MTR</td>
      <td>sub-007</td>
    </tr>
  </tbody>
</table>
</div>




```python
subjects = ds.get_subjects()
```


```python
sub = subjects[2]
```


```python
sub
```




    Subject: sub-010/anat/T2w




```python
sub.has_derivative("labels")
```




    True




```python
sub.get_derivatives("labels")
```




    ['/Users/perone/Devel/bids_neuropoly/tests/bids_unf_sct_ver1/derivatives/labels/sub-010/anat/sub-010_T2w_seg-labeled.nii.gz',
     '/Users/perone/Devel/bids_neuropoly/tests/bids_unf_sct_ver1/derivatives/labels/sub-010/anat/sub-010_T2w_seg-manual.nii.gz',
     '/Users/perone/Devel/bids_neuropoly/tests/bids_unf_sct_ver1/derivatives/labels/sub-010/anat/sub-010_T2w_seg-manual.json',
     '/Users/perone/Devel/bids_neuropoly/tests/bids_unf_sct_ver1/derivatives/labels/sub-010/anat/sub-010_T2w_seg-labeled-discs.nii.gz']




```python
sub.has_metadata()
```




    True




```python
sub.metadata()
```




    {'Axial': 0.800000011920929,
     'Contrast': 't2',
     'Coronal': 0.800000011920929,
     'EndCoverage': '',
     'GmModel': False,
     'MsMapping': False,
     'Orientation': 'ax',
     'Pam50': False,
     'Sagittal': 0.799999952316284,
     'StartCoverage': ''}




```python
only_t1w = ds.query("modality == 'T1w'")
```


```python
only_t1w
```




    [Subject: sub-011/anat/T1w,
     Subject: sub-005/anat/T1w,
     Subject: sub-003/anat/T1w,
     Subject: sub-014/anat/T1w,
     Subject: sub-013/anat/T1w,
     Subject: sub-012/anat/T1w,
     Subject: sub-008/anat/T1w,
     Subject: sub-007/anat/T1w]




```python
len(only_t1w)
```




    8




```python
volume = only_t1w[1].load()
```


```python
print(volume.header)
```

    <class 'nibabel.nifti1.Nifti1Header'> object, endian='<'
    sizeof_hdr      : 348
    data_type       : b''
    db_name         : b'?TR:2300.000 TE:2.'
    extents         : 0
    session_error   : 0
    regular         : b'r'
    dim_info        : 0
    dim             : [  3 240 320 192   1   1   1   1]
    intent_p1       : 0.0
    intent_p2       : 0.0
    intent_p3       : 0.0
    intent_code     : none
    datatype        : int16
    bitpix          : 16
    slice_start     : 0
    pixdim          : [-1.0000000e+00  1.0000000e+00  1.0000000e+00  1.0000000e+00
      2.3000000e+00  1.0000000e+00  1.0000000e+00  5.9921805e+04]
    vox_offset      : 0.0
    scl_slope       : nan
    scl_inter       : nan
    slice_end       : 0
    slice_code      : unknown
    xyzt_units      : 10
    cal_max         : 0.0
    cal_min         : 0.0
    slice_duration  : 0.0
    toffset         : 0.0
    glmax           : 255
    glmin           : 0
    descrip         : b''
    aux_file        : b''
    qform_code      : scanner
    sform_code      : scanner
    quatern_b       : 0.47797507
    quatern_c       : -0.55276346
    quatern_d       : -0.44649944
    qoffset_x       : -83.7076
    qoffset_y       : 123.299805
    qoffset_z       : -103.766335
    srow_x          : [-9.8184394e-03 -6.7302868e-02  9.9768424e-01 -8.3707603e+01]
    srow_y          : [ -0.9895258    0.14435624   0.         123.299805  ]
    srow_z          : [ 1.44021943e-01  9.87234294e-01  6.80152774e-02 -1.03766335e+02]
    intent_name     : b''
    magic           : b'n+1'

