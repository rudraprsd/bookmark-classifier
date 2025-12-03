import csv
from html.parser import HTMLParser
from pathlib import Path

class BookmarksParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.bookmarks = []
        self.directory_stack = []
        self.current_tag = None
        self.current_directory = None
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        
        if tag == 'h3':
            # This is a folder/directory
            self.current_directory = None
        elif tag == 'a':
            # This is a bookmark
            href = attrs_dict.get('href', '')
            self.current_bookmark = {'link': href, 'title': '', 'directory': ''}
    
    def handle_endtag(self, tag):
        if tag == 'dl':
            # Exiting a directory level
            if self.directory_stack:
                self.directory_stack.pop()
        self.current_tag = None
    
    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
            
        if self.current_tag == 'h3':
            # This is a directory name
            self.current_directory = data
            self.directory_stack.append(data)
        elif self.current_tag == 'a':
            # This is a bookmark title
            self.current_bookmark['title'] = data
            self.current_bookmark['directory'] = ' > '.join(self.directory_stack)
            self.bookmarks.append(self.current_bookmark.copy())

def parse_bookmarks(input_file, output_file='bookmarks_data.csv'):
    """
    Parse bookmarks HTML file and export to CSV
    
    Args:
        input_file: Path to the bookmarks.html file
        output_file: Path for the output CSV file (default: bookmarks_data.csv)
    """
    # Read the HTML file
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse the bookmarks
    parser = BookmarksParser()
    parser.feed(html_content)
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if parser.bookmarks:
            writer = csv.DictWriter(f, fieldnames=['title', 'link', 'directory'])
            writer.writeheader()
            writer.writerows(parser.bookmarks)
            
    print(f"[1] Parsed {len(parser.bookmarks)} bookmarks")
    print(f"[1] Saved to {output_file}")
    
    return parser.bookmarks

def parse_all_bookmarks_in_directory(directory_path='bookmarks', output_file='all_bookmarks.csv'):
    """
    Parse all HTML files in a directory and combine into one CSV
    
    Args:
        directory_path: Path to directory containing bookmarks files
        output_file: Path for the output CSV file
    """
    all_bookmarks = []
    bookmarks_dir = Path(directory_path)
    
    if not bookmarks_dir.exists():
        print(f"Error: Directory '{directory_path}' not found")
        return
    
    html_files = list(bookmarks_dir.glob('*.html'))
    
    if not html_files:
        print(f"No HTML files found in '{directory_path}'")
        return
    
    for html_file in html_files:
        print(f"Processing {html_file.name}...")
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        parser = BookmarksParser()
        parser.feed(html_content)
        all_bookmarks.extend(parser.bookmarks)
    
    # Write all bookmarks to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if all_bookmarks:
            writer = csv.DictWriter(f, fieldnames=['title', 'link', 'directory'])
            writer.writeheader()
            writer.writerows(all_bookmarks)
    
    print(f"\n✓ Processed {len(html_files)} file(s)")
    print(f"✓ Total bookmarks: {len(all_bookmarks)}")
    print(f"✓ Saved to {output_file}")
    
    return all_bookmarks

# Example usage:
if __name__ == "__main__":
    # Option 1: Parse a single bookmarks.html file
    bookmarks = parse_bookmarks('bookmarks.html', 'output.csv')
    
    # Option 2: Parse all HTML files in the 'bookmarks' directory
    # bookmarks = parse_all_bookmarks_in_directory('bookmarks', 'all_bookmarks.csv')
    
    # Display sample of the data
    if bookmarks:
        print("\nSample of parsed data:")
        print("-" * 80)
        for bookmark in bookmarks[:3]:
            print(f"Title: {bookmark['title']}")
            print(f"Link: {bookmark['link']}")
            print(f"Directory: {bookmark['directory']}")
            print("-" * 80)