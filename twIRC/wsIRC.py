import asyncio
import websockets
import re



class wsIRCTw:
    def __init__(self, channel, token, username, debug=False):
        self.channel = channel
        self.token = token
        self.debug = debug
        self.username = username

    async def join_server(self):
        uri = "wss://irc-ws.chat.twitch.tv:443"
        async with websockets.connect(uri) as websocket:
            await websocket.send("PASS oauth:{}".format(self.token))
            await websocket.send("NICK {}".format(self.username))
            await websocket.send("JOIN {}".format(self.channel))
            await websocket.send("CAP REQ :twitch.tv/membership")
            #await websocket.send("PRIVMSG sr_pixel_ :hola, soy un bot :D")
            while True:
                message = await websocket.recv()
                if self.debug == True:
                    print(message)
                userName = re.search(r'\:(.*?)\!', message)
                if userName:
                    userNick = userName.group(1)
                if message.find('PRIVMSG {}'.format(self.channel)) != -1:
                    chatMessage = message.partition('PRIVMSG {} :'.format(self.channel))[2].strip()
                    fullMSG = '{}: {}'.format(userNick, chatMessage)
                    print(fullMSG)
                if message == 'PING :tmi.twitch.tv':
                    websocket.send('PONG :tmi.twitch.tv')
    def run(self):
        asyncio.get_event_loop().run_until_complete(self.join_server())


