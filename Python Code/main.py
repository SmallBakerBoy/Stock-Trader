import market_data as md
import database as db






current_user = 2

def create_portfolio(user):
    SP500 = list(md.get_sp500.values())
    blacklist = db.fetch_blacklist()
    companies = [x for x in SP500 if x not in blacklist]

    market_data = md.get_market_data(companies)
    

def calc_principal_comps(n):
    pass

