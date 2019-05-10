import os,glob, argparse, shutil, csv, json

def get_parameters():
    parser = argparse.ArgumentParser(description='Convert multisubj datasets tsv into only one dataset tsv')
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
    header_tsv = ["participant_id","sex","age","date_of_scan","InstitutionName","Manufacturer","ManufacturersModelName", "ReceiveCoilName","SoftwareVersions", "Researcher"]
    path_participants_tsv = os.path.join(path_output,'participants.tsv')
    with open(path_participants_tsv, 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(header_tsv)
        for center in center_list:
            if center != ".DS_Store":
                path_input_participants_tsv = os.path.join(path_input,center,'participants.tsv')
                path_input_dataset_description_json = os.path.join(path_input,center,'dataset_description.json')
                with open(path_input_participants_tsv) as tsvfile:
                    reader = csv.reader(tsvfile, delimiter='\t')
                    next(reader)
                    for row in reader:
                        with open(path_input_dataset_description_json, 'r') as input_dataset_description_json:
                            input_dataset_description = json.load(input_dataset_description_json)
                            # print input_dataset_description
                            institution_name =  input_dataset_description["InstitutionName"]
                            manufacturer = input_dataset_description["Manufacturer"]
                            manufacturer_model = input_dataset_description["ManufacturersModelName"]
                            # print input_dataset_description.keys()
                            if "SoftwareVersions" in input_dataset_description.keys():
                                current_software_key = "SoftwareVersions"
                                software_version = input_dataset_description[current_software_key]
                            else:
                                if "SoftwareVersion" in input_dataset_description.keys():
                                    current_software_key = "SoftwareVersion"
                                    software_version = input_dataset_description[current_software_key]
                                else:
                                    software_version = "-"
                            researcher = input_dataset_description["Researcher"]
                            researcher = researcher.encode('ascii', 'ignore')
                            if "ReceiveCoilName" in input_dataset_description.keys():
                                receive_coil = input_dataset_description["ReceiveCoilName"]
                            else:
                                receive_coil = "-"
                        row.append(institution_name)
                        row.append(manufacturer)
                        row.append(manufacturer_model)
                        row.append(receive_coil)
                        row.append(software_version)
                        row.append(researcher)
                        centername = center.split("_")[0]
                        sub_id = row[0].split("-")[1]
                        new_subname = "sub-" + centername + sub_id
                        row[0] = new_subname
                        tsv_writer.writerow(row)
                        

if __name__ == "__main__":
    args = get_parameters()
    convert_multisubj(args.input, args.output)