from parser.eis_parser import EISParser
from parser.utils import detect_experiment_type

filepath = "data/Test_Data.DTA"
experiment_type = detect_experiment_type(filepath)

# Example values. !!! customize based on DOE protocol !!!
extra_metadata = {
    "doe_version": "v1.0",
    "battery_id": "Battery_12345",
    "doe_section": 2
}

if experiment_type == "PWR800_HYBRIDEIS":
    parser = EISParser(filepath, extra_metadata=extra_metadata)
    parser.parse()
    parser.export_json("output/output4.json")
else:
    print("Unsupported experiment type:", experiment_type)
