import requests
import datetime
import sys
import RPi.GPIO as GPIO
import tm1637
import time 

#CLK -> GPIO23 (Pin 16)
#DI0 -> GPIO24 (Pin 18)
client_id = ''
client_secret = ''

tokenUrl = 'https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials'.format(client_id, client_secret)
tokenRequest = requests.post(tokenUrl).json()
accessToken = tokenRequest['access_token']

### Example followgrubby id = 20992865
url = 'https://api.twitch.tv/helix/search/channels?query=followgrubby'
headers = {
    'Client-id': client_id,
    'Authorization': 'Bearer {}'.format(accessToken)
}
r = requests.get(url, headers=headers).json()
channelID = '20992865'
channelUrl = 'https://api.twitch.tv/helix/channels?broadcaster_id={}'.format(channelID)
channelRequest = requests.get(channelUrl, headers=headers).json()
def getStreamTime(stream, headers):
    streamUrl = 'https://api.twitch.tv/helix/streams'
    streamParams = {
        'user_login': stream,
        'first': 5
    }
    streamRequest = requests.get(streamUrl, 
    params=streamParams, 
    headers=headers).json()
    streamData = streamRequest['data'][0]
    streamStarted = streamData['started_at']
    streamDateStarted = datetime.datetime.strptime(
        streamStarted, '%Y-%m-%dT%H:%M:%SZ')
    now = datetime.datetime.utcnow()
    currentStreamTime = now - streamDateStarted
    timeComponents = str(currentStreamTime).split(':')
    timeString = '{}{}'.format(timeComponents[0].zfill(2), timeComponents[1])
    timeList = [int(timeString[0]),  int(timeString[1]),
                int(timeString[2]),  int(timeString[3])]
    return timeList


Display = tm1637.TM1637(23, 24, tm1637.BRIGHT_TYPICAL)
Display.Clear()
Display.SetBrightnes(1)

while(True):
    streamTime = getStreamTime('jimrsng', headers)
    Display.Show(streamTime)
    Display.ShowDoublepoint(True)
    time.sleep(10)
