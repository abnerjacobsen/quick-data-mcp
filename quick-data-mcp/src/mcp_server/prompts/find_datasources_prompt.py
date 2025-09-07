"""
Prompt-generating function for discovering local data source files.

This module provides a function that scans the local filesystem for potential
data files (CSV, JSON) and generates a prompt that lists them with ready-to-use
commands to load them.
"""

from pathlib import Path
from typing import Optional


def format_file_size(size_bytes: int) -> str:
    """
    Converts a file size in bytes to a human-readable string (KB, MB, GB).

    Args:
        size_bytes (int): The file size in bytes.

    Returns:
        str: A human-readable string representation of the file size.
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    for unit in ['KB', 'MB', 'GB']:
        size_bytes /= 1024.0
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
    return f"{size_bytes:.1f} TB"


async def find_datasources(directory_path: Optional[str] = None) -> str:
    """
    Discovers available data files and presents them as load options.

    This function scans the specified directory (or the current directory if
    none is provided) and common subdirectories like 'data/' for .csv and .json
    files. It then generates a markdown-formatted prompt listing the found
    files with their sizes and example `/load_dataset` commands.

    Args:
        directory_path (Optional[str]): The path to the directory to scan.
                                        Defaults to the current directory.

    Returns:
        str: A markdown-formatted string containing the list of discovered
             data sources and instructions.
    """
    try:
        base_path = Path(directory_path or ".").resolve()

        found_files = []
        # Scan base directory
        found_files.extend(base_path.glob('*.csv'))
        found_files.extend(base_path.glob('*.json'))
        # Scan common data subdirectories
        for subdir in ['data', 'datasets']:
            found_files.extend((base_path / subdir).glob('*.csv'))
            found_files.extend((base_path / subdir).glob('*.json'))

        if not found_files:
            return (f"### No Data Sources Found\n\n"
                    f"I searched for `.csv` and `.json` files in `{base_path}` "
                    f"but didn't find any. \n\n**Suggestion:** "
                    f"Try running this from your project's root directory or specify a path.")

        prompt = f"### Data Sources Found in `{base_path.name}`\n\n"
        prompt += "Here are the data files I found. You can load any of them using the provided commands:\n\n"

        for file_path in sorted(list(set(found_files))):
            try:
                relative_path = file_path.relative_to(base_path)
                dataset_name = file_path.stem.lower().replace('-', '_')
                size_str = format_file_size(file_path.stat().st_size)

                prompt += f"- **`{relative_path}`** ({size_str})\n"
                prompt += f"  - `/load_dataset file_path:'{relative_path}' dataset_name:'{dataset_name}'`\n"
            except (IOError, ValueError):
                # Skip files that can't be accessed or have no relative path
                continue
        
        return prompt
        
    except Exception as e:
        return f"**Error**: An unexpected error occurred while searching for data sources: {e}"