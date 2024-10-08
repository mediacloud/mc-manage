import argparse
import datetime as dt
import os

from pyairtable import Api
from pyairtable.formulas import match


# A utility to report package updates to a central airtable repository 
def create_release(
    codebase_name: str,
    version_info: str,   
) -> None:
    api = Api(os.environ["AIRTABLE_API_KEY"])
    MEAG_BASE_ID = os.environ["MEAG_BASE_ID"]

    info = "Automatic deployment record"

    # Get codebases id:
    codebase_table = api.table(MEAG_BASE_ID, table_name="Software - Codebases")
    codebase_res = codebase_table.first(formula=match({"Name": codebase_name}))

    # Get the current time in UTC
    iso_timestamp = dt.datetime.utcnow().isoformat()

    resp = codebase_table.batch_upsert(
        [
            {
                "fields": {
                    "Name": codebase_name,
                    "Version": version_info,
                    "Release Time": iso_timestamp,
                    "Info": info,
                }
            }
        ],
        key_fields=["Name"],
    )
    print(resp)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="A utility for updating an airtable package release record"
    )

    parser.add_argument("--name", help="additional deployment name")
    parser.add_argument("--version", help="A descriptive version string")

    args = parser.parse_args()

    create_release(args.name, args.version)