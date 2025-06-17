import os
import json
import glob
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent
GAMES_DIR = BASE_DIR / "Games"
HTML5_DIR = GAMES_DIR / "html5"
ROMS_DIR = GAMES_DIR / "roms"
OUTPUT_JSON = BASE_DIR / "game_list.json"

# Supported ROM extensions mapped to emulator cores
ROM_CORES = {
    ".nes": "nes", ".smc": "snes", ".sfc": "snes", ".gba": "gba",
    ".gb": "gb", ".gbc": "gb", ".md": "genesis", ".gen": "genesis"
}

# Preferred icon filenames (in order of priority)
ICON_PRIORITY = ["icon.png", "logo.png", "cover.jpg", "thumbnail.png", "icon.jpg"]

def find_icon(game_path):
    """Find matching icon file in the game's own directory"""
    game_dir = Path(game_path).parent
    
    # Check for preferred filenames first
    for icon_name in ICON_PRIORITY:
        icon_path = game_dir / icon_name
        if icon_path.exists():
            return str(icon_path.relative_to(BASE_DIR)).replace("\\", "/")
    
    # Fallback: search for any image file in the game directory
    image_exts = ("*.png", "*.jpg", "*.jpeg", "*.svg", "*.gif")
    for ext in image_exts:
        for img_path in glob.glob(str(game_dir / ext)):
            return str(Path(img_path).relative_to(BASE_DIR)).replace("\\", "/")
    
    # Final fallback: default icon
    return "icons/default.png"

def scan_html5_games():
    """Scan HTML5 games directory using folder names for game names"""
    games = []
    for game_dir in HTML5_DIR.iterdir():
        if not game_dir.is_dir():
            continue
            
        # Check for entry point files
        entry_points = ["index.html", "game.html", "main.html", "start.html"]
        for entry in entry_points:
            if (game_dir / entry).exists():
                game_name = game_dir.name
                game_path = f"Games/html5/{game_name}/{entry}"
                
                games.append({
                    "name": format_name(game_name),  # Use folder name for display
                    "type": "html5",
                    "path": game_path,
                    "icon": find_icon(game_path)
                })
                break
    return games

def scan_roms():
    """Scan ROMs directory using filename for game names"""
    roms = []
    for system_dir in ROMS_DIR.iterdir():
        if not system_dir.is_dir():
            continue
            
        # Recursively scan for ROMs in system directories
        for rom_file in system_dir.rglob("*.*"):
            if not rom_file.is_file():
                continue
                
            ext = rom_file.suffix.lower()
            if ext not in ROM_CORES:
                continue
                
            # Create relative path from base directory
            rel_path = rom_file.relative_to(GAMES_DIR)
            game_path = f"Games/{rel_path}"
            
            roms.append({
                "name": format_name(rom_file.stem),
                "type": "rom",
                "path": game_path,
                "icon": find_icon(game_path),
                "core": ROM_CORES[ext]
            })
    return roms

def format_name(raw_name):
    """Convert filename/folder name to readable game name"""
    # Replace underscores and hyphens with spaces
    name = raw_name.replace("_", " ").replace("-", " ").title()
    
    # Common abbreviations to expand
    abbreviations = {
        "Gba": "GBA", "Snes": "SNES", "Nes": "NES", "Gb": "GB",
        "Iii": "III", "Ii": "II", "Iv": "IV", "Rpg": "RPG",
        "Hd": "HD", "3d": "3D", "Remastered": "Remastered"
    }
    
    # Special case handling for Roman numerals
    roman_numerals = {
        " I ": " I ", " II ": " II ", " III ": " III ", " IV ": " IV ",
        " V ": " V ", " VI ": " VI ", " VII ": " VII ", " VIII ": " VIII "
    }
    
    # Process abbreviations
    for abbr, full in abbreviations.items():
        name = name.replace(f" {abbr} ", f" {full} ")
        if name.endswith(f" {abbr}"):
            name = name[:-len(abbr)] + full
    
    # Handle Roman numerals
    for numeral, formatted in roman_numerals.items():
        name = name.replace(numeral.lower(), formatted)
    
    # Remove file extensions from name
    if "." in name:
        name = name.split(".")[0]
    
    return name

def generate_game_list():
    """Generate combined game list JSON"""
    html5_games = scan_html5_games()
    rom_games = scan_roms()
    all_games = html5_games + rom_games
    
    # Sort alphabetically
    all_games.sort(key=lambda x: x["name"])
    
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_games, f, indent=2, ensure_ascii=False)
        
    print(f"Generated game list with {len(all_games)} entries")
    print(f"- HTML5 games: {len(html5_games)}")
    print(f"- ROMs: {len(rom_games)}")
    print(f"Output saved to: {OUTPUT_JSON}")

if __name__ == "__main__":
    # Create directories if missing
    HTML5_DIR.mkdir(parents=True, exist_ok=True)
    ROMS_DIR.mkdir(parents=True, exist_ok=True)
    
    generate_game_list()
