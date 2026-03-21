import argparse
import os

import smartsheet
from smartsheet.models import Folder, Sheet

def collect_sheet_ids(smart: smartsheet.Smartsheet, folder_id: int) -> list[int]:
    last_key = None
    sheet_ids = []

    def traverse_folder(folder_id: int) -> None:
        last_key = None
        while True:
            response = smart.Folders.get_folder_children(
                folder_id, children_resource_types=["folders","sheets"], last_key=last_key
            )
            assert isinstance(response, smartsheet.models.paginated_children_result.PaginatedChildrenResult)
            
            for child in response.data:
                if isinstance(child, Sheet):
                    sheet_ids.append(child.id)
                elif isinstance(child, Folder):
                    traverse_folder(child.id)
            
            last_key = getattr(response, "last_key", None)
            if not last_key:
                break
        
    traverse_folder(folder_id)
    return sheet_ids

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_id", type=int, help="Smartsheet workspace ID")
    args = parser.parse_args()

    token = os.getenv("SMARTSHEET_API_TOKEN")
    if not token:
        raise RuntimeError("Missing required environment variable: SMARTSHEET_API_TOKEN")

    workspace_id = args.workspace_id

    smart = smartsheet.Smartsheet(token)

    sheet_ids = []
    last_key = None
    while True:
        response = smart.Workspaces.get_workspace_children(
            workspace_id, children_resource_types=["folders","sheets"], last_key=last_key
        )
        
        assert isinstance(response, smartsheet.models.paginated_children_result.PaginatedChildrenResult)

        for child in response.data:
            if isinstance(child, Sheet):
                sheet_ids.append(child.id)
            elif isinstance(child, Folder):
                sheet_ids.extend(collect_sheet_ids(smart, child.id))

        last_key = getattr(response, "last_key", None)
        if not last_key:
            break

    print(sheet_ids)

if __name__ == "__main__":
    main()
