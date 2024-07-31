from playwright.sync_api import sync_playwright
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
  filename='financial-data/invalid-symbols.log', 
  filemode='a', 
  encoding='utf-8', 
  level=logging.INFO,
  format='%(message)s'  # Only log the message, no other information
)

def scrape(symbol_list: list):
  """
  Scrape csv files from Yahoo Finance for all ticker symbols in symbol_list.

  Parameters:
  symbol_list (list): A list of ticker symbols.
  """
  print('log info: scrape')
  with sync_playwright() as p:
    # specify the download path
    download_path = os.path.join(os.getcwd(), "financial-data/automated")
    os.makedirs(download_path, exist_ok=True)

    # headless so I see the browser, slow_mo so I see it better
    # browser = p.chromium.launch(headless=False, slow_mo=1000)
    browser = p.chromium.launch()
    context = browser.new_context(accept_downloads=True)
    page = browser.new_page()

    for symbol in symbol_list:
      try:
        # page.goto(f"https://finance.yahoo.com/quote/{symbol}/history/")
        # page.click('button[class="tertiary-btn fin-size-small menuBtn rounded yf-122t2xs"]')
        # page.fill('input[name="startDate"]', '2014-01-01')
        # page.fill('input[name="endDate"]', '2023-12-31')
        # page.click('button[class="primary-btn fin-size-small rounded yf-122t2xs"]')
        
        # I can put the time period in the link by using unix time stamps.
        # 1388534400 = 01.01.2014, 00:00; 1704067200 = 01.01.2024, 00:00
        page.goto(f"https://finance.yahoo.com/quote/{symbol}/history/?period1=1388534400&period2=1704067200")

        with page.expect_download(timeout=10000) as download_info:
          page.click('a[class="subtle-link fin-size-medium yf-13p9sh2"]')

        download = download_info.value
        download.save_as(os.path.join(download_path, download.suggested_filename))
        print(f"File downloaded to: {os.path.join(download_path, download.suggested_filename)}")
      except:
        print(f"ERROR for {symbol}")
        logger.info(symbol)

    browser.close()

def extract_stock_symbols_nasdaq():
  """
  Extract ticker symbols from stocks traded on the Nasdaq and write them to a new text file.
  """
  print('log info: extract symbols from complete data')
  input_file_path = 'financial-data/nasdaqlisted.txt'
  output_file_path = 'financial-data/nasdaqlisted-symbols.txt'

  # Open the input file for reading
  with open(input_file_path, 'r') as infile:
    next(infile)  # Skip the first line
    # Open the output file for writing
    with open(output_file_path, 'w') as outfile:
      # Read each line from the input file
      for line in infile:
        # Split the line by '|' and get the first element (symbol)
        symbol = line.split('|')[0]
        # Write the symbol to the output file
        outfile.write(symbol + '\n')

  print(f"Symbols have been extracted and written to {output_file_path}")

def get_qoute_list(invalid_symbols: list):
  """
  Read the stock ticker symbols from the file I wrote with the extract_stock_symbols_nasdaq function.

  Parameters:
  invalid_symbols (list): A list with all symbols for which scraping failed the last time.

  Returns:
  list: A list with stock ticker symbols.
  """
  print('log info: read ticker symbols from file')
  out = []
  input_file_path = 'financial-data/nasdaqlisted-symbols.txt'
  with open(input_file_path, 'r') as infile:
    for line in infile:
      symbol = line.strip()
      if not symbol in invalid_symbols:
        out.append(line.strip())
  return out

def get_invalid_symbols():
  """
  Create list of ticker symbols, for which previous scrapings failed based on logs.

  Returns:
  list: A list containing invalid ticker symbols.
  """
  print('log info: read invalid ticker symbols from logs')
  out = []
  input_file_path = 'financial-data/invalid-symbols.log'
  with open(input_file_path, 'r') as infile:
    for line in infile:
      out.append(line.strip())
  return out

def get_already_scraped_symbols():
  """
  Check for which ticker symbols I already have a csv file.

  Returns:
  list: A list containing already scraped ticker symbols.
  """
  print('log info: read already scraped ticker symbols')
  out = []
  # List all files in the specified directory
  for filename in os.listdir("financial-data/automated"):
      if filename.endswith('.csv'):
          # Extract the ticker symbol by removing the '.csv' extension
          symbol = filename[:-4]
          out.append(symbol)
  return out


ticker_symbols = []
dont_scrape_symbols = []

dont_scrape_symbols.extend(get_invalid_symbols())
dont_scrape_symbols.extend(get_already_scraped_symbols())

extract_stock_symbols_nasdaq()
ticker_symbols = get_qoute_list(dont_scrape_symbols)
scrape(ticker_symbols)
