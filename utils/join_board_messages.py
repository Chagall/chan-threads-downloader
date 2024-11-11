import glob
import json
from timeit import default_timer as timer

start_time = timer()

folders = ["../jschan/27chan", "../jschan/bostilchan", "../vichan/1500chan", "../vichan/magalichan"]

for folder in folders:
    posts = []
    folder_path = f"{folder}/list"
    chan_name = folder.split("/")[-1]
    final_file_path = f"{folder}/{chan_name}.json"

    print("Joining boards of", chan_name, "in a list")

    # List all JSON files in the folder
    for file_path in glob.glob(f"{folder_path}/*.json"):
        with open(file_path, "r") as board_file:
            try:
                board_data = json.load(board_file)
                for thread in board_data.get("threads"):
                    for reply in thread.get("replies"):
                        posts.append(reply.get("message"))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {file_path}: {e}")

    print("All boards of", chan_name, " have been joined")

    # Open the file in write mode and save the JSON data
    with open(final_file_path, "w", encoding="utf-8") as file:
        json.dump(posts, file, ensure_ascii=False, indent=4)

    print("List saved on:", final_file_path, "\n")

end_time = timer()
elapsed_time = end_time - start_time

print(f"Conversão durou: {elapsed_time} segundos")
