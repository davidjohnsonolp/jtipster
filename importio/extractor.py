import json, importio, latch

connectors = { "fixture": "96d3ce37-cf25-40bf-85bb-078c63c706ba", "history": "02fa28de-1ae0-4ca5-9f6a-de03f7775c35" }

data = { "fixture": [], "history": [], "log": [] }

def extract(connector, urls):
    # To use an API key for authentication, use the following code:
    client = importio.importio(user_id="d133b9b6-1253-4568-b727-425c7181ed93",
                               api_key="xCSj76J7NK+PaXi5foAzbIjgyo+Y+Xpu1+oS+OpngOor8gYN/johObwTLAUaQSoGTGzmSCxVMJQU3mXbICU6SQ==",
                               host="https://query.import.io",
                               proxies={"http": "http://proxy.server:3128", "https":"http://proxy.server:3128"})

    client.connect()
    queryLatch = latch.latch(len(urls))

    def callback(query, message):
        global data

        # Disconnect messages happen if we disconnect the client library while a query is in progress
        if message["type"] == "DISCONNECT":
            data["log"].append("Query in progress when library disconnected")
            data["log"].append(json.dumps(message["data"], indent=4))

        # Check the message we receive actually has some data in it
        if message["type"] == "MESSAGE":
            if "errorType" in message["data"]:
                # In this case, we received a message, but it was an error from the external service
                data["log"].append("Got an error!")
                data["log"].append(json.dumps(message["data"], indent=4))
            else:
                # Save the data we got in our dataRows variable for later
                data[connector].extend(message["data"]["results"])

        # When the query is finished, countdown the latch so the program can continue when everything is done
        if query.finished(): queryLatch.countdown()

    for url in urls:
        client.query({ "connectorGuids": [ connectors[connector] ], "input": { "webpage/url": url }}, callback)

    data["log"].append("Queries dispatched, now waiting for results")

    queryLatch.await()

    data["log"].append("Latch has completed, all results returned")

    client.disconnect()

    # Now we can print out the data we got
    data["log"].append("All data received:")
    if connector == "fixture":
        for f in data[connector]:
            data["log"].append("%s vs %s" % (f["hometeam/_title"], f["awayteam/_title"]))
    elif connector == "history":
        data["log"].extend(urls)
    else:
        data["log"].append(json.dumps(data[connector], indent=4))

    return data[connector]

def reset_data(connector):
    data[connector] = []