"""Install the isolated experiment inside an official evolve workspace.

Usage: python EXPERIMENT_ASSETS/<request-id>/install.py /workspace
Never run this against the saved champion or an already-running bot snapshot.
"""

import argparse
import shutil
from pathlib import Path

ANCHOR = ("            priority, best_action = "
          "max(actions, key=lambda x: x[0]) if actions else None\n")
MARKER = "# hypothesis: three-turn tactical forecasts avoid near-term lethal exchanges"
HOOK = (
    "            " + MARKER + "\n"
    "            if jf_config.TACTICAL_LOOKAHEAD:\n"
    "                from .combat.lookahead_adapter import select_action\n"
    "                priority, best_action = select_action(\n"
    "                    self, actions, (priority, best_action), force_attack=allow_attack_all)\n"
)


def install(solution: Path, assets: Path | None = None) -> None:
    assets = assets or Path(__file__).resolve().parent
    source_path = solution / "autoascend" / "agent.py"
    config_path = solution / "autoascend" / "jf_config.py"
    if not (solution / "bot.py").is_file() or not config_path.is_file():
        raise ValueError("Expected the AutoAscend champion layout")
    source = source_path.read_text()
    if MARKER not in source and source.count(ANCHOR) != 1:
        raise ValueError("Combat selection has changed; review integration manually")
    planner = assets / "planner.py"
    adapter = assets / "adapter.py"
    if not planner.is_file() or not adapter.is_file():
        raise ValueError("Frozen planner and adapter are both required")
    destination = solution / "autoascend" / "combat"
    destination.mkdir(exist_ok=True)
    shutil.copyfile(planner, destination / "lookahead.py")
    shutil.copyfile(adapter, destination / "lookahead_adapter.py")
    if MARKER not in source:
        source_path.write_text(source.replace(ANCHOR, ANCHOR + HOOK))
    config = config_path.read_text()
    if "TACTICAL_LOOKAHEAD" not in config:
        config_path.write_text(config.rstrip() + "\n\n# Bounded three-turn tactical experiment.\n"
                               "TACTICAL_LOOKAHEAD = True\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("solution", type=Path)
    args = parser.parse_args()
    install(args.solution)
