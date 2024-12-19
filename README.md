# **hm_master_thesis** 📊

This repository contains scripts, datasets, and visualizations created as part of the **Player Analysis Project** for the master thesis. The project involves web scraping, data cleaning, exploratory data analysis (EDA), and interactive dashboard development to derive insights from player statistics and market values.

---

## **Repository Structure**

```plaintext
hm_master_thesis/
│
├── Cleaning/                     # Data preparation and cleaning scripts
│   └── data_preparation.ipynb    # Jupyter Notebook for cleaning and processing raw data
│
├── Dashboards/                   # Interactive dashboards for visualization
│   ├── Streamlit/                # Streamlit-based interactive dashboard
│   │   └── streamlit_app.py                # Streamlit application for visualizing player statistics
│   │
│   ├── Power BI/                 # Power BI Dashboard for detailed visualizations
│       └── dashboard.pbix        # Power BI file for analysis
│
├── Data/                         # Contains all datasets
│   ├── raw/                      # Raw data collected for analysis
│   │
│   ├── cleaned/                  # Cleaned and preprocessed datasets
│
├── EDA/                          # Exploratory Data Analysis
│   └── EDA.ipynb                 # Jupyter Notebook for EDA with visualizations and insights
│
├── Scraping/                     # Data scraping scripts
│   └── players.ipynb             # Jupyter Notebook for scraping player data
│
└── README.md                     # Project overview and documentation
```

---

## **Project Overview**

The **Player Analysis Project** focuses on:

1. **Data Collection**: Extracting player data and market values from relevant sources.
2. **Data Cleaning**: Preprocessing raw data to ensure consistency, accuracy, and usability.
3. **Exploratory Data Analysis (EDA)**: Identifying trends, correlations, and insights using visualization tools.
4. **Interactive Dashboards**: Developing real-time dashboards for player performance analysis.

---

## **Folder Descriptions**

### 🧹 Cleaning
- **data_preparation.ipynb**: Processes and standardizes the raw datasets to prepare clean, ready-to-use data.

### 📊 Dashboards
- **Streamlit**: A Python-based interactive dashboard (`streamlit_app.py`) for visual exploration.
- **Power BI**: A `.pbix` file containing visualizations like age distributions, performance metrics, and market value trends.

### 📂 Data
- **Raw Data**: Original unprocessed datasets collected during scraping.
- **Cleaned Data**: Processed data for analysis and dashboards.

### 🔍 EDA
- **EDA.ipynb**: Contains visualizations such as:
    - Age distributions
    - Market value trends
    - Goals scored vs games played
    - Correlation heatmaps
    - Average goals per age group

### 🕸️ Scraping
- **players.ipynb**: Automates data extraction for player and market values from online sources.

---

## **Key Visualizations**

The **EDA** notebook generates the following insights:

1. **Age Distribution**: Histogram of player ages across seasons.
2. **Market Value Trends**: Market value progression for selected players.
3. **Goals vs. Games Played**: Scatter plots highlighting performance.
4. **Heatmaps**: Correlation between numerical variables like goals, minutes played, and age.
5. **Average Goals per Age Group**: Bar charts showing average goals scored at different ages.

---

## **Setup Instructions**

### **Prerequisites**
Ensure you have the following tools installed:
- Python 3.9+
- Jupyter Notebook or Jupyter Lab
- Streamlit (for interactive dashboards)
- Power BI Desktop (for .pbix files)

### **Dependencies**
Install required libraries using pip:

```bash
pip install pandas matplotlib seaborn plotly scikit-learn streamlit
```

---

## **How to Run**

### **Data Scraping**
Run the `players.ipynb` notebook in the **Scraping** folder to collect raw player data:

```bash
jupyter notebook Scraping/players.ipynb
```

### **Data Cleaning**
Clean the scraped data using the `data_preparation.ipynb` notebook:

```bash
jupyter notebook Cleaning/data_preparation.ipynb
```

### **Exploratory Data Analysis**
Analyze trends and create visualizations with the `EDA.ipynb` notebook:

```bash
jupyter notebook EDA/EDA.ipynb
```

### **Interactive Dashboard**
Launch the Streamlit dashboard for real-time analysis:

```bash
streamlit run Dashboards/Streamlit/streamlit_app.py
```

### **Power BI Dashboard**
Open the `Dashboard Poewr BI.pbix` file in Power BI Desktop for interactive exploration.

---

## **Contribution Guidelines**
Contributions are welcome! If you want to improve this project:

1. Fork this repository.
2. Create a new branch: `feature/your-feature-name`.
3. Commit your changes.
4. Open a pull request.

---

## **Contact**
For questions or feedback, feel free to reach out.

---

Happy Analyzing! 🚀
