"""
Tool for executing custom Python code for advanced analytics.

This tool provides a powerful capability to run arbitrary Python code against a
loaded dataset in a secure, isolated subprocess. It is designed for advanced
users or AI agents who need to perform analyses that are not covered by the
other available tools.
"""

import asyncio
import json
import textwrap
from ..models.schemas import DatasetManager


async def execute_custom_analytics_code(dataset_name: str, python_code: str) -> str:
    """
    Executes custom Python code against a loaded dataset in an isolated environment.

    This tool allows for flexible and powerful data analysis by running user-provided
    Python code. The dataset is available as a pandas DataFrame named `df`. The
    environment has `pandas`, `numpy`, and `plotly` pre-installed.

    IMPORTANT FOR AGENTS:
    - The dataset is available in your code as a pandas DataFrame named `df`.
    - Libraries pre-imported for you: `pandas as pd`, `numpy as np`, `plotly.express as px`.
    - You MUST `print()` any results you want to see. Only stdout is captured and returned.
    - The code runs in an isolated subprocess with a 30-second timeout.
    - Any errors during execution are caught and returned as part of the output string.

    Args:
        dataset_name (str): The name of the loaded dataset to be made available as `df`.
        python_code (str): A string containing the Python code to execute.

    Returns:
        str: The combined stdout and stderr from the code execution. This includes
             any printed output or error messages.
    """
    try:
        df = DatasetManager.get_dataset(dataset_name)
        
        # Serialize DataFrame to JSON to pass to the subprocess
        # Using a compact format to handle larger datasets
        dataset_json = df.to_json(orient='split')
        
        # Indent user code to fit within the execution template
        indented_user_code = textwrap.indent(python_code, '    ')
        
        # Create the full script to be executed by the subprocess
        execution_code = f'''
import pandas as pd
import numpy as np
import plotly.express as px
import json
import sys

try:
    # Load dataset from JSON string
    df = pd.read_json({json.dumps(dataset_json)}, orient='split')
    
    # Execute user-provided code
{indented_user_code}

except Exception as e:
    print(f"ERROR: {{type(e).__name__}}: {{str(e)}}", file=sys.stderr)
    import traceback
    print("Traceback:", file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
'''
        
        # Execute the script in a subprocess with necessary dependencies
        process = await asyncio.create_subprocess_exec(
            'uv', 'run', '--with', 'pandas', '--with', 'numpy', '--with', 'plotly',
            'python', '-c', execution_code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for the process to complete, with a timeout
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=30.0)
            output = stdout.decode('utf-8', errors='ignore')
            error_output = stderr.decode('utf-8', errors='ignore')
            return output + error_output
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            return "TIMEOUT ERROR: Code execution exceeded the 30-second limit."
            
    except Exception as e:
        return f"EXECUTION SETUP ERROR: {type(e).__name__}: {str(e)}"