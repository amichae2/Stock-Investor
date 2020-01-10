import random
from six.moves.configparser import ConfigParser

# Application-specific imports
from Robinhood.Robinhood import exceptions as RH_exception, endpoints, Robinhood

# email specific imports
from MyRobinhood.gmail.verify_email import get_email_code


class MyRobinhood(Robinhood.Robinhood):
    """Wrapper class for fetching/parsing Robinhood endpoints """

    ###########################################################################
    #                       Logging in and initializing
    ###########################################################################

    def __init__(self):
        super().__init__()
        self.headers = {
            # ":authority": "api.robinhood.com",  # this to
            # ":method": "POST",
            # ":path": "/oauth2/token/",
            # ":scheme": "https",
            "content-length": "238",
            "origin": "https://robinhood.com",
            "referer": "https://robinhood.com/login",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            #              "Chrome/79.0.3945.88 Safari/537.36",
            "Connection": "keep-alive",
            # "X-Robinhood-API-Version": "1.303.3"  # 1.0.0 may be required
        }
        self.device_token = ""
        self.challenge_id = ""

    def GenerateDeviceToken(self):
        rands = []
        for i in range(0, 16):
            r = random.random()
            rand = 4294967296.0 * r
            rands.append((int(rand) >> ((3 & i) << 3)) & 255)

        hexa = []
        for i in range(0, 256):
            hexa.append(str(hex(i + 256)).lstrip("0x").rstrip("L")[1:])

        id = ""
        for i in range(0, 16):
            id += hexa[rands[i]]

            if (i == 3) or (i == 5) or (i == 7) or (i == 9):
                id += "-"

        self.device_token = id

    def login(self, username, password, mfa_code=None):
        self.username = username
        self.password = password

        config = ConfigParser()
        config.read("login.ini")
        gmail = config.get("GMAIL", "gmail")

        if self.device_token == "":
            self.GenerateDeviceToken()
            # self.device_token = "e5f03935-3187-4aea-8470-67e071ae0e8f"

        payload = {
            'grant_type': "password",
            'scope': "internal",
            'client_id': self.client_id,
            'expires_in': 86400,
            'device_token': self.device_token,
            'username': self.username,
            'password': self.password,
            'challenge_type': 'email'
        }

        try:
            res = self.session.post(endpoints.login(), data=payload, timeout=15)

            # res.raise_for_status() keep commented out; when not commented out code stops after getting bad request
            # returned because of challenge

            response_data = res.json()
            if self.challenge_id == "" and "challenge" in response_data.keys():
                self.challenge_id = response_data["challenge"]["id"]
            self.headers["X-ROBINHOOD-CHALLENGE-RESPONSE-ID"] = self.challenge_id  # has to add this to stay logged in
            email_challenge_endpoint = "https://api.robinhood.com/challenge/{}/respond/".format(self.challenge_id)

            # wait to execute this code (WAIT FOR EMAIL)
            email_code = get_email_code.get_email_code(user_id=gmail, includeSpamTrash=False,
                                                       maxResults=1, query='from:notifications@robinhood.com')
            print(email_code)

            data = res.json()
        finally:
            print(gmail)
        # except requests.exceptions.HTTPError:
        # raise RH_exception.LoginFailed()

        if 'access_token' in data.keys() and 'refresh_token' in data.keys():
            self.auth_token = data['access_token']
            self.refresh_token = data['refresh_token']
            self.headers['Authorization'] = 'Bearer ' + self.auth_token
            return True

        return False
