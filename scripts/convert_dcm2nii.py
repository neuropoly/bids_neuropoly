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
    parser.add_argument("-d", "--data",
                        help="Path to DICOM directory",
                        required=True)
    args = parser.parse_args()
    return args

def main(path_data):
    """
    Main function
    :param path_data:
    :return:
    """
    path_out = './'

    contrast_dict = {
        'GRE-MT0': ('acq-MToff_MTS','anat'),
        'GRE-MT1': ('acq-MTon_MTS','anat'),
        'GRE-T1w': ('acq-T1w_MTS','anat'),
        'GRE-ME': ('T2star','anat'),
        'T1w': ('T1w', 'anat'),
        'T2w': ('T2w', 'anat'),
        'DWI': ('dwi', 'dwi'),
    }
   
    keylist_contrast = contrast_dict.keys()

    file_extension_dict = {'nii': 'nii.gz', 'json': 'json', 'bval': 'bval', 'bvec': 'bvec'}

    # Go to folder
    os.chdir(path_data)

    # Convert dcm to nii
    os.system('dcm2niix -b y -z y -x n -v y ' + path_out)

    # for dirName, subdirList, fileList in os.walk(path_data):
    #     for file in fileList:
    #         if file.startswith(file.split('-')[0] + '-0001.dcm'):
    #             init_path = os.path.join(dirName,file)
    #             os.system("dcm2niix -b y -z y " + init_path )
    # print '\n'

    # Loop across NIFTI files
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
                    fname_out = os.path.join(contrast_dict[contrast][1],
                                             contrast_dict[contrast][0] + '.' + nii_file.split(os.extsep, 1)[1])
                    os.makedirs(os.path.abspath(os.path.dirname(fname_out)), exist_ok=True)
                    # Move
                    shutil.move(nii_file_all_ext, fname_out)
                break

    # TODO: just loop across files instead of fetching all files+folder
    # for dirName, subdirList, fileList in os.walk(path_data):
    #     # Loop across all files in the local dir
    #     for file in fileList:
    #         if file.split('.')[1] in file_extension_dict :
    #             init_path = os.path.join(dirName,file)
    #             file_extension = file_extension_dict[file.split('.')[1]]
    #             current_contrast = file.split('_')[1]
    #
    #             # If file name includes contrast listed in dictionary, then rename and move in BIDS dir
    #             if current_contrast in contrast_dict:
    #                 root_new_path = '/'.join(dirName.split('/')[0:(len(dirName.split('/'))-2)])
    #
    #                 #Create BIDS folder structure
    #                 bids_folder_path = os.path.join(root_new_path,'bids_'+ (dirName.split('/')[(len(dirName.split('/'))-2)]),'sub-01',contrast_dict[current_contrast][1])
    #                 bids_file_path = os.path.join(bids_folder_path, 'sub-01_' + contrast_dict[current_contrast][0] + '.' + file_extension)
    #                 if not os.path.exists(bids_folder_path):
    #                     os.makedirs(bids_folder_path)
    #
    #                 os.rename(init_path,bids_file_path)

if __name__ == "__main__":
    args = get_parameters()
    main(args.data)