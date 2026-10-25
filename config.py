"""
Configuration and settings for Desktop Lula - Presidential Edition.
"""
import json
import os
import sys

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "scale": 1.0,                 # Scale factor for sprite
    "walk_speed": 2.2,            # Calm editorial walk speed (px per frame)
    "run_speed": 4.5,             # Gentle run speed (px per frame)
    "tick_rate_ms": 16,           # Frame update rate (60 FPS)
    "idle_min_seconds": 6.0,      # Minimum resting time
    "idle_max_seconds": 12.0,     # Maximum resting time
    "action_interval_seconds": 30.0, # Approximate frequency of special actions (~1 every 30s)
    "mouse_steal_enabled": True,  # Mouse stealing enabled
    "mouse_steal_duration_seconds": 2.5, # Short comical mouse hide duration
    "drop_trail_interval": 300,   # Steps between drops (bem mais espaçado)
    "drop_lifetime_seconds": 2.5, # Desaparece bem rápido (2.5 segundos)
    "sounds_enabled": True,       # Enable sound effects
    "speech_bubbles_enabled": True, # Enable cartoon speech bubbles
    "phrases": [
        "Companheiro!",
        "Companheiro, onde ta o app do banco?",
        "Onde fica o app do banco nessa tela? E pra checagem solidaria...",
        "Cade o app do Nubank ou Itau? So pra conferir um negocinho...",
        "O Windows ta lento? Culpa do Bolsonaro!",
        "Se o mouse travou, e culpa da heranca maldita!",
        "A bateria descarregou por culpa do capitao!",
        "Essa aba do Chrome travou por causa dos 4 anos de desgoverno!",
        "A internet caiu? Sabotagem do governo anterior!",
        "O Bolsonaro ia privatizar esse mouse, eu salvei!",
        "Nao fui eu que peguei o mouse, foi o pessoal de Orlando!",
        "Qualquer travamento no sistema e culpa do Bolsonaro!",
        "O cafe esfriou? Culpa do Bolsonaro!",
        "E a picanha, ja comprou?",
        "Segura esse boleto com muito amor!",
        "Guardei seu mouse no paleto!",
        "Sigilo de 100 anos no cursor!",
        "A faixa presidencial combina comigo!",
        "A culpa e do capitao, companheiro!"
    ]
}

def get_config_filepath():
    # If custom config.json exists next to the .exe in frozen mode, prioritize it
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        exe_cfg = os.path.join(exe_dir, CONFIG_FILE)
        if os.path.exists(exe_cfg):
            return exe_cfg
    if os.path.exists(CONFIG_FILE):
        return CONFIG_FILE
    return None

def load_config():
    cfg_path = get_config_filepath()
    if cfg_path and os.path.exists(cfg_path):
        try:
            with open(cfg_path, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
                merged = DEFAULT_CONFIG.copy()
                merged.update(cfg)
                return merged
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    target = CONFIG_FILE
    if getattr(sys, 'frozen', False):
        target = os.path.join(os.path.dirname(sys.executable), CONFIG_FILE)
    try:
        with open(target, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving config: {e}")
