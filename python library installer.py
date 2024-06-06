import subprocess

# Packages to be installed
packages = ['pytube', 'moviepy', 'pyppdf', 'wikipedia']

# Iterates over each package & installs if not already installed
for package in packages:
    try:
        # Checks if the package is already installed
        subprocess.check_call(['pip', 'show', package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{package} is already installed. Skipping...")
    except subprocess.CalledProcessError:
        # If not installed, install package
        print(f"Installing {package}...")
        subprocess.check_call(['pip', 'install', package])
        
# Author:
#                      .oooo.                   .ooo         .o   
#                     d8P'`Y8b                .88'         .d88   
#   oooo oooo    ooo 888    888 oooo    ooo  d88'        .d'888   
#    `88. `88.  .8'  888    888  `88b..8P'  d888P"Ybo. .d'  888   
#     `88..]88..8'   888    888    Y888'    Y88[   ]88 88ooo888oo 
#      `888'`888'    `88b  d88'  .o8"'88b   `Y88   88P      888   
#       `8'  `8'      `Y8bd8P'  o88'   888o  `88bod8'      o888o  
