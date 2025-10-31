# Publication Analysis Tool for Codesign and AI Research

This tool helps you analyze publication datasets to identify codesign and AI researcher publications.

## Files Created

1. **`publication_analysis.py`** - Main analysis script with the `PublicationAnalyzer` class
2. **`publication_analysis_example.ipynb`** - Jupyter notebook with step-by-step examples
3. **`sample_publication_data.csv`** - Sample dataset for testing (15 publications)

## Quick Start

### 1. Prepare Your Data

Your publication data should be in CSV or JSON format with these columns:

- **Required:**
  - `title`: Publication title
  - `authors`: Author names (comma-separated string)
  - `year`: Publication year (integer)
  
- **Recommended:**
  - `keywords`: Keywords (comma-separated string)
  - `abstract`: Abstract text
  - `venue`: Conference/journal name

**Example CSV format:**
```csv
title,authors,year,keywords,abstract,venue
"Co-Design of AI Systems","Jane Smith, John Doe",2023,"codesign, AI","...","CHI 2023"
"Machine Learning for Healthcare","Alice Johnson",2022,"ML, healthcare","...","JMIR 2022"
```

### 2. Run the Analysis

#### Option A: Using Python Script

```python
from publication_analysis import PublicationAnalyzer

# Load your data
analyzer = PublicationAnalyzer('your_publications.csv')

# Filter for codesign publications
codesign_pubs = analyzer.filter_codesign_publications()

# Filter for AI publications
ai_pubs = analyzer.filter_ai_publications()

# Find publications that combine both
intersection = analyzer.find_intersection()

# Generate comprehensive report
analyzer.generate_summary_report()

# Visualize trends over time
fig = analyzer.plot_publication_trends()

# Export results
codesign_pubs.to_csv('codesign_results.csv', index=False)
ai_pubs.to_csv('ai_results.csv', index=False)
intersection.to_csv('codesign_ai_results.csv', index=False)
```

#### Option B: Using Jupyter Notebook

1. Open `publication_analysis_example.ipynb` in Jupyter
2. Update `DATA_FILE` variable with your data file path
3. Run all cells to perform the analysis

### 3. Test with Sample Data

```bash
cd /workspace/code
python3 -c "
from publication_analysis import PublicationAnalyzer
analyzer = PublicationAnalyzer('sample_publication_data.csv')
analyzer.filter_codesign_publications()
analyzer.filter_ai_publications()
analyzer.generate_summary_report()
"
```

## Features

### 1. Data Loading
- Supports CSV and JSON formats
- Automatic column detection
- Preview loaded data

### 2. Smart Filtering

**Codesign Terms Detected:**
- codesign, co-design
- collaborative design
- participatory design
- human-centered design
- user-centered design
- design thinking

**AI Terms Detected:**
- artificial intelligence
- machine learning, deep learning
- neural network
- natural language processing (NLP)
- computer vision
- reinforcement learning
- large language model (LLM)
- transformer

### 3. Analysis Capabilities

- **Temporal Trends**: Analyze publication counts over time
- **Top Authors**: Identify most prolific authors in each category
- **Intersection Analysis**: Find publications combining codesign and AI
- **Statistical Summary**: Mean, median, standard deviation of years
- **Visualization**: Publication trend plots

### 4. Export Options

Export filtered results to:
- CSV files for further analysis
- Excel spreadsheets
- JSON for web applications

## Example Output

Running the sample analysis produces:

```
============================================================
PUBLICATION ANALYSIS SUMMARY REPORT
============================================================

Total publications in dataset: 15
Year range: 2021 - 2023

--- CODESIGN PUBLICATIONS ---
Count: 8
Mean year: 2022.1
Median year: 2022

--- AI PUBLICATIONS ---
Count: 14
Mean year: 2022.2
Median year: 2022

--- CODESIGN + AI INTERSECTION ---
Count: 7
Mean year: 2022.3
Median year: 2022

--- TOP AUTHORS (CODESIGN) ---
Jane Smith: 1 publications
Emily Brown: 1 publications
...

--- TOP AUTHORS (AI) ---
Jane Smith: 1 publications
David Chen: 1 publications
...
```

## Customization

### Add Custom Keywords

Modify the search terms in the script:

```python
# In publication_analysis.py, update these lists:

codesign_terms = [
    'codesign', 'co-design',
    'your-custom-term',  # Add your terms here
]

ai_terms = [
    'artificial intelligence', 'machine learning',
    'your-custom-ai-term',  # Add your terms here
]
```

### Specify Search Columns

Control which columns to search:

```python
# Search only title and keywords
analyzer.filter_codesign_publications(text_columns=['title', 'keywords'])

# Search all text columns including abstract
analyzer.filter_ai_publications(text_columns=['title', 'keywords', 'abstract'])
```

### Adjust Top Authors Count

```python
# Get top 20 authors instead of default 10
top_authors = analyzer.extract_top_authors(codesign_pubs, top_n=20)
```

## Sample Data Description

The included `sample_publication_data.csv` contains 15 realistic publications:
- 8 codesign-related publications
- 14 AI-related publications  
- 7 publications at the intersection of both
- Publication years: 2021-2023
- Various venues (CHI, CVPR, ACL, etc.)

## Troubleshooting

### "No module named 'pandas'"
Install required packages:
```bash
pip install pandas numpy matplotlib
```

### "No 'year' column found"
Ensure your CSV has a 'year' column with integer years.

### No matches found
Check that:
1. Your column names match expected names (title, keywords, abstract)
2. The terms exist in your data (try case-insensitive search)
3. Your data encoding is UTF-8

### Empty intersection
This is normal if no publications combine both topics. Consider:
- Broadening search terms
- Checking different text columns
- Reviewing your dataset manually

## Advanced Usage

### Programmatic Access

```python
# Access filtered dataframes directly
codesign_df = analyzer.codesign_pubs
ai_df = analyzer.ai_pubs

# Custom filtering with pandas
recent_codesign = codesign_df[codesign_df['year'] >= 2022]

# Combine with other analyses
from collections import Counter
keywords = ' '.join(codesign_df['keywords'].dropna()).split(',')
keyword_freq = Counter(k.strip().lower() for k in keywords)
print(keyword_freq.most_common(10))
```

### Batch Processing

```python
# Analyze multiple datasets
datasets = ['data1.csv', 'data2.csv', 'data3.csv']

for dataset in datasets:
    analyzer = PublicationAnalyzer(dataset)
    analyzer.filter_codesign_publications()
    analyzer.filter_ai_publications()
    
    # Save results with dataset name
    base_name = dataset.replace('.csv', '')
    analyzer.codesign_pubs.to_csv(f'{base_name}_codesign.csv')
    analyzer.ai_pubs.to_csv(f'{base_name}_ai.csv')
```

## Next Steps

1. **Load your own data**: Replace `sample_publication_data.csv` with your dataset
2. **Customize search terms**: Add domain-specific keywords
3. **Extend analysis**: Add citation analysis, collaboration networks, venue analysis
4. **Visualize more**: Create word clouds, network graphs, heatmaps

## Support

For issues or questions:
1. Check that your data format matches the expected schema
2. Review the example notebook for proper usage
3. Test with `sample_publication_data.csv` first to verify installation

---

**Created for ThinkStats2 project** - Statistical analysis of publication data
