from signalr_aio import Connection
import json

def process_message(message):
    return json.loads(message)

# Create debug message handler.
async def on_debug(**msg):
    #print(msg)
    # In case of 'queryExchangeState'
    if 'R' in msg and type(msg['R']) is not bool:
        #decoded_msg = process_message(msg['R'])
        with open("result.json", "w") as f:
            json.dump(msg, f)
        print("DEBUG")

# Create error handler
async def on_error(msg):
    print("ERROR")


# Create hub message handler
async def on_message(msg):
    #decoded_msg = process_message(msg[0])
    with open("record_race.json", "a") as f:
        json.dump(msg, f)
    print("MESSAGE")

if __name__ == "__main__":
    # Create connection
    # Users can optionally pass a session object to the client, e.g a cfscrape session to bypass cloudflare.
    connection = Connection('https://livetiming.formula1.com/signalr', session=None)

    # Register hub
    hub = connection.register_hub('streaming')

    # Assign debug message handler. It streams unfiltered data, uncomment it to test.
    connection.received += on_debug

    # Assign error handler
    connection.error += on_error

    # Assign hub message handler
    hub.client.on('feed', on_message)
    hub.client.on('log', on_message)
    hub.client.on('StreamStatus', on_message)

    # Send a message
    hub.server.invoke('Subscribe', ["SPFeed", "ExtrapolatedClock", "StreamingStatus"])

    # Start the client
    connection.start()