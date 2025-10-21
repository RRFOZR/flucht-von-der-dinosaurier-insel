# config.py

class Config:
    """
    Global configuration settings.
    """
    DEBUG_MODE = False  # Set to False for normal play; True for debugging features.
    SEED = 12341

    WINDOW_WIDTH = 1500
    WINDOW_HEIGHT = 900
    FPS = 60  # Increased to 60 FPS for ultra-smooth gameplay!

    MAP_WIDTH = 512
    MAP_HEIGHT = 512
    TILE_SIZE = 32

    # Joystick Configuration
    ENABLE_JOYSTICK = False
    JOYSTICK_FIRE_BUTTON = 3
    JOYSTICK_AXIS_THRESHOLD = 0.5

    BIOMES = {
        0: {"color": (139, 69, 19),  "passable": True,  "name": "Volcano"},
        1: {"color": (34, 139, 34),  "passable": True,  "name": "Forest"},
        2: {"color": (238, 214, 175),"passable": True,  "name": "Beach"},
        3: {"color": (0, 0, 255),    "passable": False, "name": "Water"},
        4: {"color": (102, 51, 0),   "passable": True,  "name": "Mud"},
        5: {"color": (128, 128, 128),"passable": True,  "name": "Spikes"}
    }

    PLAYER_SPEED = 1
    PLAYER_MAX_HP = 120

    DINOSAUR_COUNT_NORMAL = 100
    DINOSAUR_SPEED_NORMAL = 1.0
    DINOSAUR_COUNT_AGGRESSIVE = 60
    DINOSAUR_SPEED_AGGRESSIVE = 0.8
    DINOSAUR_SIGHT_DAY = 5
    DINOSAUR_SIGHT_NIGHT = 8
    DINOSAUR_ATTACK_DAMAGE = 5
    DINOSAUR_RANDOM_MOVE_CHANCE = 0.05
    DINOSAUR_RUNAWAY_DISTANCE = 3

    DAY_LENGTH = 8.0
    NIGHT_LENGTH = 8.0
    CYCLE_LENGTH = DAY_LENGTH + NIGHT_LENGTH

    LAVA_DURATION = 5.0
    LAVA_INTERVAL = 10.0
    LAVA_DAMAGE = 20

    SPIKE_DAMAGE = 0
    SPIKES_ENABLED = False

    POTION_HEAL = 25
    REPELLENT_DURATION = 10.0

    BOAT_COLOR = (255, 255, 0)
    BOAT_SIZE_FACTOR = 2
    BOAT_ARRIVAL_CYCLES = 3

    NIGHT_OVERLAY = (0, 0, 50, 100)

    SPRITES = {
        "entities": {
            "player": {
                "idle_0": "konrad_insel/bg_entities/player_0.png",
                "idle_1": "konrad_insel/bg_entities/player_1.png",
            },
            "dinosaur": {
                "aggressive": {
                    "idle_0": "konrad_insel/bg_entities/aggdino_0.png",
                    "idle_1": "konrad_insel/bg_entities/aggdino_1.png",
                },
                "normal": {
                    "idle_0": "konrad_insel/bg_entities/dino_0.png",
                    "idle_1": "konrad_insel/bg_entities/dino_1.png",
                },
            },
        },
        "items": {
            "potion": "konrad_insel/bg_entities/healing0.png",
            "repellent": "konrad_insel/bg_entities/repellent1_0.png",
        },
        "boats": {
            "frame_0": "konrad_insel/bg_entities/ship_0.png",
            "frame_1": "konrad_insel/bg_entities/ship_1.png",
        },
    }

    SOUNDS = {
        "entities": {
            "player_move_soft": "konrad_insel/sounds/player_move_soft.mp3",
            "potion_use": "konrad_insel/sounds/potion_use.mp3",
            "repellent_trigger": "konrad_insel/sounds/repellent_trigger.mp3",
            "player_damage": "konrad_insel/sounds/player_damage.mp3",
        },
        "environment": {
            "day": "konrad_insel/sounds/day.mp3",
            "night": "konrad_insel/sounds/night.mp3",
            "boat_arrives": "konrad_insel/sounds/boat_arrives.mp3",
            "background_music": [
                "konrad_insel/sounds/music1.mp3",
                "konrad_insel/sounds/music2.mp3",
            ],
        },
        "actions": {
            "game_start": "konrad_insel/sounds/game_start.mp3",
            "game_over": "konrad_insel/sounds/game_over.mp3",
            "win_game": "konrad_insel/sounds/win_game.mp3",
            "dino_roar": "konrad_insel/sounds/dino_roar.mp3",
            "dino_steps": "konrad_insel/sounds/dino_steps.mp3",
            "potion_pickup": "konrad_insel/sounds/potion_repellent_pickup.mp3",
            "healing": "konrad_insel/sounds/healing.mp3",
            "screen_flash": "konrad_insel/sounds/screen_flash.mp3",
            "repellent_trigger": "konrad_insel/sounds/repellent_trigger.mp3",
        },
    }

    SOUND_VOLUMES = {
        "boat_arrives":     0.6,
        "day":              0.4,
        "dino_roar":        0.2,
        "dino_steps":       0.5,
        "game_over":        0.8,
        "game_start":       0.5,
        "night":            0.4,
        "player_damage":    0.9,
        "player_move_soft": 0.5,
        "potion_use":       0.6,
        "repellent_trigger":0.6,
        "win_game":         0.7,
        "potion_pickup":    0.6,
        "healing":          0.7,
        "screen_flash":     0.5,
    }

    DEFAULT_SOUND_VOLUME = 0.5
    MUSIC_VOLUME_DAY = 0.4
    MUSIC_VOLUME_NIGHT = 0.4

    SCREENS = {
        "title": "konrad_insel/bg_images/title.png",
        "begin": "konrad_insel/bg_images/begin.png",
        "help":  "konrad_insel/bg_images/help.png",
        "lose":  "konrad_insel/bg_images/loose.png",
        "pause": "konrad_insel/bg_images/pause.png",
        "win":   "konrad_insel/bg_images/rescue.png",
    }

    TEXTS = {
        "MAIN_MENU": [
            "FLUCHT VON DER DINOSAURIER-INSEL",
            "Ein Spiel von Konrad Weber",
            "Umgesetzt von Stefan Weber (und ChatGPT 4o1) im Dezember 2024",
            "Drücke [ENTER] zum STARTEN, [H] für Hilfe, [Q] zum Beenden."
        ],
        "HELP_SCREEN": [
            "HILFE",
            "Kontrolle:",
            " - Bewegen: WASD / Pfeiltasten",
            " - Leertaste: Dino Spray benutzen",
            " - E oder Rechts-Shift: Heiltrank benutzen",
            " - ESC: Pause/Unpause oder Exit",
            "",
            "Ziel des Spiels ist es auf der Dinosaurier-Insel zu überleben bis das rettende Boot ankommt.",
            "Drücke eine beliebige Taste, um zum Hauptmenü zurückzukehren."
        ],
        "PAUSE_SCREEN": [
            "SPIEL PAUSIERT",
            "Drücke [ESC] zum Fortsetzen, [H] für Hilfe, [M] für Musik an/aus oder [Q] zum Beenden."
        ],
        "LOSE_SCREEN": [
            "GAME OVER!",
            "Du musst leider aufgeben... Vielleicht beim nächsten Mal!",
            "Drücke [ENTER] um zum Hauptmenü zurückzukehren."
        ],
        "WIN_SCREEN": [
            "GLÜCKWUNSCH!",
            "Du hast die Insel überlebt und das rettende Schiff erreicht!",
            "Drücke [ENTER] um zum Hauptmenü zurückzukehren."
        ],
        "INTRO_SCREEN": [
            "Willkommen auf der gefährlichen Dinosaurier-Insel.",
            "Du bist mit dem Flugzeug abgestürzt direkt neben dem Vulkan auf der Mitte der Insel.",
            "Du musst überleben und dich zum Strand durchschlagen, bis ein Boot ankommt.",
            "Dabei musst du gefährlichen Dinos ausweichen!",
            "Drücke eine beliebige Taste, um das Abenteuer zu beginnen! Viel Glück!"
        ],
    }

    @staticmethod
    def get_sprite_path(*keys) -> str:
        """
        Retrieve a sprite path from the nested SPRITES structure.
        Returns an empty string if the path is not found.
        """
        try:
            node = Config.SPRITES
            for key in keys:
                node = node[key]
            return node
        except KeyError:
            return ""

    @staticmethod
    def get_sound_path(*keys) -> str:
        """
        Retrieve a sound path from the nested SOUNDS structure.
        Returns an empty string if the path is not found.
        """
        try:
            node = Config.SOUNDS
            for key in keys:
                node = node[key]
            return node
        except KeyError:
            return ""

    @staticmethod
    def get_screen_image(key: str) -> str:
        """
        Returns the path to the screen image specified by 'key'.
        Returns an empty string if it doesn't exist.
        """
        return Config.SCREENS.get(key, "")
