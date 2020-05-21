import json

import nibabel
import pandas as pd
from pathlib import Path


class DatasetDescription(object):
    DATASET_DESCRIPTIO_FNAME = "dataset_description.json"

    def __init__(self, file_path):
        self.file_path = Path(file_path) / self.DATASET_DESCRIPTIO_FNAME
        if not self.file_path.exists():
            raise RuntimeError("The {} file was not found.".format(self.DATASET_DESCRIPTIO_FNAME))

        self.__parse_file()

    def __parse_file(self):
        with open(self.file_path, "r") as fp:
            self.json_content = json.load(fp)

    def __getitem__(self, key):
        return self.json_content[key]

    def keys(self):
        return self.json_content.keys()

    def __repr__(self):
        return "{}: {j[Name]}/{j[Study]}".format(self.__class__.__name__,
                                                 j=self.json_content)


class Participants(object):
    PARTICIPANTS_FNAME = "participants.tsv"

    def __init__(self, file_path):
        self.file_path = Path(file_path) / self.PARTICIPANTS_FNAME
        if not self.file_path.exists():
            raise RuntimeError("The {} file was not found.".format(self.PARTICIPANTS_FNAME))
        self.__parse_file()

    def __parse_file(self):
        self.content = pd.read_csv(self.file_path, sep='\t', encoding="ISO-8859-1")

    def get_by_participant_id(self, participant_id):
        return self.content[self.content["participant_id"] == participant_id]

    def query(self, query):
        return self.content.query(query)

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__,
                               len(self.content))


class Subject(object):
    def __init__(self, record):
        self.record = record

    def load(self):
        nib_file = nibabel.load(self.record.absolute_path)
        return nib_file

    def has_derivative(self, derivative_name):
        root_path = Path(self.record.dataset_root)
        derivatives = root_path / "derivatives" / derivative_name
        if derivatives.exists() and derivatives.is_dir():
            return True
        return False

    def __get_metadata_path(self):
        file_path = Path(self.record.absolute_path)
        metadata_fname = file_path.stem.split(".")[0]
        metadata_fname = metadata_fname + ".json"
        metadata_path = Path(self.record.absolute_path).parent / metadata_fname
        return metadata_path

    def has_metadata(self):
        metadata_path = self.__get_metadata_path()
        if not metadata_path.exists():
            return False
        return True

    def get_participant_id(self):
        return self.record.subject_id

    def metadata(self):
        if not self.has_metadata():
            raise RuntimeError("This subject does not have a metadata file.")
        metadata_path = self.__get_metadata_path()
        with open(metadata_path, "r") as fp:
            json_content = json.load(fp)
        return json_content

    def get_derivatives(self, derivative_name):
        if not self.has_derivative(derivative_name):
            raise RuntimeError("Derivative not found for this subject.")

        root_path = Path(self.record.dataset_root)
        derivatives = root_path / "derivatives" / derivative_name

        derivative_subj = derivatives / self.record.subject_id / self.record.data_type
        prefix_name = "{}_{}".format(self.record.subject_id, self.record.modality)

        all_available = []
        for i in derivative_subj.rglob(prefix_name + "_*"):
            all_available.append(str(i.absolute()))

        return all_available

    def __repr__(self):
        return "{}: {j[subject_id]}/{j[data_type]}/{j[modality]}".format(self.__class__.__name__,
                                                                         j=self.record)


class BIDS(object):
    METADATA_FNAMES = ["dataset_description.json",
                       "participants.json",
                       "participants.tsv"]
    NIFTI_EXTENSION = '.nii'

    def __init__(self, root_path):
        self.root_path = Path(root_path).absolute()
        self.description = DatasetDescription(self.root_path)
        self.participants = Participants(self.root_path)
        self.__load_data()

    def __load_data(self):
        all_records = []
        for i in self.root_path.rglob('*.*'):
            if i.name.lower() in self.METADATA_FNAMES:
                continue
            if ".git" in str(i.absolute()):
                continue


            # Check if its a nifti file
            if self.NIFTI_EXTENSION in i.suffixes:
                relative_parts = i.relative_to(self.root_path).parts

                # Skip derivatives
                if relative_parts[0] == 'derivatives':
                    continue

                # Get rid of all suffixes
                fstem = i.stem.split('.')[0]
                subject_id, data_type, _ = relative_parts
                modality = fstem.split("_", maxsplit=1)[1]

                drow = {
                    "subject_id": subject_id,
                    "modality": modality,
                    "data_type": data_type,
                    "absolute_path": str(i.absolute()),
                    "dataset_root": str(self.root_path),
                }

                all_records.append(drow)

        self.df = pd.DataFrame.from_records(all_records)

    def as_dataframe(self):
        return self.df.copy()

    def query(self, query):
        results = self.df.query(query)
        return [Subject(row) for _, row in results.iterrows()]

    def get_subjects(self):
        return [Subject(row) for _, row in self.df.iterrows()]

    def __repr__(self):
        return repr(self.description)

    def has_derivatives(self):
        derivatives = self.root_path / "derivatives"
        if derivatives.exists() and derivatives.is_dir():
            return True
        return False
