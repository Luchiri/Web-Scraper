# Python Web Scraper GUI

A **user-friendly Python GUI application** to scrape data from websites. This tool allows you to scrape **text, links, or images** from any page using CSS selectors, preview the data, filter results, apply regex patterns, and export the data to CSV or Excel files.

## Features

- Scrape **Text, Links, or Images** from websites using CSS selectors.
- Handle **pagination** automatically (if URL has `{page}` placeholder).
- **Filter scraped data** using keywords.
- Apply **regular expressions** to extract patterns.
- **Progress bar** shows scraping status for multiple pages.
- **Preview** results in a scrollable Listbox.
- Export data to **CSV or Excel**.
- Simple, **centered GUI** layout with scrollable Listbox.
- Supports **error handling** for bad URLs or missing elements.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/luchiri/web-scraper.git
Navigate to the project folder:

bash
Copy code
cd python-web-scraper-gui
Install dependencies (make sure you have Python 3.x installed):

bash
Copy code
pip install -r requirements.txt
If you don't have a requirements.txt, install manually:

bash
Copy code
pip install requests beautifulsoup4 pandas
Usage
Run the application:

bash
Copy code
python web-scraper.py
Enter the Target URL of the website you want to scrape.

Enter the CSS Selector for the elements you want to extract.

Choose the Scrape Type from the dropdown (Text, Links, or Images).

Click Scrape Data → results appear in the Listbox.

Optional:

Filter / Keyword → display only items that match a keyword.

Regex Pattern → extract specific patterns from the scraped data.

Export → save the visible data to CSV or Excel.

Example
URL: https://quotes.toscrape.com/

CSS Selector (Text): .quote .text

CSS Selector (Links): .quote span a

CSS Selector (Images): img

Screenshots
(Include a screenshot of the GUI here if possible)
