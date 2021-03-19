import requests
import hashlib
from urllib import parse
from urllib.parse import urlparse
from requests import HTTPError


class MiPage:
    def __init__(self, root_url, auth_data, auth_headers=None):

        if auth_headers is None:
            auth_headers = {}
        self.r_session = requests.Session()
        self.root_url = root_url

        # self.auth_response = self.get_auth_response()
        # print(self.auth_response.text)
        # self.auth_url = self.get_auth_url()
        # self.auth_param = self.get_auth_param()
        # self.dict_auth_param = self.get_dict_auth_param()
        # self.return_url = self.get_return_url()
        self._auth_headers = {}
        self._auth_data = {}
        self.auth_headers = auth_headers
        self.auth_data = auth_data

    @property
    def auth_response(self):
        return self.r_session.get(self.root_url)

    @property
    def auth_url(self):
        return 'https://account.xiaomi.com/pass/serviceLoginAuth2'

    @property
    def auth_param(self):
        return urlparse(self.auth_response.url).query

    @property
    def return_url(self):
        return self.dict_auth_param['callback']

    @property
    def dict_auth_param(self):
        return parse.parse_qs(self.auth_param)

    @property
    def auth_headers(self):
        return self._auth_headers

    @auth_headers.setter
    def auth_headers(self, auth_headers):
        # auth_headers['Referer'] = self.auth_response.url
        self._auth_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        # print(auth_headers)
        for k, v in auth_headers.items():
            self._auth_data[k] = v

    @property
    def auth_data(self):
        return self._auth_data

    @auth_data.setter
    def auth_data(self, auth_data):
        for k, v in self.dict_auth_param.items():
            self._auth_data[k] = v
        for k, v in auth_data.items():
            self._auth_data[k] = v

    def login(self):

        # print(self.auth_headers)
        # print(self.auth_data)
        # print(self.auth_url)
        try:
            login_response = self.r_session.post(url=self.auth_url, headers=self._auth_headers, data=self._auth_data)
            return login_response
        except HTTPError as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            return None


if __name__ == '__main__':
    hash_pass = hashlib.md5('XXX'.encode('utf8')).hexdigest()
    data = {'user': 'XXX', 'hash': hash_pass, 'cc': '+86', }
    test = MiPage('https://d.miwifi.com/d2r/login?referer=http%3A%2F%2Fd.miwifi.com%2Fd2r%2F', data)
    r = test.login()
    print(r.text)
