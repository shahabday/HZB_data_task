from eis_parser import EISParser
from utils import detect_experiment_type

filepath = "data/Test_Data.DTA"
experiment_type = detect_experiment_type(filepath)

if experiment_type == "PWR800_HYBRIDEIS":
    parser = EISParser(filepath)
    parser.parse()
    parser.export_json("output2.json")
else:
    print("Unsupported experiment type:", experiment_type)
