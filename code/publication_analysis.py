"""
Publication Analysis for Codesign and AI Researchers
This script analyzes publication data to find codesign and AI researcher publications.

Expected data format (CSV or JSON):
- title: Publication title
- authors: Author names (comma-separated or list)
- year: Publication year
- keywords: Keywords (comma-separated or list)
- abstract: Abstract text (optional)
- venue: Conference/journal name (optional)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PublicationAnalyzer:
    """Analyzer for publication data focused on codesign and AI research."""
    
    def __init__(self, data_path=None):
        """Initialize the analyzer with optional data path."""
        self.data = None
        self.codesign_pubs = None
        self.ai_pubs = None
        
        if data_path:
            self.load_data(data_path)
    
    def load_data(self, filepath):
        """
        Load publication data from CSV or JSON file.
        
        Args:
            filepath: Path to the data file
        """
        if filepath.endswith('.csv'):
            self.data = pd.read_csv(filepath)
        elif filepath.endswith('.json'):
            self.data = pd.read_json(filepath)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")
        
        print(f"Loaded {len(self.data)} publications")
        print(f"Columns: {list(self.data.columns)}")
        return self.data
    
    def filter_codesign_publications(self, text_columns=['title', 'keywords', 'abstract']):
        """
        Filter publications related to codesign.
        
        Searches for codesign-related terms in specified text columns.
        """
        codesign_terms = [
            'codesign', 'co-design', 'collaborative design', 
            'participatory design', 'human-centered design',
            'user-centered design', 'design thinking'
        ]
        
        mask = pd.Series([False] * len(self.data))
        
        for col in text_columns:
            if col in self.data.columns:
                for term in codesign_terms:
                    mask |= self.data[col].str.contains(term, case=False, na=False)
        
        self.codesign_pubs = self.data[mask]
        print(f"Found {len(self.codesign_pubs)} codesign publications")
        return self.codesign_pubs
    
    def filter_ai_publications(self, text_columns=['title', 'keywords', 'abstract']):
        """
        Filter publications related to AI research.
        
        Searches for AI-related terms in specified text columns.
        """
        ai_terms = [
            'artificial intelligence', 'machine learning', 'deep learning',
            'neural network', 'natural language processing', 'NLP',
            'computer vision', 'reinforcement learning', 'AI',
            'large language model', 'LLM', 'transformer'
        ]
        
        mask = pd.Series([False] * len(self.data))
        
        for col in text_columns:
            if col in self.data.columns:
                for term in ai_terms:
                    mask |= self.data[col].str.contains(term, case=False, na=False)
        
        self.ai_pubs = self.data[mask]
        print(f"Found {len(self.ai_pubs)} AI publications")
        return self.ai_pubs
    
    def find_intersection(self):
        """Find publications that are both codesign AND AI related."""
        if self.codesign_pubs is None:
            self.filter_codesign_publications()
        if self.ai_pubs is None:
            self.filter_ai_publications()
        
        # Find publications in both categories
        intersection = pd.merge(
            self.codesign_pubs, 
            self.ai_pubs, 
            how='inner'
        )
        
        print(f"Found {len(intersection)} publications at intersection of codesign and AI")
        return intersection
    
    def analyze_temporal_trends(self, subset=None):
        """
        Analyze publication trends over time.
        
        Args:
            subset: DataFrame subset to analyze (default: all data)
        """
        data_to_analyze = subset if subset is not None else self.data
        
        if 'year' not in data_to_analyze.columns:
            print("No 'year' column found in data")
            return None
        
        # Count publications per year
        yearly_counts = data_to_analyze['year'].value_counts().sort_index()
        
        # Calculate statistics
        stats = {
            'mean_year': data_to_analyze['year'].mean(),
            'median_year': data_to_analyze['year'].median(),
            'std_year': data_to_analyze['year'].std(),
            'total_pubs': len(data_to_analyze),
            'year_range': (data_to_analyze['year'].min(), data_to_analyze['year'].max())
        }
        
        return yearly_counts, stats
    
    def plot_publication_trends(self):
        """Plot publication trends for codesign, AI, and their intersection."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if self.codesign_pubs is not None and 'year' in self.codesign_pubs.columns:
            codesign_yearly = self.codesign_pubs['year'].value_counts().sort_index()
            ax.plot(codesign_yearly.index, codesign_yearly.values, 
                   label='Codesign', marker='o', linewidth=2)
        
        if self.ai_pubs is not None and 'year' in self.ai_pubs.columns:
            ai_yearly = self.ai_pubs['year'].value_counts().sort_index()
            ax.plot(ai_yearly.index, ai_yearly.values, 
                   label='AI', marker='s', linewidth=2)
        
        intersection = self.find_intersection()
        if len(intersection) > 0 and 'year' in intersection.columns:
            inter_yearly = intersection['year'].value_counts().sort_index()
            ax.plot(inter_yearly.index, inter_yearly.values, 
                   label='Codesign + AI', marker='^', linewidth=2)
        
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Publications')
        ax.set_title('Publication Trends: Codesign and AI Research')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def extract_top_authors(self, subset=None, top_n=10):
        """
        Extract top authors by publication count.
        
        Args:
            subset: DataFrame subset to analyze (default: all data)
            top_n: Number of top authors to return
        """
        data_to_analyze = subset if subset is not None else self.data
        
        if 'authors' not in data_to_analyze.columns:
            print("No 'authors' column found in data")
            return None
        
        # Extract individual authors
        all_authors = []
        for authors in data_to_analyze['authors'].dropna():
            if isinstance(authors, str):
                # Split by comma or semicolon
                author_list = [a.strip() for a in authors.replace(';', ',').split(',')]
                all_authors.extend(author_list)
            elif isinstance(authors, list):
                all_authors.extend(authors)
        
        # Count occurrences
        author_counts = pd.Series(all_authors).value_counts().head(top_n)
        return author_counts
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report."""
        print("\n" + "="*60)
        print("PUBLICATION ANALYSIS SUMMARY REPORT")
        print("="*60 + "\n")
        
        if self.data is not None:
            print(f"Total publications in dataset: {len(self.data)}")
            
            if 'year' in self.data.columns:
                print(f"Year range: {self.data['year'].min()} - {self.data['year'].max()}")
        
        print("\n--- CODESIGN PUBLICATIONS ---")
        if self.codesign_pubs is not None:
            print(f"Count: {len(self.codesign_pubs)}")
            if 'year' in self.codesign_pubs.columns:
                _, stats = self.analyze_temporal_trends(self.codesign_pubs)
                print(f"Mean year: {stats['mean_year']:.1f}")
                print(f"Median year: {stats['median_year']:.0f}")
        
        print("\n--- AI PUBLICATIONS ---")
        if self.ai_pubs is not None:
            print(f"Count: {len(self.ai_pubs)}")
            if 'year' in self.ai_pubs.columns:
                _, stats = self.analyze_temporal_trends(self.ai_pubs)
                print(f"Mean year: {stats['mean_year']:.1f}")
                print(f"Median year: {stats['median_year']:.0f}")
        
        print("\n--- CODESIGN + AI INTERSECTION ---")
        intersection = self.find_intersection()
        if len(intersection) > 0:
            print(f"Count: {len(intersection)}")
            if 'year' in intersection.columns:
                _, stats = self.analyze_temporal_trends(intersection)
                print(f"Mean year: {stats['mean_year']:.1f}")
                print(f"Median year: {stats['median_year']:.0f}")
        
        print("\n--- TOP AUTHORS (CODESIGN) ---")
        top_codesign_authors = self.extract_top_authors(self.codesign_pubs, top_n=5)
        if top_codesign_authors is not None:
            for author, count in top_codesign_authors.items():
                print(f"{author}: {count} publications")
        
        print("\n--- TOP AUTHORS (AI) ---")
        top_ai_authors = self.extract_top_authors(self.ai_pubs, top_n=5)
        if top_ai_authors is not None:
            for author, count in top_ai_authors.items():
                print(f"{author}: {count} publications")
        
        print("\n" + "="*60 + "\n")


# Example usage
if __name__ == "__main__":
    print("Publication Analysis Tool for Codesign and AI Research")
    print("="*60)
    print("\nUsage:")
    print("1. Prepare your data as CSV with columns: title, authors, year, keywords, abstract")
    print("2. Run: analyzer = PublicationAnalyzer('your_data.csv')")
    print("3. Filter: analyzer.filter_codesign_publications()")
    print("4. Filter: analyzer.filter_ai_publications()")
    print("5. Analyze: analyzer.generate_summary_report()")
    print("6. Visualize: analyzer.plot_publication_trends()")
    print("\nExpected CSV format:")
    print("title,authors,year,keywords,abstract,venue")
    print("\nExample:")
    print("'AI for Design','John Doe, Jane Smith',2023,'AI, design','...','CHI 2023'")
