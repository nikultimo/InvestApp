# Get your invest earning info from any stock
import yfinance as yf  # import YahooFinance | pip install yfinance
from datetime import date  # Import date


def parser_stock(stock_name):
    # Get today's date and get the last stock price (close parameter) by stock name
    # For example: parser_stock('TAL')
    today = date.today()
    day = today.strftime("%Y-%m-%d")
    # Catch error
    try:
        s = yf.download(stock_name, day)['Close']
        res = s[1]
        return res
    except:
        print('\n', '\033[1m', '\rThe are not any existing stock with this name.\n\
            \rChoose different name')
        st = input("Do you want to try one more time? y/n\n")
        if st == 'y':
            invest_goal()
        else:
            exit()


def invest_goal():
    # Define your stock earnings in rubles by specifying stock name, your amount of buyed shares
    # and average cost of your stock (you could get it from Tinkoff Investment App)
    # If you want to add your stock - just add their stock names below
    try:
        state = int(input('Do you want to specify your stock name or choose it from existing ones?\n \
        1 - Specify\n \
        2 - Choose\n -------------\n') or 2)
        if state == 1:
            stock_name = input("Specify stock name:\n -------------\n").upper()
            print('\033[1m', 'Current price (from YahooFinance): ',
                  parser_stock(stock_name), 'USD', '\033[0m')
        elif state == 2:
            stock_number = int(
                input("Choose stock number:\n 1 - TAL\n ------------- \n") or 1)
            if stock_number == 1:
                stock_name = 'TAL'
        stock_amount_of_shares = int(
            input("Specify amount of shares:\n -------------\n") or 191)
        stock_average_price = float(input("Specify price of your average stock cost in USD:\n \
            ------------- \n") or 5.31)
        tp = int(input('Do you want to specify your desired stock cost or get it from YahooFinance?\n \
        1 - Specify\n \
        2 - Get it\n -------------\n') or 2)
        if tp == 1:
            stock_price_now = float(
                input('Specify your desired cost in USD:\n') or 6)
        elif tp == 2:
            stock_price_now = parser_stock(stock_name)
        stock_price_usd = parser_stock('USDRUB=X')
        print(' -------------\n', '\033[1m', '\rYou will earn: ',
              stock_amount_of_shares *
              (stock_price_now - stock_average_price)*stock_price_usd,
              'RUB\n\n', '\033[0m')
    except (ValueError):
        print('\n', '\033[1m', '\rProvided input is not correct.\n', '\033[0m')
        st = input("\rDo you want to try one more time? y/n\n")
        if st == 'y':
            invest_goal()
        else:
            exit()


# Call invest_goal function
invest_goal()
st = 'y'
while st == 'y':
    st = input("'\rDo you want to continue? y/n\n")
    if st == 'y':
        invest_goal()
    else:
        print('\033[1m', 'Goodbye!', '\033[0m\n')
