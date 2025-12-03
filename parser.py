import csv
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

class BookmarksParser(HTMLParser):
    def __init__(self, skip_root=True):
        super().__init__()
        self.bookmarks = []
        self.directory_stack = []
        self.current_tag = None
        self.current_directory = None
        self.skip_root = skip_root
        
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
            cleaned_title = self.clean_text(data)
            self.current_bookmark['title'] = cleaned_title
            dir_stack = self.directory_stack[1:] if self.skip_root and len(self.directory_stack) > 1 else self.directory_stack
            # '> ' separator is used because some categories uses '/'
            self.current_bookmark['directory'] = ' > '.join(dir_stack)
            self.bookmarks.append(self.current_bookmark.copy())

    @staticmethod
    def clean_text(text):
        """
        Remove unicode invisible characters and normalize text
        """
        # Remove unicode directional marks and other invisible characters
        # These include: LTR mark, RTL mark, zero-width space, etc.
        cleaned = ''.join(char for char in text if unicodedata.category(char)[0] != 'C' 
                         or char in ['\n', '\r', '\t'])
        
        # Also remove common invisible unicode characters explicitly
        invisible_chars = [
            '\u200e',  # Left-to-right mark
            '\u200f',  # Right-to-left mark
            '\u202a',  # Left-to-right embedding
            '\u202b',  # Right-to-left embedding
            '\u202c',  # Pop directional formatting
            '\u202d',  # Left-to-right override
            '\u202e',  # Right-to-left override
            '\u200b',  # Zero-width space
            '\u200c',  # Zero-width non-joiner
            '\u200d',  # Zero-width joiner
            '\ufeff',  # Zero-width no-break space
        ]
        
        for char in invisible_chars:
            cleaned = cleaned.replace(char, '')
        
        return cleaned.strip()

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

#### Not required as of now
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
    print(f"[1] Total bookmarks: {len(all_bookmarks)}")
    print(f"[1] Saved to {output_file}")
    
    return all_bookmarks

#####

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