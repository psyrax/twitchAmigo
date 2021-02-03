from login import twLogin
from twIRC import wsIRC
import configparser
import asyncio

config = configparser.ConfigParser()
config.read('./config.ini')

twLogin = twLogin.TwitchLogin(config['twitch'])
twToken = twLogin.getToken()

print("opening IRC")
twIRCBot = wsIRC.wsIRCTw(
    token=config['twitch']['chat_token'],
    username='fritangatv', 
    channel='#followgrubby',
    debug=True
)

twIRCBot.run()
