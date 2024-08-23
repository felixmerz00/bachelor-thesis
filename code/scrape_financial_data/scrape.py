from playwright.sync_api import sync_playwright
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
  filename='code/scrape_financial_data/invalid-symbols.log',
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
    # Specify the download path
    download_path = os.path.join(os.getcwd(), "data/finance/automated")
    os.makedirs(download_path, exist_ok=True)

    # Headless so I see the browser, slow_mo so I see it better
    # browser = p.chromium.launch(headless=False, slow_mo=1000)   # For debugging
    browser = p.chromium.launch()
    context = browser.new_context(accept_downloads=True)
    page = browser.new_page()

    # Navigate the cookie banner
    re = page.goto(f"https://finance.yahoo.com")
    # print(f"response.status {re.status}")   # For debugging
    page.click('button[id="scroll-down-btn"]')
    page.click('button[class="btn secondary accept-all "]')

    for symbol in symbol_list:
      print(f"log info: working on {symbol}")
      try:
        # I can put the time period in the link by using unix time stamps.
        # 1388534400 = 01.01.2014, 00:00; 1704067200 = 01.01.2024, 00:00
        page.goto(f"https://finance.yahoo.com/quote/{symbol}/history/?period1=1388534400&period2=1704067200")

        with page.expect_download(timeout=10000) as download_info:
          page.get_by_test_id("download-link").click(timeout=10000)

        download = download_info.value
        download.save_as(os.path.join(download_path, download.suggested_filename))
        print(f"log info: file downloaded to: {os.path.join(download_path, download.suggested_filename)}")
      except Exception as e:
        print(f"ERROR for {symbol}")
        logger.info(symbol)

    browser.close()

def extract_stock_symbols_nasdaq():
  """
  Extract ticker symbols from stocks traded on the Nasdaq and write them to a new text file.
  """
  print('log info: extract symbols from complete data')
  input_file_path = 'code/scrape_financial_data/nasdaqlisted.txt'
  output_file_path = 'code/scrape_financial_data/nasdaqlisted-symbols.txt'

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

  print(f"log info: symbols have been extracted and written to {output_file_path}")

def get_qoute_list(invalid_symbols: list):
  """
  Read the stock ticker symbols from the file I wrote with the extract_stock_symbols_nasdaq function.

  Parameters:
  invalid_symbols: A list with all symbols for which scraping failed the last time.

  Returns:
  list: A list with stock ticker symbols.
  """
  print('log info: read ticker symbols from file')
  out = []
  input_file_path = 'code/scrape_financial_data/nasdaqlisted-symbols.txt'
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
  input_file_path = 'code/scrape_financial_data/invalid-symbols.log'
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
  for filename in os.listdir("data/finance/automated"):
      if filename.endswith('.csv'):
          # Extract the ticker symbol by removing the '.csv' extension
          symbol = filename[:-4]
          out.append(symbol)
  return out


ticker_symbols = []
dont_scrape_symbols = []

dont_scrape_symbols.extend(get_invalid_symbols())
dont_scrape_symbols.extend(get_already_scraped_symbols())

# extract_stock_symbols_nasdaq()  # Run this only when nasdaqlisted.txt changes
ticker_symbols = get_qoute_list(dont_scrape_symbols)
scrape(ticker_symbols)
