from pathlib import Path

PACKAGE_BASEPATH = Path(__file__) / "../"
SETTINGS_PATH = PACKAGE_BASEPATH / "stock" / "settings.toml"

DATA_BASEPATH = Path.home() / ".stockapp/"
STOCKFILES = DATA_BASEPATH / "stockfiles"

MODELS_BASEPATH = DATA_BASEPATH / "models"