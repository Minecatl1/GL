import os
import json
import webbrowser
from PIL import Image
import subprocess

def list_games(directory, file_extensions):
    games = []
    for game_dir in os.listdir(directory):
        game_path = os.path.join(directory, game_dir)
        if os.path.isdir(game_path) and game_dir not in ["roms"]:
            for file in os.listdir(game_path):
                if file.endswith(tuple(file_extensions)):
                    games.append({
                        "name": game_dir,
                        "type": file.split('.')[-1],
                        "path": os.path.join(game_path, file),
                        "icon": os.path.join(game_path, "Icon.png")
                    })
    return games

def list_rom_games(directory):
    rom_games = []
    rom_path = os.path.join(directory, "roms")
    for rom_file in os.listdir(rom_path):
        if rom_file.endswith((".nes", ".xci", ".wbfs", ".rvz")):
            rom_games.append({
                "name": os.path.splitext(rom_file)[0],
                "type": rom_file.split('.')[-1],
                "path": os.path.join(rom_path, rom_file)
            })
    return rom_games

def list_web_games(directory):
    web_games = []
    web_games_dir = os.path.join(directory, "WebGames")
    for web_game_file in os.listdir(web_games_dir):
        if web_game_file.endswith(".txt"):
            with open(os.path.join(web_games_dir, web_game_file), "r") as file:
                name = file.readline().strip()
                url = file.readline().strip()
                web_games.append({
                    "name": name,
                    "type": "web",
                    "url": url
                })
    return web_games


def save_games_to_json(games, filename="game_list.json"):
    with open(filename, "w") as file:
        json.dump(games, file, indent=4)

def main():
    games_dir = "Games"
    roms_dir = os.path.join(games_dir, "roms")
    
    # Create the "roms" directory if it doesn't exist
    os.makedirs(roms_dir, exist_ok=True)
    
    # Move all files from NESGames, XCIGames, and Wiigames to "roms"
    for folder in ["NESGames", "XCIGames", "Wiigames"]:
        folder_path = os.path.join(games_dir, folder)
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    os.rename(file_path, os.path.join(roms_dir, file))
            os.rmdir(folder_path)

    games = list_games(games_dir, ["py", "html", "js"])  # Include JS files
    rom_games = list_rom_games(games_dir)
    web_games = list_web_games(games_dir)

    all_games = games + web_games + rom_games

    save_games_to_json(all_games)


if __name__ == "__main__":
    main()