from base import GammryParser


from collections import defaultdict



class EISParser(GammryParser):
    def _extract_specific_metadata(self, lines):
        eis_tags = [
            "CAPACITY", "IDCREQ", "FREQINIT", "FREQFINAL", "PTSPERDEC",
            "VACREQ", "SPEED", "DRIFTCOR", "ZGUESS", "CELLTYPE", "PSTATMODEL"
        ]
        for line in lines:
            parts = line.split('\t')
            if parts and parts[0] in eis_tags:
                self.metadata[parts[0]] = parts[2]

    
    def _extract_data(self, lines):
        start_index = next(i for i, line in enumerate(lines) if line.startswith("ZCURVE"))
        headers = lines[start_index + 1].strip().split('\t')[1:]  # skip indent
        data_lines = lines[start_index + 3:]  # skip two header lines

        data_dict = defaultdict(list)

        for line in data_lines:
            if not line.strip():
                continue
            values = line.strip().split('\t')
            for key, value in zip(headers, values):
                data_dict[key].append(self._safe_convert(value))

        self.data = dict(data_dict)

    def _safe_convert(self, val):
        try:
            return float(val)
        except ValueError:
            return val
