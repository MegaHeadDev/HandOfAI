import os
import shutil
from typing import List, Dict, Union, Optional
from pathlib import Path

class FileOperations:
    """
    A class that handles basic file operations across different platforms.
    Supports operations like create, move, copy, delete files and folders.
    """
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize FileOperations with optional base path.
        
        Args:
            base_path (str, optional): Base directory for all operations. 
                                     Defaults to current working directory.
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        
    def create_folder(self, folder_name: str) -> Dict[str, Union[bool, str]]:
        """
        Create a new folder at specified path.
        
        Args:
            folder_name (str): Name of the folder to create
            
        Returns:
            dict: Operation result with status and message
        """
        try:
            folder_path = self.base_path / folder_name
            os.makedirs(folder_path, exist_ok=True)
            return {
                "success": True,
                "message": f"Folder '{folder_name}' created successfully",
                "path": str(folder_path)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create folder: {str(e)}"
            }

    def move_files(self, files: List[str], destination: str) -> Dict[str, Union[bool, str]]:
        """
        Move files to destination folder.
        
        Args:
            files (List[str]): List of file paths to move
            destination (str): Destination folder path
            
        Returns:
            dict: Operation result with status and message
        """
        try:
            dest_path = self.base_path / destination
            if not dest_path.exists():
                os.makedirs(dest_path)
                
            moved_files = []
            for file in files:
                file_path = self.base_path / file
                if file_path.exists():
                    shutil.move(str(file_path), str(dest_path / file_path.name))
                    moved_files.append(file)
                    
            return {
                "success": True,
                "message": f"Successfully moved {len(moved_files)} files",
                "moved_files": moved_files
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to move files: {str(e)}"
            }

    def list_files(self, 
                   extension: Optional[str] = None,
                   recursive: bool = False) -> Dict[str, Union[bool, List[str], str]]:
        """
        List files in the base directory with optional extension filter.
        
        Args:
            extension (str, optional): File extension to filter (e.g., '.txt')
            recursive (bool): Whether to search recursively in subdirectories
            
        Returns:
            dict: Operation result with status and list of files
        """
        try:
            files = []
            if recursive:
                for root, _, filenames in os.walk(self.base_path):
                    for filename in filenames:
                        if extension and filename.endswith(extension):
                            files.append(str(Path(root) / filename))
                        elif not extension:
                            files.append(str(Path(root) / filename))
            else:
                for item in self.base_path.iterdir():
                    if item.is_file():
                        if extension and item.name.endswith(extension):
                            files.append(str(item))
                        elif not extension:
                            files.append(str(item))
                            
            return {
                "success": True,
                "files": files,
                "message": f"Found {len(files)} files"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to list files: {str(e)}"
            }
        

    def copy_files(self, files: List[str], destination: str) -> Dict[str, Union[bool, str]]:
        """
        Copy files to destination folder.
        
        Args:
            files (List[str]): List of file paths to copy
            destination (str): Destination folder path
            
        Returns:
            dict: Operation result with status and message
        """
        try:
            dest_path = self.base_path / destination
            if not dest_path.exists():
                os.makedirs(dest_path)
                
            copied_files = []
            for file in files:
                file_path = self.base_path / file
                if file_path.exists():
                    shutil.copy2(str(file_path), str(dest_path / file_path.name))
                    copied_files.append(file)
                    
            return {
                "success": True,
                "message": f"Successfully copied {len(copied_files)} files",
                "copied_files": copied_files
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to copy files: {str(e)}"
            }

if __name__ == "__main__":
    """
    Test main function to demonstrate FileOperations functionality
    """
    # Initialize FileOperations with test directory
    test_dir = "test_files"
    file_ops = FileOperations(test_dir)
    
    # Test create_folder
    print("\n1. Testing create_folder:")
    result = file_ops.create_folder("test_folder")
    print(result)
    
    # Create some test files
    test_folder = Path(test_dir)
    test_folder.mkdir(exist_ok=True)
    
    # Create test text files
    for i in range(3):
        with open(test_folder / f"test{i}.txt", "w") as f:
            f.write(f"Test content {i}")
            
    # Test list_files
    print("\n2. Testing list_files:")
    result = file_ops.list_files(extension=".txt")
    print(result)
    
    # Test copy_files
    print("\n3. Testing copy_files:")
    result = file_ops.copy_files(
        [f"test{i}.txt" for i in range(3)],
        "backup"
    )
    print(result)
    
    # Test move_files
    print("\n4. Testing move_files:")
    result = file_ops.move_files(
        [f"test{i}.txt" for i in range(3)],
        "moved"
    )
    print(result)
    
    print("\n5. Final directory structure:")
    # Show final directory structure
    def print_tree(directory, prefix=""):
        """Helper function to print directory structure"""
        path = Path(directory)
        print(f"{prefix}└── {path.name}/")
        prefix += "    "
        for item in path.iterdir():
            if item.is_file():
                print(f"{prefix}└── {item.name}")
            elif item.is_dir():
                print_tree(item, prefix)
                
    print_tree(test_dir)