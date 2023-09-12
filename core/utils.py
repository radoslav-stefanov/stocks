import yfinance as yf

def fetch_spy_price_on_date(date):
    spy = yf.Ticker("SPY")
    historical_data = spy.history(period="1d", start=date, end=date)
    return historical_data['Close'][0] if not historical_data.empty else None
