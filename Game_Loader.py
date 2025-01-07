import os
import json
import webbrowser
from PIL import Image
import subprocess

def list_games(directory, file_extensions):
    games = []
    for game_dir in os.listdir(directory):
        game_path = os.path.join(directory, game_dir)
        if os.path.isdir(game_path) and game_dir not in ["WebGames", "NESGames"]:
            for file in os.listdir(game_path):
                if file.endswith(tuple(file_extensions)):
                    games.append({
                        "name": game_dir,
                        "type": file.split('.')[-1],
                        "path": os.path.join(game_path, file),
                        "icon": os.path.join(game_path, "Icon.png")
                    })
    return games

def list_web_games(directory):
    web_games = []
    for web_game_file in os.listdir(directory):
        if web_game_file.endswith(".txt"):
            with open(os.path.join(directory, web_game_file), "r") as file:
                name = file.readline().strip()
                url = file.readline().strip()
                web_games.append({
                    "name": name,
                    "type": "web",
                    "url": url
                })
    return web_games

def list_nes_games(directory):
    nes_games = []
    for nes_game_file in os.listdir(directory):
        if nes_game_file.endswith(".nes"):
            nes_games.append({
                "name": os.path.splitext(nes_game_file)[0],
                "type": "nes",
                "path": os.path.join(directory, nes_game_file)
            })
    return nes_games

def scan_external_storage(file_extensions):
    external_drives = [f"/mnt/{d}" for d in os.listdir("/mnt") if os.path.isdir(f"/mnt/{d}")]
    found_games = []

    for drive in external_drives:
        for root, dirs, files in os.walk(drive):
            for file in files:
                if file.endswith(tuple(file_extensions)):
                    found_games.append({
                        "path": os.path.join(root, file),
                        "type": file.split('.')[-1]
                    })
    return found_games

def save_games_to_json(games, filename="game_list.json"):
    with open(filename, "w") as file:
        json.dump(games, file, indent=4)

def main():
    games_dir = "Games"
    web_games_dir = os.path.join(games_dir, "WebGames")
    nes_games_dir = os.path.join(games_dir, "NESGames")

    games = list_games(games_dir, ["py", "html"])
    web_games = list_web_games(web_games_dir)
    nes_games = list_nes_games(nes_games_dir)
    
    all_games = games + web_games + nes_games

    while True:
        choice = input("Do you want to scan external storage for games? (y/n): ").strip().lower()
        if choice == 'y':
            found_games = scan_external_storage(["py", "html", "nes"])
            if found_games:
                for game in found_games:
                    print(f"Found game: {game['path']}")
                    add_choice = input("Do you want to add this game to the list? (y/n): ").strip().lower()
                    if add_choice == 'y':
                        game_name = input("Enter the name of the game: ").strip()
                        icon_path = input("Enter the path to the icon: ").strip()
                        game["name"] = game_name
                        game["icon"] = icon_path
                        all_games.append(game)
            else:
                print("No games found on external storage.")
        else:
            break
    
    save_games_to_json(all_games)

    # Optional: automatically open the HTML interface
    webbrowser.open("index.html")

if __name__ == "__main__":
    main()
