import os,glob, argparse, shutil

def get_parameters():
    parser = argparse.ArgumentParser(description='Convert multisubj datasets into only one dataset')
    parser.add_argument('-i', '--input',
                        help='Root path to input multisubj directory.',
                        required=True)
    parser.add_argument('-o', '--output',
                        help='Root path to output multisubj directory.',
                        required=True)
    args = parser.parse_args()
    return args


def convert_multisubj(path_input, path_output):
    center_list = os.listdir(path_input)
    for center in center_list:
        if center != ".DS_Store":
            centername = center.split("_")[0]
            for cwd, dirs, files in os.walk(os.path.join(path_input,center)):
                for item in files:
                    if item.startswith('sub'):
                        init_file_path = os.path.join(cwd,item)
                        print init_file_path
                        sub_subfolder = cwd.split("/")[-1]
                        sub_id = item.split("_")[0].split("-")[1]
                        new_subname = "sub-" + centername + sub_id
                        init_name_end = '_'.join(item.split("_")[1:])
                        new_filename = new_subname + '_' + init_name_end
                        new_file_folder_path = os.path.join(path_output,new_subname,sub_subfolder)
                        if not os.path.exists (new_file_folder_path):
                            os.makedirs (new_file_folder_path)
                        new_file_path = os.path.join(new_file_folder_path,new_filename)
                        print new_file_path
                        shutil.copyfile(init_file_path,new_file_path)

                        

if __name__ == "__main__":
    args = get_parameters()
    convert_multisubj(args.input, args.output)