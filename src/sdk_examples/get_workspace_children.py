import argparse
import os
from smartsheet.models import Folder, Sheet, Report, Sight, Template

import smartsheet

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_id", type=int, help="Smartsheet workspace ID")
    args = parser.parse_args()

    token = os.getenv("SMARTSHEET_API_TOKEN")
    if not token:
        raise RuntimeError("Missing required environment variable: SMARTSHEET_API_TOKEN")
    workspace_id = args.workspace_id

    smart = smartsheet.Smartsheet(token)

    last_key = None
    while True:
        response = smart.Workspaces.get_workspace_children(
            workspace_id, last_key=last_key
        )
        assert isinstance(response, smartsheet.models.paginated_children_result.PaginatedChildrenResult)

        for child in response.data:
            object_type = None
            if type(child) is Folder:
                object_type = "Folder"
            elif type(child) is Sheet:
                object_type = "Sheet"
            elif type(child) is Report:
                object_type = "Report"
            elif type(child) is Sight:
                object_type = "Sight"
            elif type(child) is Template:
                object_type = "Template"
            else:
                object_type = "Unknown"

            print(f"{object_type}: {child.name}")

        last_key = getattr(response, "last_key", None)
        if not last_key:
            break

if __name__ == "__main__":
    main()
