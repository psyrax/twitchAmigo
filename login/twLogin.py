import requests
class TwitchLogin:
    def __init__(self, config):
        self.clientID = config['client_id']
        self.clientSecret = config['client_secret']
    
    def getToken(self):
        tokenUrl = 'https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials&scope=chat:read'.format(
            self.clientID, self.clientSecret)
        tokenRequest = requests.post(tokenUrl).json()
        try:
            accessToken = tokenRequest['access_token']
        except:
            accessToken = None
        return accessToken
