# E-Commerce Data Analytics Project

This project was built for the Dicoding Bangkit Academy Data Analytics course. It analyzes an E-Commerce dataset to uncover insights regarding customer satisfaction based on product data completeness and delivery time.

**Live Dashboard:** [https://xyvern-proyekanalisadatadicoding-dashboardstreamlit-ogee8d.streamlit.app/](https://xyvern-proyekanalisadatadicoding-dashboardstreamlit-ogee8d.streamlit.app/)
## Project Structure
- `data/`: Contains raw datasets (`orders_dataset.csv`, `order_items_dataset.csv`, etc.).
- `scripts/`: Contains a script (`preprocess_data.py`) to process the raw datasets into an optimized, lightweight CSV for the dashboard.
- `dashboard/`: Contains the Streamlit app code (`streamlit.py`) and the processed lightweight data (`main_data.csv`).
- `notebook.ipynb`: Original Jupyter Notebook detailing the data wrangling and exploratory data analysis.

## Setup Environment

### Using Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Using Shell/Terminal
```bash
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
pip install -r requirements.txt
```

## Running the Application

### 1. Data Preprocessing (Optional)
If you need to regenerate the `main_data.csv` used by the dashboard from the raw data:
```bash
python scripts/preprocess_data.py
```

### 2. Run the Streamlit Dashboard
```bash
streamlit run dashboard/streamlit.py
```