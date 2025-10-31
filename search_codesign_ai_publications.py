#!/usr/bin/env python3
"""
Search for codesign and AI researcher publications
"""

import json
import sys
import urllib.request
import urllib.parse
import time
import xml.etree.ElementTree as ET

def search_semantic_scholar(query, limit=20):
    """Search Semantic Scholar API"""
    results = []
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,year,venue,abstract,citationCount,url"
        }
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        
        req = urllib.request.Request(full_url)
        req.add_header("User-Agent", "Mozilla/5.0")
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get("data", [])
    except Exception as e:
        print(f"Error searching Semantic Scholar: {e}", file=sys.stderr)
    return results

def search_arxiv(query, limit=20):
    """Search arXiv API"""
    results = []
    try:
        url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": limit,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        
        req = urllib.request.Request(full_url)
        req.add_header("User-Agent", "Mozilla/5.0")
        
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read().decode()
            root = ET.fromstring(xml_data)
            
            # Parse arXiv XML response
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = root.findall('.//atom:entry', namespace)
            
            for entry in entries[:limit]:
                title = entry.find('atom:title', namespace)
                title_text = title.text.strip().replace('\n', ' ') if title is not None else "N/A"
                
                authors = entry.findall('.//atom:author/atom:name', namespace)
                author_names = [a.text for a in authors] if authors else []
                
                published = entry.find('atom:published', namespace)
                year = published.text[:4] if published is not None else None
                
                summary = entry.find('atom:summary', namespace)
                abstract = summary.text.strip().replace('\n', ' ') if summary is not None else ""
                
                link = entry.find('atom:link[@type="text/html"]', namespace)
                url = link.get('href') if link is not None else ""
                
                id_elem = entry.find('atom:id', namespace)
                arxiv_id = id_elem.text if id_elem is not None else ""
                
                results.append({
                    "title": title_text,
                    "authors": author_names,
                    "year": year,
                    "abstract": abstract[:200] + "..." if len(abstract) > 200 else abstract,
                    "url": url,
                    "arxiv_id": arxiv_id,
                    "source": "arXiv"
                })
    except Exception as e:
        print(f"Error searching arXiv: {e}", file=sys.stderr)
    return results

def search_dblp(query, limit=20):
    """Search DBLP (Computer Science Bibliography)"""
    results = []
    try:
        url = "https://dblp.org/search/publ/api"
        params = {
            "q": query,
            "h": limit,
            "format": "json"
        }
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        
        req = urllib.request.Request(full_url)
        req.add_header("User-Agent", "Mozilla/5.0")
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get("result", {}).get("hits", {}).get("hit", [])
    except Exception as e:
        print(f"Error searching DBLP: {e}", file=sys.stderr)
    return results

def format_semantic_scholar_result(paper):
    """Format Semantic Scholar result"""
    authors = ", ".join([a.get("name", "") for a in paper.get("authors", [])[:5]])
    if len(paper.get("authors", [])) > 5:
        authors += " et al."
    
    return {
        "title": paper.get("title", "N/A"),
        "authors": authors,
        "year": paper.get("year"),
        "venue": paper.get("venue", "N/A"),
        "citation_count": paper.get("citationCount", 0),
        "url": paper.get("url", ""),
        "abstract": paper.get("abstract", "")[:200] + "..." if paper.get("abstract") else "",
        "source": "Semantic Scholar"
    }

def main():
    queries = [
        "hardware software codesign artificial intelligence",
        "algorithm hardware codesign neural network",
        "AI accelerator codesign",
        "neural network codesign",
        "machine learning codesign",
        "deep learning hardware codesign",
        "AI chip codesign",
        "human computer interaction AI codesign",
        "codesign framework AI"
    ]
    
    all_results = []
    
    print("Searching for codesign and AI researcher publications...")
    print("=" * 80)
    
    for query in queries:
        print(f"\nSearching: {query}")
        print("-" * 80)
        
        # Search Semantic Scholar
        print("  Querying Semantic Scholar...")
        try:
            ss_results = search_semantic_scholar(query, limit=10)
            for paper in ss_results[:5]:  # Limit to top 5 per query
                formatted = format_semantic_scholar_result(paper)
                # Check if already in results
                if not any(r.get('title') == formatted['title'] for r in all_results):
                    all_results.append(formatted)
                    print(f"    - {formatted['title']} ({formatted['year']})")
                    print(f"      Authors: {formatted['authors']}")
                    print(f"      Venue: {formatted['venue']}")
                    print(f"      Citations: {formatted['citation_count']}")
                    print()
        except Exception as e:
            print(f"    Error: {e}")
        
        # Search arXiv
        print("  Querying arXiv...")
        try:
            arxiv_results = search_arxiv(query, limit=5)
            for paper in arxiv_results:
                # Filter for relevant papers (must contain codesign/co-design related terms)
                title_lower = paper['title'].lower()
                abstract_lower = paper.get('abstract', '').lower()
                if any(term in title_lower or term in abstract_lower for term in 
                       ['codesign', 'co-design', 'co design', 'algorithm-hardware', 'hardware-software', 
                        'ai', 'artificial intelligence', 'neural', 'machine learning', 'accelerator']):
                    # Check if already in results
                    if not any(r.get('title') == paper['title'] for r in all_results):
                        all_results.append(paper)
                        authors_str = ", ".join(paper['authors'][:3])
                        if len(paper['authors']) > 3:
                            authors_str += " et al."
                        print(f"    - {paper['title']} ({paper['year']})")
                        print(f"      Authors: {authors_str}")
                        print(f"      URL: {paper['url']}")
                        print()
        except Exception as e:
            print(f"    Error: {e}")
        
        time.sleep(2)  # Rate limiting - increased delay
    
    # Save results to JSON
    output_file = "codesign_ai_publications.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 80}")
    print(f"Found {len(all_results)} publications")
    print(f"Results saved to: {output_file}")
    
    # Also create a summary text file
    with open("codesign_ai_publications_summary.txt", "w", encoding="utf-8") as f:
        f.write("Codesign and AI Researcher Publications\n")
        f.write("=" * 80 + "\n\n")
        for i, result in enumerate(all_results, 1):
            f.write(f"{i}. {result['title']}\n")
            if isinstance(result['authors'], list):
                authors_str = ", ".join(result['authors'][:5])
                if len(result['authors']) > 5:
                    authors_str += " et al."
                f.write(f"   Authors: {authors_str}\n")
            else:
                f.write(f"   Authors: {result['authors']}\n")
            f.write(f"   Year: {result['year']}\n")
            if result.get('venue'):
                f.write(f"   Venue: {result['venue']}\n")
            if result.get('citation_count') is not None:
                f.write(f"   Citations: {result['citation_count']}\n")
            if result.get('url'):
                f.write(f"   URL: {result['url']}\n")
            if result.get('arxiv_id'):
                f.write(f"   arXiv ID: {result['arxiv_id']}\n")
            if result.get('abstract'):
                f.write(f"   Abstract: {result['abstract']}\n")
            f.write(f"   Source: {result.get('source', 'Unknown')}\n")
            f.write("\n")
    
    print("Summary saved to: codesign_ai_publications_summary.txt")

if __name__ == "__main__":
    main()
