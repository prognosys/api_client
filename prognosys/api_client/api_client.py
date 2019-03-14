from __future__ import annotations
from requests.auth import HTTPBasicAuth
from pathlib import Path
from typing import Optional, Dict
from .errors import HttpError
import json
import logging
import requests


class ApiClient():
    """Class to create an interface with Prognosys Gateway API
    
    It is responsible for authenticate with api and handle HTTP methods.
    """
    def __init__(self,
                 token:str,
                 host:str = 'localhost', 
                 port:int = 5000,
    ) -> None:
        '''Construct a ApiClient object.
        
        Use to abstract connection with Prognosys Gateway API and its objects.

        :args:
            token: Authentication token string. Any application must have an API Token 
                that can be created using the Gateway Web Application or the CLI.
            host: URL address of the gateway where the API is installed.
            port: Port to which the gateway is listening.
        '''
        self.token = token
        self.host = host
        self.port = port
        self.is_connected = False
        self.logger = logging.getLogger(__name__)

    def __create_url(self,
                     endpoint: str) -> str:
        '''Create url with client parameters.'''
        if endpoint[0] == '/':
            endpoint = endpoint[:1]
        return f'http://{self.host}:{self.port}/{endpoint}'

    def get(self, 
            endpoint:str
    ) -> Dict:
        """Get data from an endpoint
        
        :args:
            endpoint: string with the url to request

        :returns:
            dict with response data. If fails, returns an empty dict

        :raises:
            HttpError: the connection was not successful with the server.
        """
        url = self.__create_url(endpoint)
        self.logger.info(f'Requesting data from {url}')

        r = requests.get(url, auth=HTTPBasicAuth(self.token, 'x'))
        if r.status_code != 200:
            raise HttpError(str(r.text), r.status_code)

        # Successfull request
        resp = r.json()
        self.logger.info('Data requested successfully.')
        self.logger.debug(f'{str(resp)[:200]}')

        # Return data
        return resp

    def post(self, 
             endpoint: str, 
             data: Dict
    ) -> Dict:
        """Post data into an endpoint.
        
        :args:
            endpoint: string with the url to request
            data: json object to send

        :returns:
            dict with response data.

        :raises:
            HttpError
        """
        url = self.__create_url(endpoint)
        resp = None
        self.logger.info(f'Posting data to {url}')
        
        r = requests.post(url, json=data, auth=HTTPBasicAuth(self.token, 'x'))
        if r.status_code != 200 and r.status_code != 201:
            raise HttpError(str(r.text), r.status_code)

        # Success
        resp = r.json()
        self.logger.info('Data posted successfully.')
        self.logger.debug(f'{str(resp)[:200]}')

        # Return data
        return resp

    @classmethod
    def from_file(self, 
                  path: str
    ) -> ApiClient:
        '''Create a new object with configuration from a given file.

        It searchs for the configuration in yaml format:
            ``host`` -> host url
            ``port`` -> port number
            ``token`` -> token string

        All these values must be setted inside a ``api_client`` key.
        
        :args:
            path: string with file name.

        :returns:
            ApiClient object instance.

        :raises:
            FileNotFoundError
            ValueError
        '''
        import yaml

        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f'File {path} does not exist')

        with p.open('r') as f:
            data = yaml.load(f)

        api = data.get('api', None)
        if api is None:
            raise ValueError('Could not found "api" key in configuration file')

        obj = ApiClient(data.get('token', ''), data.get('host', 'localhost'), data.get('port', 5000))
        return obj
