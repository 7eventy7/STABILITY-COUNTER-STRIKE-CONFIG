import os
import platform
from pathlib import Path
from urllib.request import urlopen

GITHUB_REPO_URL = "https://github.com/7eventy7/STABILITY-COUNTER-STRIKE-CONFIG"
AUTOEXEC_URL = f"{GITHUB_REPO_URL}/raw/main/autoexec.cfg"

def display_startup_screen():
    print("=" * 70)
    print(" " * 15 + "STABILITY-COUNTER-STRIKE-CONFIG INSTALLER")
    print("=" * 70)
    print(" " * 25 + "v1.0.0 -- July 29, 2024")
    print("=" * 70)
    print("\nThis script will help you install the Stability Counter-Strike Config.")
    print("Please follow the instructions as prompted.\n")
    print("=" * 70 + "\n")

def find_cs_install_directory():
    possible_paths = []
    system = platform.system()
    
    if system == "Windows":
        for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            drive_path = Path(f"{drive}:")
            if drive_path.exists():
                possible_paths.extend([
                    drive_path / "Program Files (x86)" / "Steam" / "steamapps" / "common" / "Counter-Strike Global Offensive" / "game" / "csgo" / "cfg",
                    drive_path / "steam" / "steamapps" / "common" / "Counter-Strike Global Offensive" / "game" / "csgo" / "cfg"
                ])
                steam_path = next((Path(root) / "steamapps" / "common" / "Counter-Strike Global Offensive" / "game" / "csgo" / "cfg" 
                                   for root, dirs, _ in os.walk(drive_path) if "steamapps" in dirs), None)
                if steam_path:
                    possible_paths.append(steam_path)
    elif system == "Darwin":  # macOS
        possible_paths.append(Path.home() / "Library" / "Application Support" / "Steam" / "steamapps" / "common" / "Counter-Strike Global Offensive" / "game" / "csgo" / "cfg")
    elif system == "Linux":
        possible_paths.extend([
            Path.home() / ".steam" / "steam" / "steamapps" / "common" / "Counter-Strike Global Offensive" / "game" / "csgo" / "cfg",
            Path.home() / ".local" / "share" / "Steam" / "steamapps" / "common" / "Counter-Strike Global Offensive" / "game" / "csgo" / "cfg"
        ])

    for path in possible_paths:
        if path.exists():
            print(f"Counter-Strike install directory found:\n\"{path}\"\n")
            return path

    raise FileNotFoundError("Counter-Strike install directory not found in any of the steamapps directories")

def download_autoexec(url):
    with urlopen(url) as response:
        if response.status != 200:
            raise Exception(f"Failed to download file: {response.reason}")
        return response.read().decode('utf-8')

def get_valid_input(prompt, valid_check, error_message):
    while True:
        user_input = input(prompt).strip()
        if valid_check(user_input):
            return user_input
        print(error_message)

def customize_config(config_content):
    print("\nCustomization Options:")
    
    # FPS Limit
    fps_limit = get_valid_input(
        "\n1. What is your desired fps limit? (0-1000, 0 for unlimited): ",
        lambda x: x.isdigit() and 0 <= int(x) <= 1000,
        "Invalid input. Please enter a number between 0 and 1000."
    )
    config_content = config_content.replace('fps_max "0"', f'fps_max "{fps_limit}"')

    # Menu FPS Limit
    menu_fps_limit = get_valid_input(
        "\n2. What is your desired menu fps limit? (0-1000, 0 for unlimited): ",
        lambda x: x.isdigit() and 0 <= int(x) <= 1000,
        "Invalid input. Please enter a number between 0 and 1000."
    )
    config_content = config_content.replace('fps_max_ui "180"', f'fps_max_ui "{menu_fps_limit}"')

    # Zoom Sensitivity Ratio
    disable_zoom_ratio = get_valid_input(
        "\n3. Disable accurate zoom ratio for scoped weapons? (yes/no): ",
        lambda x: x.lower() in ['yes', 'no', 'y', 'n'],
        "Invalid input. Please enter 'yes' or 'no'."
    )
    if disable_zoom_ratio.lower() in ['yes', 'y']:
        config_content = config_content.replace('zoom_sensitivity_ratio "0.818933027098955175"', 'zoom_sensitivity_ratio "1"')

    # Toggle Quick Recoil Bind
    remove_recoil_bind = get_valid_input(
        "\n4. Remove the toggle quick recoil bind? (yes/no): ",
        lambda x: x.lower() in ['yes', 'no', 'y', 'n'],
        "Invalid input. Please enter 'yes' or 'no'."
    )
    if remove_recoil_bind.lower() in ['yes', 'y']:
        start_index = config_content.find("// TOGGLE STATIC & RECOIL CROSSHAIR BIND")
        end_index = config_content.find("//--------------------------------------------------------------------------------------------------------", start_index)
        if start_index != -1 and end_index != -1:
            config_content = config_content[:start_index] + config_content[end_index:]

    return config_content

def save_config(content, destination):
    with open(destination, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\nSaved customized autoexec.cfg to:\n\"{destination}\"\n")

def main():
    display_startup_screen()
    
    try:
        cs_cfg_path = find_cs_install_directory()
        autoexec_path = cs_cfg_path / "autoexec.cfg"
        
        config_content = download_autoexec(AUTOEXEC_URL)
        customized_content = customize_config(config_content)
        save_config(customized_content, autoexec_path)
        
        print("=" * 70)
        print(" " * 22 + "INSTALLATION SUCCESSFUL!")
        print("=" * 70)
        print(f"\nThe Stability Counter-Strike Config has been successfully installed and customized at:\n\"{autoexec_path}\".")
        print("\nThank you for choosing to use this configuration!\n")
        print("=" * 70)

        input("Press any button to exit...")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()