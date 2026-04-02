import argparse
import os

import smartsheet
from smartsheet.models import Folder

class TreeNode:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.children = []  # List to store child nodes

    def add_node(self, child):
        self.children.append(child)
        
    def print_hierarchy(self, level=0):
        indent = "  " * level
        print(f"{indent}- {self.name} (ID: {self.id})")
        
        # Recursively call this method for every child child
        for child in self.children:
            child.print_hierarchy(level + 1)

def expand_tree(smart: smartsheet.Smartsheet, folder_node: TreeNode):
    # Recursively get each folder's child folders
    last_key = None

    def traverse_folder(node: TreeNode) -> None:
        # Page through results based on the token called last_key. None value gets the first page.
        last_key = None
        while True:
            # Call Folders.get_folder_children(...) to get the folder's immediate child folders
            response = smart.Folders.get_folder_children(
                node.id, children_resource_types=["folders"], last_key=last_key
            )
            assert isinstance(response, smartsheet.models.paginated_children_result.PaginatedChildrenResult)
            
            for child in response.data:
                if type(child) is Folder:
                    new_node = TreeNode(child.name, child.id)
                    folder_node.add_node(new_node)
                    traverse_folder(new_node)
            
            last_key = getattr(response, "last_key", None)
            if not last_key:
                break
        
    traverse_folder(folder_node)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_id", type=int, help="Smartsheet workspace ID")
    args = parser.parse_args()

    token = os.getenv("SMARTSHEET_API_TOKEN")
    if not token:
        raise RuntimeError("Missing required environment variable: SMARTSHEET_API_TOKEN")

    workspace_id = args.workspace_id

    smart = smartsheet.Smartsheet(token)

    # Build a tree to store the workspace folder hierarchy
    workspace_tree = TreeNode("Workspace", workspace_id)
    
    # Page through results based on the token called last_key. None value gets the first page.
    last_key = None
    while True:
        # Call Workspaces.get_workspace_children(...) to get the workspace's immediate child folders
        response = smart.Workspaces.get_workspace_children(
            workspace_id, children_resource_types=["folders"], last_key=last_key
        )
        assert isinstance(response, smartsheet.models.paginated_children_result.PaginatedChildrenResult)

        for child in response.data:
            if type(child) is Folder:
                new_node = TreeNode(child.name, child.id)
                workspace_tree.add_node(new_node)
                expand_tree(smart, new_node)

        last_key = getattr(response, "last_key", None)
        if not last_key:
            break

    workspace_tree.print_hierarchy()

if __name__ == "__main__":
    main()
