import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import re

# ---- Functions ----
scraped_data = []

def scrape_data():
    global scraped_data
    url = url_entry.get().strip()
    selector = element_entry.get().strip()
    scrape_type = scrape_type_var.get()
    
    if not url or not selector:
        messagebox.showwarning("Input Error", "Please provide both URL and element selector.")
        return

    scraped_data = []
    page = 1
    max_pages = 50
    
    # Reset progress bar
    progress_bar["value"] = 0
    progress_label.config(text="Progress: 0%")
    root.update_idletasks()
    
    try:
        while True:
            page_url = url.replace("{page}", str(page)) if "{page}" in url else url
            response = requests.get(page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.select(selector)
            if not elements:
                break

            for el in elements:
                if scrape_type == "Text":
                    scraped_data.append(el.get_text(strip=True))
                elif scrape_type == "Links":
                    href = el.get("href")
                    if href:
                        scraped_data.append(href)
                elif scrape_type == "Images":
                    if el.name == "img":
                        src = el.get("src")
                        if src:
                            scraped_data.append(src)

            # Update progress
            progress_percent = (page / max_pages) * 100
            progress_bar["value"] = min(progress_percent, 100)
            progress_label.config(text=f"Scraping page {page}...")
            root.update_idletasks()
            
            page += 1
            if page > max_pages:
                break

        # Display results
        result_list.delete(0, tk.END)
        for item in scraped_data:
            result_list.insert(tk.END, item)

        progress_bar["value"] = 100
        progress_label.config(text=f"Done! Scraped {len(scraped_data)} items across {page-1} pages.")
        root.update_idletasks()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data:\n{e}")
        progress_label.config(text="Error occurred")
        root.update_idletasks()

def export_data_csv():
    if not scraped_data:
        messagebox.showwarning("No Data", "Scrape data first before exporting.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files","*.csv")])
    if file_path:
        pd.DataFrame(scraped_data, columns=["Data"]).to_csv(file_path, index=False)
        messagebox.showinfo("Success", f"Data exported to {file_path}")

def export_data_excel():
    if not scraped_data:
        messagebox.showwarning("No Data", "Scrape data first before exporting.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files","*.xlsx")])
    if file_path:
        pd.DataFrame(scraped_data, columns=["Data"]).to_excel(file_path, index=False)
        messagebox.showinfo("Success", f"Data exported to {file_path}")

def filter_data():
    keyword = filter_entry.get().strip().lower()
    if not scraped_data:
        messagebox.showwarning("No Data", "Scrape data first before filtering.")
        return
    if not keyword:
        messagebox.showwarning("No Keyword", "Please enter a keyword to filter.")
        return
    filtered = [item for item in scraped_data if keyword in item.lower()]
    result_list.delete(0, tk.END)
    if not filtered:
        messagebox.showinfo("No Results", f"No items matched '{keyword}'")
        return
    for item in filtered:
        result_list.insert(tk.END, item)

def regex_extract():
    pattern = regex_entry.get().strip()
    if not scraped_data:
        messagebox.showwarning("No Data", "Scrape data first before applying regex.")
        return
    if not pattern:
        messagebox.showwarning("No Pattern", "Please enter a regex pattern.")
        return
    try:
        extracted = []
        for item in scraped_data:
            matches = re.findall(pattern, item)
            extracted.extend(matches)
        result_list.delete(0, tk.END)
        if not extracted:
            messagebox.showinfo("No Matches", f"No items matched the pattern '{pattern}'")
            return
        for match in extracted:
            result_list.insert(tk.END, match)
    except re.error as e:
        messagebox.showerror("Regex Error", f"Invalid pattern:\n{e}")

# ---- GUI Setup ----
root = tk.Tk()
root.title("Web Scraper")
root.geometry("750x700")
root.resizable(False, False)

# Centered frame
content_frame = tk.Frame(root)
content_frame.pack(pady=10)

# URL
tk.Label(content_frame, text="Target URL:").grid(row=0, column=0, sticky="w")
url_entry = tk.Entry(content_frame, width=50)
url_entry.grid(row=0, column=1, pady=3)

# CSS selector
tk.Label(content_frame, text="CSS Selector / Element:").grid(row=1, column=0, sticky="w")
element_entry = tk.Entry(content_frame, width=35)
element_entry.grid(row=1, column=1, sticky="w", pady=3)

# Scrape type dropdown (next to CSS selector)
scrape_type_var = tk.StringVar(value="Text")
scrape_type_dropdown = ttk.OptionMenu(content_frame, scrape_type_var, "Text", "Text", "Links", "Images")
scrape_type_dropdown.grid(row=1, column=1, sticky="e", padx=5, pady=3)

# Scrape button
scrape_button = tk.Button(content_frame, text="Scrape Data", width=20, command=scrape_data)
scrape_button.grid(row=2, column=0, columnspan=2, pady=5)

# Scrollable Listbox
listbox_frame = tk.Frame(content_frame)
listbox_frame.grid(row=3, column=0, columnspan=2, pady=5)
scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_list = tk.Listbox(listbox_frame, width=80, height=15, yscrollcommand=scrollbar.set)
result_list.pack()
scrollbar.config(command=result_list.yview)

# Export buttons
export_csv_btn = tk.Button(content_frame, text="Export CSV", width=15, command=export_data_csv)
export_csv_btn.grid(row=4, column=0, pady=3)
export_excel_btn = tk.Button(content_frame, text="Export Excel", width=15, command=export_data_excel)
export_excel_btn.grid(row=4, column=1, pady=3)

# Filter
tk.Label(content_frame, text="Filter / Keyword:").grid(row=5, column=0, sticky="w")
filter_entry = tk.Entry(content_frame, width=35)
filter_entry.grid(row=5, column=1, pady=3)
filter_button = tk.Button(content_frame, text="Apply Filter", width=20, command=filter_data)
filter_button.grid(row=6, column=0, columnspan=2, pady=5)

# Regex
tk.Label(content_frame, text="Regex Pattern:").grid(row=7, column=0, sticky="w")
regex_entry = tk.Entry(content_frame, width=35)
regex_entry.grid(row=7, column=1, pady=3)
regex_button = tk.Button(content_frame, text="Apply Regex", width=20, command=regex_extract)
regex_button.grid(row=8, column=0, columnspan=2, pady=5)

# Progress
progress_label = tk.Label(content_frame, text="Progress: 0%")
progress_label.grid(row=9, column=0, sticky="w", pady=3)
progress_bar = ttk.Progressbar(content_frame, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=9, column=1, pady=3)

root.mainloop()
