import os
import json

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
        if nes_game_file.endswith(".NES"):
            nes_games.append({
                "name": os.path.splitext(nes_game_file)[0],
                "type": "nes",
                "path": os.path.join(directory, nes_game_file)
            })
    return nes_games

def main():
    games_dir = "Games"
    web_games_dir = os.path.join(games_dir, "WebGames")
    nes_games_dir = os.path.join(games_dir, "NESGames")

    games = list_games(games_dir, ["py", "html"])
    web_games = list_web_games(web_games_dir)
    nes_games = list_nes_games(nes_games_dir)

    all_games = games + web_games + nes_games

    with open("game_list.json", "w") as file:
        json.dump(all_games, file, indent=4)

if __name__ == "__main__":
    main()
