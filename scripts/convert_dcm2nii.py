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

import os, glob, argparse, shutil


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
        'GRE-T1w': ('acq-T1w_MTS', 'anat'),
        'GRE-ME': ('T2star', 'anat'),
        'T1w': ('T1w', 'anat'),
        'T2w': ('T2w', 'anat'),
        'DWI': ('dwi', 'dwi'),
    }

    # Convert dcm to nii
    os.makedirs(path_out, exist_ok=True)
    # os.chdir(path_data)
    os.system('dcm2niix -b y -z y -x n -v y -o ' + path_out + ' ' + path_data)

    # Loop across NIFTI files
    os.chdir(path_out)
    nii_files = glob.glob('*.nii.gz')
    for nii_file in nii_files:
        # Loop across contrasts
        for contrast in list(contrast_dict.keys()):
            # Check if file name includes contrast listed in dict
            if contrast in nii_file:
                print("Detected: "+nii_file+" --> "+contrast)
                # Fetch all files with same base name (to include json, bval, etc.), rename and move to BIDS output dir
                nii_file_all_exts = glob.glob(nii_file.strip('.nii.gz') + '.*')
                for nii_file_all_ext in nii_file_all_exts:
                    # Build output file name
                    fname_out = os.path.join(subject, contrast_dict[contrast][1],
                                             subject + '_' + contrast_dict[contrast][0] + '.'
                                             + nii_file.split(os.extsep, 1)[1])
                    os.makedirs(os.path.abspath(os.path.dirname(fname_out)), exist_ok=True)
                    # Move
                    shutil.move(nii_file_all_ext, fname_out)
                break


if __name__ == "__main__":
    args = get_parameters()
    convert_dcm2nii(args.path_dicom, args.subject, path_out=args.path_output)
