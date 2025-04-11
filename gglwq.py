import os
import json

def list_html_games(directory):
    games = []

    print(f"Scanning for HTML5 games in directory: {directory}")
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):  # Only consider .html files for HTML5 games
                game_name = os.path.basename(root).replace('-', ' ')  # Replace dashes with spaces
                game_path = os.path.join(root, file)
                icon_path = os.path.join(root, 'Icon.png') if os.path.exists(os.path.join(root, 'Icon.png')) else None

                print(f"Adding HTML5 game: {game_name}, Path: {game_path}, Icon: {icon_path}")

                games.append({
                    "name": game_name,
                    "type": "html",
                    "path": game_path,
                    "icon": icon_path
                })
                
    return games

def list_roms(directory):
    games = []

    print(f"Scanning for ROMs in directory: {directory}")

    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            rom_folder = os.path.join(root, dir_name)
            for file in os.listdir(rom_folder):
                if file.endswith(('.nes', '.snes', '.gba', '.gb', '.gen', '.bin')):  # Supported ROM extensions
                    game_name = dir_name.replace('-', ' ')  # Replace dashes with spaces
                    game_path = os.path.join(rom_folder, file)
                    icon_path = os.path.join(rom_folder, 'Icon.png') if os.path.exists(os.path.join(rom_folder, 'icon.png')) else None

                    print(f"Adding ROM: {game_name}, Path: {game_path}, Icon: {icon_path}")

                    games.append({
                        "name": game_name,
                        "type": file.split('.')[-1],  # Infer the ROM type from the file extension
                        "path": game_path,
                        "icon": icon_path
                    })
                
    return games

def main():
    games_dir = 'Games'
    roms_dir = os.path.join(games_dir, 'roms')  # Nested roms folder inside Games directory

    all_games = []

    # Scan for HTML5 games
    print("Scanning for HTML5 games...")
    all_games.extend(list_html_games(games_dir))

    # Scan for ROMs
    print("Scanning for ROMs...")
    if os.path.exists(roms_dir):
        all_games.extend(list_roms(roms_dir))

    # Write to game_list.json
    with open('game_list.json', 'w') as file:
        json.dump(all_games, file, indent=4)

    print("game_list.json has been successfully written with the game data.")

if __name__ == '__main__':
    main()
