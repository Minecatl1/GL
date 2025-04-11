import os
import json

def list_games(directory, file_extensions):
    games = []
    
    # Debugging: Print the directory being scanned
    print(f"Scanning directory: {directory}")
    
    for root, _, files in os.walk(directory):
        for file in files:
            # Debugging: Print each file being considered
            print(f"Found file: {file}")
            
            if file.endswith(tuple(file_extensions)):
                game_path = os.path.join(root, file)
                game_name = os.path.splitext(file)[0]
                game_type = file.split('.')[-1]
                icon_path = os.path.join(root, 'icon.png') if os.path.exists(os.path.join(root, "icon.png")) else None
                
                # Debugging: Print the game details being added
                print(f"Adding game: {game_name}, Type: {game_type}, Path: {game_path}, Icon: {icon_path}")
                
                games.append({
                    "name": game_name,
                    "type": game_type,
                    "path": game_path,
                    "icon": icon_path
                })
                
    # Debugging: Print the total number of games found
    print(f"Total games found in {directory}: {len(games)}")
    
    return games

def main():
    # Directories to scan
    games_dir = 'Games'
    roms_dir = os.path.join(games_dir, 'roms')  # Roms subdirectory inside Games

    # Supported file extensions for games
    html5_extensions = ['.html']  # HTML5 games (skip .js files)
    rom_extensions = ['.nes', '.snes', '.gba', '.gb', '.gen', '.bin']  # ROM files

    all_games = []

    # Scan for HTML5 games in the Games directory
    print("Scanning for HTML5 games...")
    all_games.extend(list_games(games_dir, html5_extensions))

    # Scan for ROMs in the roms subdirectory
    print("Scanning for ROMs...")
    if os.path.exists(roms_dir):
        all_games.extend(list_games(roms_dir, rom_extensions))

    # Debugging: Print the total number of games in the combined list
    print(f"Total games in combined list: {len(all_games)}")

    # Write to game_list.json
    with open('game_list.json', 'w') as file:
        json.dump(all_games, file, indent=4)
        
    # Debugging: Confirm that the JSON has been written
    print("game_list.json has been successfully written with the game data.")

if __name__ == '__main__':
    main()
