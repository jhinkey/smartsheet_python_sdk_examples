import argparse
import os

import smartsheet

def main() -> None:
    token = os.getenv("SMARTSHEET_API_TOKEN")
    print(f"SMARTSHEET_API_TOKEN set: {bool(token)}")
    if not token:
        raise RuntimeError("Missing required environment variable: SMARTSHEET_API_TOKEN")

    smart = smartsheet.Smartsheet(token)

    last_key = None
    while True:
        page = smart.Workspaces.list_workspaces(
            pagination_type='token',
            max_items=100,
            last_key=last_key
        )
        assert isinstance(page, smartsheet.models.IndexResult)

        print(page.to_dict()) # Do what you want with the page items

        last_key = getattr(page, "last_key", None)
        if not last_key:
            break


if __name__ == "__main__":
    main()
