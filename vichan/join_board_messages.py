import glob
import json
from timeit import default_timer as timer

start_time = timer()

folders = ["magalichan", "1500chan"]

for folder in folders:
    posts = []
    folder_path = f"{folder}/list"
    final_file_path = f"{folder}/{folder}.json"

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

    # Open the file in write mode and save the JSON data
    with open(final_file_path, "w", encoding="utf-8") as file:
        json.dump(posts, file, ensure_ascii=False, indent=4)

end_time = timer()
elapsed_time = end_time - start_time

print(f"Conversão durou: {elapsed_time} segundos")
