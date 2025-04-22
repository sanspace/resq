import logging
from pathlib import Path
from typing import Any

import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
)
CONTENTS_DIR = Path("contents")


def load_resume_data(contents_path: Path = CONTENTS_DIR) -> dict[str, Any] | None:
    resume_data: dict[str, Any] | None = {}

    if not contents_path.is_dir():
        logging.error(f"Contents directory not found: {contents_path}")
        return None

    yaml_files_found = False
    for file_path in contents_path.glob("*.y*ml"):
        section_name = file_path.stem
        yaml_files_found = True

        try:
            with open(file_path, "r") as file:
                file_data = yaml.safe_load(file)
                if file_data:
                    resume_data[section_name] = file_data
                else:
                    logging.warning(f"Empty YAML file: {file_path.name}")
        except yaml.YAMLError as e:
            mark = getattr(e, "problem_mark", None)
            if mark:
                logging.error(
                    f"Error parsing YAML file: {file_path.name} at"
                    f" line {mark.line + 1}, column {mark.column + 1}: {e.problem}"
                )
            else:
                logging.error(f"Error parsing YAML file: {file_path.name} - {e}")
        except IOError as e:
            logging.error(
                f"Error reading YAML file: {file_path.name} - {e}", exc_info=True
            )
        except Exception as e:
            logging.error(
                f"An unexpected error processing file: {file_path.name} - {e}",
                exc_info=True,
            )

    if not yaml_files_found:
        logging.warning("No YAML files found in the contents directory.")
        return None

    return resume_data


if __name__ == "__main__":
    print(f"Attempting to load resume data from {CONTENTS_DIR.resolve()}")
    resume_data = load_resume_data()
    if resume_data:
        print("\n---Successfully loaded resume data---")
        print(resume_data)
        print("\n---Secions Loaded---")
        for section in resume_data.keys():
            print(f" - {section}")
    else:
        print("\n---Failed to load resume data---")
    print("\nTesting Complete.")
