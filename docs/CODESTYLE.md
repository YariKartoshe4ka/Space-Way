## Codestyle of project


#### Structure

Now project has this structure:

```sh
|____ __init__.py
|____ boost.py
|____ collection.py
|____ config.py
|____ debug.py
|____ hitbox.py
|____ main.py
|____ mixins.py
|____ music.py
|____ updater.py
|____ assets
| |____ <fonts, sprites, sounds and other binary files...>
|____ config
| |____ config.json
| |____ user.json
| |____ score.csv
|____ scenes
| |____ __init__.py
| |____ <some scene...>
| | |____ __init__.py
| | |____ functions.py
| | |____ objects.py
```

General files:
- *\_\_init__.py* - default file for python modules. Checks version of Python and prints exception if it less than 3.6.0
- *boost.py* - file with implementation of various utility functions
- *collection.py* - file with the implementation of additional data structures, mainly the *pygame.sprite.Group* extensions
- *config.py* - file with some objects for easier configuration management
- *debug.py* - file with some objects for easier debugging game
- *hitbox.py* - file with implementation of hitboxes for some objects calculations
- *main.py* - main file, import all modules, contains the entrypoint of game and connects all the scenes together
- *mixins.py* - file with mixins which are needed for simple creation of the same type of objects (DRY principle)
- *music.py* - file with some objects for easier music (sounds) management
- *updater.py* - file responsible for updating Space Way

Assets:
- *assets* - directory with assets for game, mainly sprites, sounds and fonts

Configuration:
- *config* - directory with the original configuration files
- *config/config.json* - main configuration file, contains the current version, FPS, and other static Space Way parameters
- *config/user.json* - onfiguration file that is changed by the user during the process of changing the game settings
- *config/score.csv* - table with the data of the best 10 user attempts

Scenes:
- *scenes* - directory with scenes for game
- *scenes/\_\_init__.py* - default file for python modules. In this case loads all scripts of all scenes
- *scenes/\<scene name>* - directory with scripts of defined scene
- *scenes/\<scene name>/\_\_init__.py* - contains only one function - `init`, which creates all the objects of this scene and returns them
- *scenes/\<scene name>/functions.py* - file with the functions of this scene. It must contain at least two functions: `check_events` (checks the keyboard, mouse, and other events) and `update` (updates and blits all objects of this scene)


#### Codestyle

Basically, the code should be written in the PEP8 style.<br>
You can omit various rules that are sometimes difficult to follow (e.g. E509), but you should not abuse this.<br>
It is recommended to type functions (with `typing` module or default classes).<br>
Also, do not comment on every line of code, do not chew what is already clear
