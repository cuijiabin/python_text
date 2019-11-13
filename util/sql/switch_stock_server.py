import requests


def server_switch():
    for url in ["http://10.5.105.112:9089/stock/serverSwitch", "http://10.5.105.104:9089/stock/serverSwitch",
                "http://10.5.109.12:9089/stock/serverSwitch"]:
        r = requests.get(url)
        print(r.content.decode("utf-8"))


def open_switch():
    for url in ["http://10.5.105.112:9089/stock/openSwitch", "http://10.5.105.104:9089/stock/openSwitch",
                "http://10.5.109.12:9089/stock/openSwitch"]:
        r = requests.get(url)
        print(r.content.decode("utf-8"))


def close_switch():
    for url in ["http://10.5.105.112:9089/stock/closeSwitch", "http://10.5.105.104:9089/stock/closeSwitch",
                "http://10.5.109.12:9089/stock/closeSwitch"]:
        r = requests.get(url)
        print(r.content.decode("utf-8"))


if __name__ == '__main__':
    server_switch()
