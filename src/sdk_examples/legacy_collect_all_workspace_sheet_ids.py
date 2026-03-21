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
 
    workspace = smart.Workspaces.get_workspace(
        workspace_id, load_all=True
    )
    assert isinstance(workspace, smartsheet.models.workspace.Workspace)

    sheet_ids = []
    for sheet in workspace.sheets:
        sheet_ids.append(sheet.id)

    print(f"Sheet IDs: {sheet_ids}")

if __name__ == "__main__":
    main()
