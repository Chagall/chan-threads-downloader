import json
import os
import sys
from time import sleep
from timeit import default_timer as timer

import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils._1500_chan_boards import _1500boards
from utils.chan_html_parser import ChanHTMLParser
from utils.misc import print_execution_time


def get_all_boards_data(chan_name, tld):
    board_counter = 0

    print("Chan:", chan_name, "\nGetting boards")

    boards = get_available_boards(chan_name, tld)
    boards_count = len(boards)

    print(boards_count, " boards found")

    cookies = {"mc": "1"}

    for board in boards:
        thread_counter = 0
        board_id = board.get("id")

        print("Downloading data from board /", board_id, "/. Board: ", board_counter, " of ", boards_count)

        board["threads"] = get_board_threads(chan_name, tld, board_id, cookies)
        threads_count = len(board["threads"])

        print(threads_count, " threads found on board /", board_id)

        for thread in board["threads"]:
            if thread_counter % 20 == 0:
                print("Getting thread ", thread_counter)

            thread["replies"] = get_thread_replies(chan_name, tld, board_id, thread.get("id"), cookies)

            thread_counter += 1

        board_counter += 1

        save_board_data(chan_name, board_id, board)


def get_available_boards(chan_name, tld):
    # Como o 1500chan não oferece uma rota para pegar todas as boards,
    # vamos carregá-las a partir de um arquivo específico
    if chan_name == "1500chan":
        boards = []
        for board_data in _1500boards:
            boards.append(
                {
                    "id": board_data.get("name"),
                    "name": board_data.get("name"),
                    "description": board_data.get("description"),
                }
            )
        return boards

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

        for board_data in data:
            title = board_data.get("board").get("title") if board_data.get("board").get("title") != None else ""
            subtitle = (
                board_data.get("board").get("subtitle") if board_data.get("board").get("subtitle") != None else ""
            )
            description = title + ". " + subtitle

            boards.append(
                {
                    "id": board_data.get("board").get("uri"),
                    "name": board_data.get("board").get("uri"),
                    "description": description,
                }
            )
        return boards
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []


def get_board_threads(chan_name, tld, board_name, cookies):
    """
    chan_name: 8chan, 27chan, 4chan, etc.
    tld: top level domain (.org, .com, etc)
    board_id: b, anime, etc
    """
    url = f"https://{chan_name}{tld}/{board_name}/threads.json"

    response = requests.get(url, cookies=cookies)

    # Check if the request was successful
    if response.status_code == 200:
        pages = response.json()
        threads = []

        for page in pages:
            for thread in page.get("threads"):
                threads.append(
                    {
                        "id": thread.get("no"),
                    }
                )
        return threads
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []


def get_thread_replies(chan_name, tld, board_name, thread_id, cookies):
    """
    chan_name: 8chan, 27chan, 4chan, etc.
    tld: top level domain (.org, .com, etc)
    board_id: _id of the boards
    thread_id: postId from catalog.json
    """
    url = f"https://{chan_name}{tld}/{board_name}/res/{thread_id}.json"

    response = requests.get(url, cookies=cookies)

    if chan_name != "1500chan":
        sleep(5)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        replies = []
        parser = ChanHTMLParser()

        for reply in data.get("posts"):
            if reply.get("com") != None:
                parser.feed(reply.get("com"))
                parsed_message = parser.get_parsed_text()

                if parsed_message != "":
                    replies.append({"id": reply.get("no"), "message": parsed_message})
            # Limpe o parser
            parser.clear()

        return replies
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []


def save_board_data(chan_name, board_id, board_data):
    os.makedirs(f"{chan_name}/list/", exist_ok=True)

    with open(f"{chan_name}/list/{board_id}.json", "w", encoding="utf-8") as file:
        json.dump(board_data, file, ensure_ascii=False, indent=4)


chans = [{"name": "1500chan", "tld": ".org"}, {"name": "magalichan", "tld": ".com"}]

start_time = timer()

for chan in chans:
    get_all_boards_data(chan.get("name"), chan.get("tld"))

end_time = timer()

total_time = end_time - start_time

print_execution_time(start_time, end_time)
