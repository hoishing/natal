from natal.config import Config

config = {
    "light_theme": {
        "fire": "#ff0000",
        "earth": "#ffff00",
        "air": "#00ff00",
        "water": "#0000ff",
        "points": "#00ffff",
    },
    "display": {
        "asc_node": False,
        "chiron": True,
    },
    "orb": {
        "conjunction": 8,
        "opposition": 7,
        "trine": 6,
        "square": 6,
        "sextile": 8,
    },
}


def test_load_config_from_dict() -> None:
    cfg = Config(**config)
    assert cfg.light_theme.fire == "#ff0000"
    assert cfg.display.asc_node == False
    assert cfg.orb.opposition == 7


def test_mono_theme() -> None:
    cfg = Config(theme_type="mono")
    assert cfg.theme_type == "mono"
    assert cfg.theme.foreground == cfg.theme.fire
    assert cfg.theme.background == "white"
    assert cfg.theme.transparency == 0
