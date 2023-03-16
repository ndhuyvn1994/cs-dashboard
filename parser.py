"""
Standalone program
Receive request from hlds server, parse log and store to Redis
"""

import re
import redis
import socket

from constant import *

rd = redis.Redis(decode_responses=True)

# event_name, regex, extract_field_name, key_index, value_index, custom_value
PARSERS = [
    # L 03/09/2023 - 14:16:04: "CSC| Player<6><STEAM_0:0:201391372><>" connected, address "106.104.77.151:53449"
    (
        "player_connected", r'"(.+)<.+><.+><>" connected, address "(.+):(.+)"',
        0,
        {'ip': 1, 'port': 2},
        {'online': 1, 'is_join_game': 0}
    ),

    # L 03/08/2023 - 16:03:52: "ThongCaTheGioi<1><STEAM_0:0:94837813><>" entered the game
    (
        "player_joined_game",
        r'"(.+)<.+><.+><>" entered the game',
        0,
        {},
        {'is_join_game': 1}
    ),

    # L 03/08/2023 - 16:03:55: "ThongCaTheGioi<1><STEAM_0:0:94837813><>" joined team "TERRORIST"
    (
        "player_joined_team",
        r'"(.+)<.+><.+><>" joined team "(.+)"',
        0,
        {'team': 1},
        {'is_join_game': 1}
    ),

    # L 03/09/2023 - 14:42:26: "MrDonkey<3><STEAM_0:0:245202777><CT>" disconnected
    (
        "player_disconnected",
        r'"(.+)<.+><.+><.*>" disconnected',
        0,
        {},
        {'is_join_game': 0, 'team': '', 'online': 0}
    ),
]


def parse(data):
    print(type(data))
    for parser in PARSERS:
        event_name, regex, key_id, dict_template, custom_values = parser
        match = re.findall(regex, data)
        if not match:
            continue

        update_dict = {key: match[0][index] for key, index in dict_template.items()}
        update_dict.update(custom_values)

        print(update_dict)
        key = f"{match[0][key_id]}"
        rd.hset(key, mapping=update_dict)

        # keep track of online players
        if event_name == "player_connected":
            rd.sadd(RD_ONLINE_KEY, key)
        if event_name == "player_disconnected":
            rd.srem(RD_ONLINE_KEY, key)

        return


if __name__ == "__main__":
    UDP_IP = "127.0.0.1"
    UDP_PORT = 9999

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print(f"received raw message: {data}")
        parse(str(data))
