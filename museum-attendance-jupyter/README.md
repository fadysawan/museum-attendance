# Museum Attendance Jupyter Analysis

Jupyter notebook environment for interactive analysis and visualization of museum attendance data.

## Features

- Interactive data exploration with Jupyter Lab
- Linear regression model training and evaluation
- Comprehensive visualizations:
  - Scatter plots with regression lines
  - Residual analysis
  - Prediction vs actual comparisons
  - Feature importance charts
- Model performance metrics (R², MSE, RMSE, MAE)

## Usage

### With Docker Compose

```bash
# Start all services including Jupyter
docker-compose up

# Access Jupyter Lab at:
http://localhost:8888

# Open and run: notebooks/regression_analysis.ipynb
```

### Local Development

```bash
# Install dependencies
pip install -e .

# Start Jupyter Lab
jupyter lab
```

## Notebooks

- `regression_analysis.ipynb`: Complete regression analysis workflow
  - Data loading from PostgreSQL
  - Data cleaning and preparation
  - Model training and evaluation
  - Interactive visualizations
  - Insights and conclusions

## Project Structure

```
museum-attendance-jupyter/
├── Dockerfile
├── pyproject.toml
├── notebooks/
│   └── regression_analysis.ipynb
└── src/
    └── visualization/
        ├── __init__.py
        └── regression_visualizer.py
```

## Dependencies

- JupyterLab 4.0+
- Matplotlib & Seaborn (visualizations)
- Scikit-learn (regression models)
- museum-attendance-common (database access)
- museum-attendance-data-estimator (model utilities)
