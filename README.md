# Introduction

The project consists in building an ecosystem that fetches data from Wikipedia to gather the list of most visited museums and to correlate the tourist attendance at their museums with the population of the respective cities.

The data that should be fetched should include the following:
Museum data:
- Museum Name
- Location
- Tourist Attendance

Museum characterstics
- Collection Size
- Number Of Public Transit Access
- Characteristics of the museum
- ... These attributes are dynamically fetched from the museum the museum page

City:
- Name
- Population

After fetching the data, a predictive AI model should be applied to the data(regression) and should try to correlate the city population and the influx of visitors.

# Technical Requirements

The project should be developed in Python and should be deployed and accessible through a Docker container

Docker Compose should be used to provision additional infrastructure

A Jupyter notebook hosted in docker should be created. This Jupyter notebook should import the python packages and call the functions from them without duplicating the code. It should also create charts for visualization, to show the correlation between the city population and the museum attendance and help in assessing the model's performance.

# Technical Implementation

The following section is a detailed documentation showing the implementation of the solution.

## Analysis

The implementation of this project will consist in the development of 2 python packages:
- The "museum-attendance-data-fetcher"
- The "museum-attendance-common"
- The "museum-attendance-jupyter"

They will use a PostgreSQL database to fetch and store the data. A flyway migration will be used to create the schema of the database in order to maintain a consistent structure. This will take into account the replication of the database in different environments.

A Jupyter notebook will be used to showcase the performance of the regression model applied to the data.

## Architecture

![System Architecture](./docs/system-architecture/system-architecture.png)

Editable diagram file: [DRAWIO Diagram](./docs/system-architecture/system-architecture.drawio)

## Database Schema

![Database Schema](./docs/database-diagram/database-diagram.png)

Editable diagram file: [DRAWIO Diagram](./docs/database-diagram/database-diagram.drawio)

## Functional Components

### common

This python package will be mainly used for the components that are shared between the museum-attendance-data-fetcher and the museum-attendance-jupyter. It will mainly contain the data-layer that will be used to interact with the database through an ORM.

### museum-attendance-data-fetcher

This python module will use the Wikipedia API to fetch the master "List_of_most_visited_museums" page, will parse it in order to fetch the table containing the list of museums, and will extract the data from the pages of museums and cities to insert them into the database.

![Museum Attendance Data Fetcher Activity Diagram](./docs/components/museum-attendance-data-fetcher.drawio.png)

Editable diagram file: [DRAWIO Diagram](./docs/components/museum-attendance-data-fetcher.drawio)

### museum-attendance-jupyter

This python module will fetch data from the database and will crunch the data using pandas and numpy in order to use the data in a predictive AI model -> regression. 

## Technical Aspects

### Code Quality

This project enforces:
- 80% minimum test coverage (pytest-cov)
- Static type checking (mypy)
- Code linting (ruff)
- Code formatting (black)

Run quality checks:
```bash
cd museum-attendance-data-fetcher
mypy src/
ruff check src/
pytest --cov --cov-fail-under=80

## How to run the project

### Prerequisites

- Docker Desktop installed and running
- Docker Compose v2.0 or higher
- Wikipedia API credentials (Client ID and Client Secret)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/fadysawan/museum-attendance.git
   cd museum-attendance
   ```

2. **Create environment file**
   
   Create a `.env` file in the project root with the following content:
   ```env
   # Database Configuration
   POSTGRES_USER=IL_USER
   POSTGRES_PASSWORD=postgres123
   POSTGRES_DB=museum_attendance
   DB_PORT=5432

   # Wikipedia API Credentials (Required)
   WIKIPEDIA_CLIENT_ID=your_client_id_here
   WIKIPEDIA_CLIENT_SECRET=your_client_secret_here

   # Optional Configuration
   LOG_LEVEL=INFO
   KEEP_HTML_FILES=false
   DB_POOL_SIZE=1
   DB_MAX_OVERFLOW=0
   ```

   **Note:** Replace `your_client_id_here` and `your_client_secret_here` with your actual Wikipedia API credentials.

3. **Build and start all services**
   ```bash
   docker-compose up --build
   ```

   This will:
   - Start PostgreSQL database
   - Run Flyway migrations to create the database schema
   - Execute the data-fetcher to collect museum data from Wikipedia
   - Start Jupyter Lab for interactive analysis

### Access the Services

- **Jupyter Notebook**: http://localhost:8888
  - Open `notebooks/museum_regression.ipynb` to view the regression analysis
  - No authentication required (development mode)

- **PostgreSQL Database**: `localhost:5432`
  - Host: `localhost`
  - Port: `5432`
  - Database: `museum_attendance`
  - User: `IL_USER`
  - Password: `postgres123`

### Using the Jupyter Notebook

1. Access Jupyter at http://localhost:8888
2. Open `notebooks/museum_regression.ipynb`
3. Run all cells to:
   - Load museum data from the database
   - Prepare data for regression analysis
   - Train a linear regression model
   - View model metrics and visualization
4. (Optional) Uncomment cell 6 to re-fetch data from Wikipedia

### Manual Data Extraction

To manually run the data fetcher without Docker:

```bash
# Install dependencies
cd museum-attendance-common
pip install -e .

cd ../museum-attendance-data-fetcher
pip install -e .

# Set environment variables
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=IL_USER
export DB_PASSWORD=postgres123
export DB_NAME=museum_attendance
export WIKIPEDIA_CLIENT_ID=your_client_id_here
export WIKIPEDIA_CLIENT_SECRET=your_client_secret_here

# Run the fetcher
python src/museum_attendance_data_fetcher.py
```

### Stopping the Services

```bash
# Stop services (keeps data)
docker-compose stop

# Stop and remove containers (keeps data)
docker-compose down

# Stop, remove containers and delete all data
docker-compose down -v
```


