# Generic Data Analytics MCP Server

This repository provides a powerful and flexible Model Context Protocol (MCP) server designed for generic data analysis. It can ingest any structured dataset (JSON or CSV) and transform it into an intelligent, AI-guided analytics workflow. The server is built with a modular architecture and a dataset-agnostic design, meaning it automatically adapts to your data without requiring hardcoded schemas.

This project serves as a comprehensive example of how to build a robust MCP server, demonstrating best practices in organizing tools, resources, and prompts.

<img src="./images/mcp-server-prompts.png" alt="MCP Server Prompts" style="max-width: 800px;">

## ✨ Features

- **Universal Data Compatibility**: Works with any JSON/CSV dataset out of the box.
- **Automatic Schema Discovery**: Intelligently infers column types (numerical, categorical, temporal, identifier) without manual configuration.
- **Rich Analytics Toolkit**: Comes with a comprehensive suite of tools for data cleaning, analysis, and visualization.
- **AI-Guided Workflows**: Utilizes adaptive prompts to guide users through complex analysis tasks.
- **Modular Architecture**: Clean separation of concerns between tools, resources, prompts, and data models makes the server easy to extend and maintain.
- **Tool-Only Client Support**: Includes resource mirror tools to ensure compatibility with all MCP clients.
- **Memory-Aware**: Provides tools for monitoring and optimizing memory usage.

## 🚀 Getting Started

Follow these steps to get the server up and running in minutes.

### 1. Navigate to the Project Directory
```bash
cd quick-data-mcp/
```

### 2. Configure for Your MCP Client
You need to create a `.mcp.json` file to tell your MCP client how to run the server. A sample is provided.

```bash
# Copy the sample configuration
cp .mcp.json.sample .mcp.json
```

Next, you need to **edit `.mcp.json`** and replace the placeholder paths with the absolute paths on your system.

- `"command"`: Update this with the path to your `uv` executable. You can find this by running `which uv`.
- `"--directory"`: Update this with the absolute path to the `quick-data-mcp` directory. You can find this by running `pwd` from within the directory.

Here is an example of a configured `.mcp.json`:
```json
{
  "mcpServers": {
    "quick-data": {
      "command": "/Users/your_username/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/your_username/projects/quick-data-mcp",
        "run",
        "python",
        "main.py"
      ],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### 3. Run the Server
Once your configuration is set, you can start the server with your MCP client or test it directly from the command line:

```bash
# This command will start the server on http://0.0.0.0:8000
uv run python main.py
```

## 🤖 How to Use

Once the server is running, the best way to start is by asking for a list of all its capabilities.

In your MCP client (like Claude Code), run the following prompt:
```
/quick-data:list_mcp_assets_prompt
```
This will return a complete, formatted list of all available prompts, tools, and resources, giving you a full menu of what you can do next.

### Example Workflow

1.  **Find your data**:
    ```
    /quick-data:find_datasources_prompt
    ```
2.  **Load a dataset**:
    ```
    /quick-data:load_dataset file_path:'data/ecommerce_orders.json' dataset_name:'sales'
    ```
3.  **Get a first look**:
    ```
    /quick-data:dataset_first_look_prompt dataset_name:'sales'
    ```
4.  **Run a suggested analysis**:
    ```
    /quick-data:find_correlations dataset_name:'sales'
    ```
5.  **Visualize the results**:
    ```
    /quick-data:create_chart dataset_name:'sales' chart_type:'scatter' x_column:'order_value' y_column:'customer_age'
    ```

## 🛠️ Capabilities

The server comes with a rich set of prompts, tools, and resources.

### 📝 Prompts
Guided workflows to help you with common analysis tasks.

- **/dataset_first_look**: Get a quick overview and suggested starting points for a dataset.
- **/segmentation_workshop**: Plan a strategy for segmenting your data.
- **/data_quality_assessment**: Start a systematic review of your data's quality.
- **/correlation_investigation**: Get a guided workflow for finding relationships in your data.
- **/insight_generation_workshop**: A guided session to turn data findings into business insights.
- **/dashboard_design_consultation**: Plan a dashboard tailored to a specific audience.
- **/find_datasources**: Discover available `.csv` and `.json` files in your project directory.
- **/list_mcp_assets**: See a complete list of all server capabilities.

### 🔧 Tools
Functions for performing specific actions like data manipulation, analysis, and visualization.

#### Data Management
- **/load_dataset**: Loads a dataset from a JSON or CSV file into memory.
- **/list_loaded_datasets**: Shows a summary of all datasets currently loaded.
- **/clear_dataset**: Removes a specific dataset from memory.
- **/clear_all_datasets**: Removes all datasets from memory.

#### Core Analytics
- **/suggest_analysis**: Suggests relevant analysis tools based on the dataset's schema.
- **/analyze_distributions**: Analyzes the statistical distribution of a single column.
- **/find_correlations**: Finds correlations between numerical columns.
- **/segment_by_column**: Segments the data by a categorical column and calculates statistics.
- **/detect_outliers**: Detects outliers in numerical columns using IQR or Z-score methods.
- **/time_series_analysis**: Performs a basic time series analysis.
- **/validate_data_quality**: Performs a comprehensive data quality assessment.

#### Advanced Operations & I/O
- **/compare_datasets**: Performs a side-by-side comparison of two datasets.
- **/merge_datasets**: Merges multiple datasets on a common column.
- **/calculate_feature_importance**: Calculates feature importance based on correlation.
- **/memory_optimization_report**: Analyzes memory usage and suggests optimizations.
- **/execute_custom_analytics_code**: Executes custom Python code in an isolated environment.
- **/create_chart**: Creates a chart (histogram, bar, scatter, etc.) and saves it as HTML.
- **/generate_dashboard**: Generates a set of charts for a dashboard.
- **/export_insights**: Exports a summary of dataset insights to a file (JSON, CSV, HTML).

### 📊 Resources
Read-only endpoints that provide real-time information about the server and data.

- `datasets://loaded`: A list of all currently loaded datasets.
- `datasets://{dataset_name}/schema`: The dynamically discovered schema of a dataset.
- `datasets://{dataset_name}/summary`: A statistical summary of a dataset's numerical columns.
- `datasets://{dataset_name}/sample`: A small sample of rows for data preview.
- `analytics://current_dataset`: The name of the most recently loaded dataset.
- `analytics://available_analyses`: A list of analysis types applicable to the current dataset.
- `analytics://column_types`: The inferred role for each column in a dataset.
- `analytics://suggested_insights`: A list of suggested next analysis steps.
- `analytics://memory_usage`: The total memory usage of all loaded datasets.
- `config://server`: The server's configuration and capabilities.
- `system://status`: The current status and health of the server.

## 🏗️ Architecture

The project is organized into a clean, modular structure to promote maintainability and extensibility.

```
quick-data-mcp/
├── .mcp.json.sample      # Sample MCP client configuration
├── data/                   # Sample datasets for demonstration
├── src/mcp_server/         # Core server source code
│   ├── config/             # Server configuration settings
│   ├── models/             # Pydantic data models and schemas
│   ├── prompts/            # Implementations for guided prompts
│   ├── resources/          # Implementations for data resources
│   ├── tools/              # Implementations for analytics tools
│   └── server.py           # Main server definition and asset registration
├── tests/                  # Pytest test suite
└── main.py                 # Server entry point
```

## 🧪 Testing

The repository includes a comprehensive test suite. To run the tests, navigate to the `quick-data-mcp` directory and run:

```bash
uv run python -m pytest
```

This will execute all tests and provide a coverage report.