from configparser import ConfigParser
from MyRobinhood.MyRobinhood import MyRobinhood


def main():
    config = ConfigParser()
    config.read("login.ini")
    username = config.get("ROBINHOOD", "username")
    password = config.get("ROBINHOOD", "password")

    # Setup
    my_trader = MyRobinhood()

    # login
    my_trader.login(username=username, password=password, mfa_code=None)

    account = my_trader.get_account()
    buying_power = account['buying_power']
    cash = account['cash']
    print(account)

    # Logout
    my_trader.logout()


if __name__ == '__main__':
    main()
