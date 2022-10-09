import json
import pathlib
import os
import arrow
from deliverables import CMS125v11Runner, CMS147v11Runner, CMS165v11Runner

# NOTE: Swap this with below for running on full graded dataset
TEST_SUBSET_DIR = f"{pathlib.Path(__file__).parent.parent.absolute()}/test_subset"
DATA_DIR = f"{TEST_SUBSET_DIR}/data"
OUTPUT_DIR = f"{TEST_SUBSET_DIR}/output"


# DATA_DIR = f"{pathlib.Path(__file__).parent.parent.absolute()}/data"
# OUTPUT_DIR = f"{pathlib.Path(__file__).parent.absolute()}/output"

MEASUREMENT_PERIOD_START_DATETIME = arrow.get(
    "2018-01-01"
).datetime  # 2018-01-01 00:00:00+00:00
MEASUREMENT_PERIOD_END_DATETIME = arrow.get(
    "2022-01-01"
).datetime  # 2022-01-01 00:00:00+00:00


def load_ndjson_file(filepath: str) -> list[dict]:
    with open(filepath, "r") as file:
        return [dict(json.loads(line)) for line in file]

def test():
    solution_path = 'output'
    test = 0
    errors = []
    for runner in ['CMS125v11Runner', 'CMS147v11Runner', 'CMS165v11Runner']:
        for file in os.listdir(os.path.join(solution_path, runner)):
            test+=1
            solution = os.path.join(solution_path, runner, file)
            output = os.path.join('..','test_subset', solution_path, runner, file)
            if(os.path.exists(output)):
                with open(solution) as s, open(output) as o:
                    if (json.load(o) != json.load(s)):
                        errors.append(output)
                        print(output, ': error detected.')
            else:
                errors.add(output)
                print(output, 'is missing.')
    print(test, 'files were tested.')
    if(len(errors)>0):
        print(len(errors), 'errors were found:', errors)
    else:
        print('All tests were passed.')

if __name__ == "__main__":
    # Initiate lists
    patient_list = load_ndjson_file(f"{DATA_DIR}/Patient.ndjson")
    observation_list = load_ndjson_file(f"{DATA_DIR}/Observation.ndjson")
    condition_list = load_ndjson_file(f"{DATA_DIR}/Condition.ndjson")
    encounter_list = load_ndjson_file(f"{DATA_DIR}/Encounter.ndjson")
    immunization_list = load_ndjson_file(f"{DATA_DIR}/Immunization.ndjson")
    procedure_list = load_ndjson_file(f"{DATA_DIR}/Procedure.ndjson")

    # Run each eCQM
    runners = [
        CMS125v11Runner(
            MEASUREMENT_PERIOD_START_DATETIME,
            MEASUREMENT_PERIOD_END_DATETIME,
            patient_list=patient_list,
            encounter_list=encounter_list,
            procedure_list=procedure_list,
        ),
        CMS147v11Runner(
            MEASUREMENT_PERIOD_START_DATETIME,
            MEASUREMENT_PERIOD_END_DATETIME,
            patient_list=patient_list,
            encounter_list=encounter_list,
            immunization_list=immunization_list,
        ),
        CMS165v11Runner(
            MEASUREMENT_PERIOD_START_DATETIME,
            MEASUREMENT_PERIOD_END_DATETIME,
            patient_list=patient_list,
            condition_list=condition_list,
            observation_list=observation_list,
        ),
    ]
    for runner in runners:
        result_dict = runner.run_all(print_counts=True, save_to_dir=OUTPUT_DIR)
    test()
