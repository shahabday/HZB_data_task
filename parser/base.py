import json
from abc import ABC, abstractmethod
from parser.utils import smart_open  




class GammryParser(ABC):
    def __init__(self, filepath , extra_metadata=None):
        self.filepath = filepath
        self.metadata = {}
        self.data = []
        self.extra_metadata = extra_metadata or {}

    def parse(self):
        lines = self._read_file()
        self._extract_common_metadata(lines)
        self._extract_specific_metadata(lines)
        self._extract_data(lines)


    def _read_file(self):
        return [line.strip() for line in smart_open(self.filepath)]

    """ This raises unicode error :
    def _read_file(self):
        with open(self.filepath, 'r') as f:
            return [line.strip() for line in f.readlines()]
    """

    def _extract_common_metadata(self, lines):
        common_tags = ["TAG", "TITLE", "DATE", "TIME", "NOTES"]
        for line in lines:
            parts = line.split('\t')
            if parts and parts[0] in common_tags:
                self.metadata[parts[0]] = parts[2] if len(parts) > 2 else parts[1]

    @abstractmethod
    def _extract_specific_metadata(self, lines):
        pass

    @abstractmethod
    def _extract_data(self, lines):
        pass

    def export_json(self, output_path):
        with open(output_path, 'w') as f:
            json.dump({
                "instrument_type": "Gamry",
                "experiment_class": self.__class__.__name__.replace("Parser", ""), #This will replase specific parser class name 
                "metadata" : self.metadata,
                "doe_version": self.extra_metadata.get("doe_version"),
                "battery_id": self.extra_metadata.get("battery_id"),
                "doe_section": self.extra_metadata.get("doe_section"),
                "data": self.data


            }, f, indent=2)


    def export_json_old(self, output_path):
        with open(output_path, 'w') as f:
            json.dump({
                "metadata": self.metadata,
                "data": self.data
            }, f, indent=2)
