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

    workspace = None
    folders = []
    sheets = []
    reports = []
    sights = []
    templates = []

    response = smart.Workspaces.get_workspace_metadata(workspace_id)
    assert isinstance(response, smartsheet.models.workspace.Workspace)

    workspace = response.name, response.id, response.permalink, response.access_level, response.created_at, response.modified_at

    last_key = None
    while True:
        response = smart.Workspaces.get_workspace_children(
            workspace_id, last_key=last_key
        )
        assert isinstance(
            response,
            smartsheet.models.paginated_children_result.PaginatedChildrenResult
        )

        for child in response.data:
            if type(child) is Folder:
                folders.append(child)
            elif type(child) is Sheet:
                sheets.append(child)
            elif type(child) is Report:
                reports.append(child)
            elif type(child) is Sight:
                sights.append(child)
            elif type(child) is Template:
                templates.append(child)

        last_key = getattr(response, "last_key", None)
        if not last_key:
            break

    print(f"workspace: {workspace}")
    print(f"folders: {folders}")
    print(f"sheets: {sheets}")
    print(f"reports: {reports}")
    print(f"sights: {sights}")
    print(f"templates: {templates}")

if __name__ == "__main__":
    main()
