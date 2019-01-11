#!/usr/bin/env python
#
# Script to convert DICOM data to NIFTI and organize into BIDS structure.
#
# Dependencies:
#   dcm2niix
#
# Usage:
#   python convert_dcm2nii.py -d FOLDER_DICOM
#
# Authors: Alexandru Foias, Julien Cohen-Adad

# TODO: convert in temp folder

import os, glob, argparse, shutil, tempfile
import nibabel as nib

def get_parameters():
    parser = argparse.ArgumentParser(description='Convert DICOM data to NIFTI and organize into BIDS structure. The '
                                                 'BIDS structure is specific to the spine_generic project. More info at: '
                                                 'https://github.com/sct-pipeline/spine_generic')
    parser.add_argument('-d', '--path-dicom',
                        help='Path to input DICOM directory.',
                        required=True)
    parser.add_argument('-s', '--subject',
                        help='Subject number (e.g. sub-03). Required by BIDS to name folders and files.',
                        required=True)
    parser.add_argument('-o', '--path-output',
                        help='Path to output BIDS dataset directory. Default is current directory.',
                        required=False)
    args = parser.parse_args()
    return args


def convert_dcm2nii(path_data, subject, path_out='./'):
    """
    Convert DICOM data to BIDS-compatible NIFTI files.
    :param path_data: Path to input DICOM directory
    :param subject: Subject number (e.g. sub-03). Required by BIDS to name folders and files
    :param path_out: Path to output BIDS dataset directory
    :return:
    """

    # Dictionary of BIDS naming. First element: file name suffix, Second element: destination folder.
    # Note: this dictionary is based on the spine_generic protocol, but could be extended to other usage:
    contrast_dict = {
        'GRE-MT0': ('acq-MToff_MTS', 'anat'),
        'GRE-MT1': ('acq-MTon_MTS', 'anat'),
        'GRE-T1': ('acq-T1w_MTS', 'anat'), # This is a hack for Philips
        'GRE-T1w': ('acq-T1w_MTS', 'anat'),
        'GRE-ME': ('T2star', 'anat'),
        'T1w': ('T1w', 'anat'),
        'T2w': ('T2w', 'anat'),
        'DWI': ('dwi', 'dwi'),
    }

    # Convert dcm to nii
    path_tmp = tempfile.mkdtemp()

    os.system('dcm2niix -b y -z y -x n -v y -o ' + path_tmp + ' ' + path_data)

    # Loop across NIFTI files and move converted files to output dir
    if not os.path.exists(path_out):
        os.makedirs(path_out)
    os.chdir(path_tmp)
    nii_files = glob.glob(os.path.join(path_tmp, '*.nii.gz'))

    # Hacking for Philips scanners (and other potential outliers in other vendors)
    for nii_file in nii_files:
        # Identify MT volume
        if "GRE-MT" in nii_file:
            # Make sure it is concatenated along t, i.e., len(dim3)=2
            img = nib.load(nii_file)
            if len(img.shape) == 4:
                print("WARNING: Detected 4D MT scan (likely Philips system). Splitting into MT1 and MT0 3D Nifti files.")
                # Name the file with key present in contrast_dict{} so it is identified later on
                nib.save(nib.Nifti1Image(img.get_data()[:, :, :, 0], img.affine, img.header), 'tmp_GRE-MT0.nii.gz')
                nib.save(nib.Nifti1Image(img.get_data()[:, :, :, 1], img.affine, img.header), 'tmp_GRE-MT1.nii.gz')
                # And copy the json
                shutil.copy(nii_file.strip('.nii.gz') + '.json', 'tmp_GRE-MT0.json')
                shutil.copy(nii_file.strip('.nii.gz') + '.json', 'tmp_GRE-MT1.json')
        # Identify DWI scan
        if "DWI" in nii_file:
            img = nib.load(nii_file)
            # Check if file is metric (FA, ADC, etc.) instead of DWI time series
            # TODO: Make sure there are no metric files with dim(3) != 1 (e.g. Tensor files)
            if len(img.shape) == 3:
                os.remove(nii_file)

    # If multiple GRE-ME files, then only consider the one with "sum" in file name
    ind_gre = [nii_files.index(nii_file) for nii_file in nii_files if "GRE-ME" in nii_file]
    if not len(ind_gre) == 1:
        print('WARNING: Detected multiple GRE-ME scans. Only keeping the file which contains "sum".')
        ind_gre_sum = [nii_files.index(nii_file) for nii_file in nii_files if "sSUM" in nii_file]
        if len(ind_gre_sum) == 1:
            # Remove each individual echo
            for i_file in ind_gre:
                os.remove(nii_files[i_file])
            # And rename the sSUM with GRE-ME in file name
            shutil.copy(nii_files[ind_gre_sum[0]], 'tmp_GRE-ME.nii.gz')
            shutil.copy(nii_files[ind_gre_sum[0]].strip('nii.gz') + '.json', 'tmp_GRE-ME.json')
        else:
            print('WARNING: Cannot find sSUM scan.')

    # Main Loop (file name should be consistent with contrast_dict at this point)
    nii_files = glob.glob(os.path.join(path_tmp, '*.nii.gz'))  # need to reinitialize in case temp files were created
    for nii_file in nii_files:
        # Loop across contrasts
        for contrast in list(contrast_dict.keys()):
            # Check if file name includes contrast listed in dict
            if contrast in nii_file:
                print("Detected: "+nii_file+" --> "+contrast)
                # Fetch all files with same base name (to include json, bval, etc.), rename and move to BIDS output dir
                nii_file_all_exts = glob.glob(os.path.join(path_tmp, nii_file.strip('.nii.gz')) + '.*')
                for nii_file_all_ext in nii_file_all_exts:
                    # Build output file name
                    fname_out = os.path.join(path_out, subject, contrast_dict[contrast][1],
                                             subject + '_' + contrast_dict[contrast][0] + '.'
                                             + nii_file_all_ext.split(os.extsep, 1)[1])
                    if not os.path.exists(os.path.abspath(os.path.dirname(fname_out))):
                        os.makedirs(os.path.abspath(os.path.dirname(fname_out)))
                    # Move
                    shutil.move(nii_file_all_ext, fname_out)
                break


if __name__ == "__main__":
    args = get_parameters()
    convert_dcm2nii(args.path_dicom, args.subject, path_out=args.path_output)
