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
 
    response = smart.Workspaces.get_workspace(workspace_id)
    assert isinstance(response, smartsheet.models.workspace.Workspace)

    workspace = response.name, response.id, response.permalink, response.access_level

    for child in response.folders:
        folders.append(child)
    for child in response.sheets:
        sheets.append(child)
    for child in response.reports or []:
        reports.append(child)
    for child in response.sights or []:
        sights.append(child)
    for child in response.templates or []:
        templates.append(child)
    
    print(f"workspace: {workspace}")
    print(f"folders: {folders}")
    print(f"sheets: {sheets}")
    print(f"reports: {reports}")
    print(f"sights: {sights}")
    print(f"templates: {templates}")
if __name__ == "__main__":
    main()
