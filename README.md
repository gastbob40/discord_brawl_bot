# Brawl Bot

![Discord](https://img.shields.io/badge/Discord-project-brightgreen)
![python](https://img.shields.io/badge/Language-Python-blueviolet)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## About

Brawl Bot is a discord bot for server moderation, and includes several points:
- Management of member Warns
- Management of member Mute
- Management of member Kicks
- Management of member Bans
- Management of clearing message
- All based on a configuration file
- ...

Brawl Bot is a project by [gastbob40](https://github.com/gastbob40).

## Requirements

You will need all these elements for the proper working of the project.

- [Python 3](https://www.python.org/downloads/)
- [A Discord Bot Token](https://discordapp.com/developers/applications/)


## Getting started

1. **First, you will have to clone the project.**

```shell
git clone https://github.com/gastbob40/discord_brawl_bot
```

2. **Create a `virtual environment`, in order to install dependencies locally.** For more information about virtual environments, [click here](https://docs.python.org/3/library/venv.html).

```shell
python -m venv .venv
```

3. **Activate the virtual environment**

Linux/macOS:

```shell
# Using bash/zsh
source .venv/bin/activate
# Using fish
. .venv/bin/activate.fish
# Using csh/tcsh
source .venv/bin/activate.csh
``` 

Windows:

```
# cmd.exe
.venv\Scripts\activate.bat
# PowerShell
.venv\Scripts\Activate.ps1
```


4. **Finally, install the dependencies**

````shell
pip install -r requirements.txt
````

5. **Configure EpiModo**. This is necessary to use the bot. Check the next section for instructions.

6. **Run `python index.py` to launch Brawl Bot.** Also make sure that the venv is activated when you launch Brawl Bot (you should see `venv` to the left of your command prompt).

## Configuration

The `run/config` folder contains all the data of the program configuration.

### config.default.yml

This file contain all data about configuration. This file looks like this:
 
```yaml
prefix: ~ 
token: ~
```

You must fill in the file and rename it to `config.yml`
