import finnhub as fh
import market_data as md

fh_client = fh.Client(api_key="d5r3eo9r01qqqlh9irjgd5r3eo9r01qqqlh9irk0")

def search(query):
    lookup = fh_client.symbol_lookup(query)
    SP500 = list(md.get_sp500().values())
    companies = [x['symbol'] for x in lookup['result'] if x['symbol'] in SP500]
    return companies
    