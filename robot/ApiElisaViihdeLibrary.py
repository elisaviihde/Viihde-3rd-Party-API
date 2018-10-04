import logging

import requests


class ApiElisaViihdeLibrary(object):

    base_url_api_viihde               = 'https://api-viihde-gateway.dc1.elisa.fi'

    external_client_id                = 'external'
    external_client_secret            = 'nZhkFGz8Zd8w'
    external_api_key                  = 'GetThisFromElisa'

    metadata_query_param              = 'programId,channel,suggestedFolderNames,suggestedWildcardRules,recordable,id,name,status,startTime,endTime,startTimeUTC,lengthMinutes,isPopular,shortDescription,thumbnailUrl,thumbnails,genres,showtype,images,series,credits,starRating,contentRating,ageLimit'

    #############
    # OAuth
    #############

    def get_authcode_from_oauth(self):
        payload = {"client_id": self.external_client_id, "client_secret": self.external_client_secret, "response_type": "code", "scopes": []}
        headers = {'content-type': 'application/json','apikey': self.external_api_key}
        logging.debug(headers)
        response = requests.post("{}/auth/authorize/access-code".format(self.base_url_api_viihde), json=payload, headers=headers)
        logging.debug(response.text)
        response.raise_for_status()
        data = Data(response.json())
        return data.code

    def get_oauth_token_for_user_with_password_and_code(self, username, password, code):
        payload = {'grant_type':'authorization_code','username': username, 'password':password,"client_id": self.external_client_id, "code": code}
        headers = {'content-type': 'application/x-www-form-urlencoded', 'apikey': self.external_api_key}
        response = requests.post("{}/auth/authorize/access-token".format(self.base_url_api_viihde), data=payload, headers=headers)
        logging.debug(response.text)
        response.raise_for_status()
        return Data(response.json())

    def get_oauth_token_for_user_with_refresh_token(self, refresh_token):
        payload = {'grant_type':'refresh_token',"client_id": self.external_client_id, "client_secret": self.junction_client_secret, "refresh_token": refresh_token}
        headers = {'Authorization': 'Bearer '+ refresh_token, 'apikey': self.external_api_key}
        response = requests.post("{}/auth/authorize/access-token".format(self.base_url_api_viihde), data=payload, headers=headers)
        logging.debug(response.text)
        response.raise_for_status()
        return Data(response.json())

    #############
    # Recordings
    #############

    def get_all_recordings(self, token, platform, app_version):
        headers = {'Authorization': 'Bearer '+ token, 'apikey': self.external_api_key}
        logging.debug(headers)
        response = requests.get("{}/rest/npvr/recordings/all?v=2.1&platform={}&appVersion={}".format(self.base_url_api_viihde,platform,app_version), headers=headers)
        logging.debug(response.text)
        response.raise_for_status()
        return response.json()

    def get_recording_with_metadata(self, token, program_id, include_metadata, platform, app_version):
        headers = {'Authorization': 'Bearer '+ token, 'apikey': self.external_api_key}
        logging.debug(headers)
        response = requests.get("{}/rest/npvr/recordings/info/{}?v=2.1&platform={}&appVersion={}&includeMetadata={}".format(self.base_url_api_viihde, program_id, platform, app_version, include_metadata), headers=headers)
        logging.debug(response.text)
        response.raise_for_status()
        return Data(response.json())

    def get_recording_url(self, token, program_id, platform, app_version):
        headers = {'Authorization': 'Bearer '+ token, 'apikey': self.external_api_key}
        logging.debug(headers)
        response = requests.get("{}/rest/npvr/recordings/url/{}?v=2.1&platform={}&appVersion={}".format(self.base_url_api_viihde, program_id, platform, app_version), headers=headers)
        logging.debug(response.text)
        response.raise_for_status()
        return response.json()

    #############
    # EPG
    #############

    def get_all_channels(self, token, platform, app_version):
        headers = {'Authorization': 'Bearer '+ token, 'apikey': self.external_api_key}
        logging.debug(headers)
        response = requests.get("{}/rest/epg/channels?platform={}&appVersion={}".format(self.base_url_api_viihde, platform, app_version), headers=headers)
        logging.debug(response.text)
        response.raise_for_status()
        return Data(response.json())

    def get_schedule_for_channel_with_metadata(self, token, channel_id, platform, app_version):
        headers = {'Authorization': 'Bearer '+ token, 'apikey': self.external_api_key}
        logging.debug(headers)
        response = requests.get("{}/rest/epg/schedule?channelId={}&platform={}&appVersion={}&includeField={}".format(self.base_url_api_viihde, channel_id, platform, app_version, self.metadata_query_param), headers=headers, stream=True)
        logging.debug(response.text)
        response.raise_for_status()
        return Data(response.json())

    def get_program_with_metadata(self, token, program_id, platform, app_version):
        headers = {'Authorization': 'Bearer '+ token, 'apikey': self.external_api_key}
        logging.debug(headers)
        response = requests.get("{}/rest/epg/program/{}/?platform={}&appVersion={}&includeField={}".format(self.base_url_api_viihde, program_id, platform, app_version, self.metadata_query_param), headers=headers, stream=True)
        logging.debug(response.text)
        response.raise_for_status()
        return Data(response.json())

    #############
    # Search
    #############

    def do_search_for_user(self, token, search_string, include_metadata, platform):
        headers = {'Authorization': 'Bearer '+ token, 'apikey': self.external_api_key}
        logging.debug(headers)
        response = requests.get("{}/rest/search/query?q={}&includeMetadata={}&platform={}".format(self.base_url_api_viihde, search_string, include_metadata, platform), headers=headers)
        logging.debug(response.text)
        response.raise_for_status()
        return response.json()


class Data(object):

    def __init__(self, data):
        data = {key: Data(value) if isinstance(value, dict) else value
                for key, value in data.items()}
        self.__dict__.update(data)
