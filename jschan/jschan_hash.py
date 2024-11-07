import json
import os
import sys

import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.chan_html_parser import ChanHTMLParser


def get_all_boards_data(chan_name, tld):
    board_counter = 0

    print("Chan:", chan_name, "\nGetting boards")

    boards = get_available_boards(chan_name, tld)
    boards_count = len(boards)

    print(boards_count, " boards found")

    for board in boards:
        thread_counter = 0
        board_id = board.get("_id")

        print("Downloading data from board: /", board_id, "/. Board: ", board_counter, " of ", boards_count)

        board["threads"] = get_board_threads_hash(chan_name, tld, board_id)
        threads_count = len(board["threads"])

        print(threads_count, "threads found on board /", board_id)

        for thread_id in board["threads"]:
            if thread_counter % 20 == 0:
                print("Getting thread ", thread_counter)

            board["threads"][thread_id] = get_thread_replies_hash(chan_name, tld, board_id, thread_id)

            thread_counter += 1

        board_counter += 1

        save_board_data(chan_name, board_id, board)


def get_available_boards(chan_name, tld):
    """
    chan_name: 8chan, 27chan, 4chan, etc.
    tld: top level domain (.org, .com, etc)
    """
    url = f"https://{chan_name}{tld}/boards.json"

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        boards = []

        for board_data in data.get("boards"):
            boards.append(
                {
                    "_id": board_data.get("_id"),
                    "name": board_data.get("settings").get("name"),
                    "description": board_data.get("settings").get("description"),
                }
            )
        return boards
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []


def get_board_threads_hash(chan_name, tld, board_id):
    """
    chan_name: 8chan, 27chan, 4chan, etc.
    tld: top level domain (.org, .com, etc)
    board_id: _id of the boards
    """
    url = f"https://{chan_name}{tld}/{board_id}/catalog.json"

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        threads = {}

        for thread_data in data:
            threads[str(thread_data.get("postId"))] = {"replies": {}}
        return threads
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return {}


def get_thread_replies_hash(chan_name, tld, board_id, thread_id):
    """
    chan_name: 8chan, 27chan, 4chan, etc.
    tld: top level domain (.org, .com, etc)
    board_id: _id of the boards
    thread_id: postId from catalog.json
    """
    url = f"https://{chan_name}{tld}/{board_id}/thread/{thread_id}.json"

    response = requests.get(url)

    # Only proceed if the request was successful
    if response.status_code == 200:
        thread = response.json()
        replies = {}
        parser = ChanHTMLParser()
        # The first reply in the thread is contained in the thread data itself
        # Only save messages where nomarkup is not null (It isn't a post with only images)
        if thread.get("nomarkup") != None and thread.get("nomarkup") != "":
            parser.feed(thread.get("nomarkup"))
            parsed_message = parser.get_parsed_text()

            if parsed_message != "":
                replies[str(thread.get("postId"))] = {"message": parsed_message}
            # Limpe o parser
            parser.clear()

        # Agora pegamos as respostas
        for reply in thread.get("replies"):
            if reply.get("nomarkup") != None and reply.get("nomarkup") != "":
                parser.feed(reply.get("nomarkup"))
                parsed_message = parser.get_parsed_text()

                if parsed_message != "":
                    replies[str(reply.get("postId"))] = {"message": parsed_message}
            # Limpe o parser
            parser.clear()

        return replies
    else:
        print(f"Failed to retrieve thread: {response.status_code}")
        return {}


def save_board_data(chan_name, board_id, board_data):
    os.makedirs(f"{chan_name}/hash/", exist_ok=True)

    with open(f"{chan_name}/hash/{board_id}.json", "w", encoding="utf-8") as file:
        json.dump(board_data, file, ensure_ascii=False, indent=4)


chans = [{"name": "bostilchan", "tld": ".org"}, {"name": "27chan", "tld": ".org"}]

for chan in chans:
    get_all_boards_data(chan.get("name"), chan.get("tld"))
