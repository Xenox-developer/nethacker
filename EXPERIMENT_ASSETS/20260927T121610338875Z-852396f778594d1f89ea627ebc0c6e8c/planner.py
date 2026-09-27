"""Small, observation-only tactical model; no game engine or NLE dependency.

Only supplied root action keys can be returned. The adapter must keep emergency
and unsupported actions, supply conservative combat estimates, and exclude unknown
terrain, doors, hazards and friendly occupancy from the topology. Player edges
must be confirmed legal. Enemies conservatively get every known adjacent floor
square, including corner squeezes; player corner restrictions cannot imply safety.
This is a bounded approximation, not a reconstruction of hidden game state.
"""
from __future__ import annotations

import math
from collections import deque
from collections.abc import Hashable, Sequence
from dataclasses import dataclass, replace

Pos = tuple[int, int]
_DIRECTIONS = tuple((y, x) for y in (-1, 0, 1) for x in (-1, 0, 1) if (y, x) != (0, 0))


@dataclass(frozen=True)
class Topology:
    cells: frozenset[Pos]
    diagonals: frozenset[tuple[Pos, Pos]] = frozenset()

    def __post_init__(self) -> None:
        object.__setattr__(self, "cells", frozenset(self.cells))
        object.__setattr__(self, "diagonals", frozenset(self.diagonals))

    def allows(self, source: Pos, target: Pos) -> bool:
        if source not in self.cells or target not in self.cells:
            return False
        dy, dx = target[0] - source[0], target[1] - source[1]
        if (dy, dx) not in _DIRECTIONS:
            return False
        if not dy or not dx:
            return True
        return (((source, target) in self.diagonals or (target, source) in self.diagonals)
                and (source[0], target[1]) in self.cells
                and (target[0], source[1]) in self.cells)

    def neighbors(self, pos: Pos) -> tuple[Pos, ...]:
        return tuple(target for dy, dx in _DIRECTIONS
                     if self.allows(pos, target := (pos[0] + dy, pos[1] + dx)))


@dataclass(frozen=True)
class Monster:
    key: str
    pos: Pos
    hp: float
    damage: float
    speed: float = 12.0


@dataclass(frozen=True)
class State:
    topology: Topology
    player_pos: Pos
    hp: float
    damage: float
    monsters: tuple[Monster, ...]
    speed: float = 12.0
    recent_positions: tuple[Pos, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "monsters", tuple(self.monsters))
        object.__setattr__(self, "recent_positions", tuple(self.recent_positions))


@dataclass(frozen=True)
class Action:
    key: Hashable
    kind: str  # only "move" and "melee" are modeled root actions
    target: Pos


@dataclass(frozen=True)
class Config:
    depth: int = 3
    beam_width: int = 6
    max_nodes_per_root: int = 160
    score_margin: float = 4.0
    min_damage_reduction: float = 2.0
    min_damage_fraction: float = 0.12
    max_monsters: int = 6
    max_cells: int = 121


_DEFAULT_CONFIG = Config()


@dataclass(frozen=True)
class RootMetrics:
    key: Hashable
    score: float
    worst_min_hp: float
    worst_damage: float
    lethal_scenarios: int
    terminal_hp: tuple[float, ...]
    nodes: int
    depth_reached: int
    principal_variation: tuple[Pos, ...]  # relative commands, including the root


@dataclass(frozen=True)
class Decision:
    override_key: Hashable | None
    reason: str
    roots: tuple[RootMetrics, ...] = ()

    @property
    def nodes(self) -> int:
        return sum(root.nodes for root in self.roots)


@dataclass(frozen=True)
class _Scenario:
    hp_scale: float
    player_damage_scale: float
    enemy_damage_scale: float
    initial_credit: float
    reverse_order: bool


_SCENARIOS = (_Scenario(1.0, 1.0, 1.0, 0.0, False),
              _Scenario(1.5, 0.75, 1.35, 1.0 - 1e-8, True))


@dataclass(frozen=True)
class _Enemy:
    model: Monster
    pos: Pos
    hp: float
    credit: float


@dataclass(frozen=True)
class _World:
    pos: Pos
    hp: float
    min_hp: float
    enemies: tuple[_Enemy, ...]
    damage_dealt: float = 0.0
    kills: int = 0
    moves: int = 0
    revisits: int = 0
    visited: tuple[Pos, ...] = ()


@dataclass(frozen=True)
class _Branch:
    worlds: tuple[_World, ...]
    commands: tuple[Pos, ...]


def _initial(state: State, scenario: _Scenario) -> _World:
    return _World(state.player_pos, state.hp, state.hp, tuple(
        _Enemy(monster, monster.pos, monster.hp * scenario.hp_scale, scenario.initial_credit)
        for monster in sorted(state.monsters, key=lambda m: m.key)),
        visited=state.recent_positions[-6:] + (state.player_pos,))


def _enemy_neighbors(topology: Topology, pos: Pos) -> tuple[Pos, ...]:
    return tuple(target for dy, dx in _DIRECTIONS
                 if (target := (pos[0] + dy, pos[1] + dx)) in topology.cells)


class _SearchContext:
    """Per-decision memoization of explicit topology only, capped at 256 maps."""

    def __init__(self, topology: Topology) -> None:
        self.neighbors = {pos: _enemy_neighbors(topology, pos) for pos in topology.cells}
        self.cache: dict[tuple[Pos, frozenset[Pos]], dict[Pos, int]] = {}

    def distances(self, player: Pos, occupied: frozenset[Pos]) -> dict[Pos, int]:
        key = player, occupied
        if key not in self.cache:
            distances = {player: 0}
            queue = deque([player])
            while queue:
                pos = queue.popleft()
                for neighbor in self.neighbors[pos]:
                    if neighbor not in distances and neighbor not in occupied:
                        distances[neighbor] = distances[pos] + 1
                        queue.append(neighbor)
            if len(self.cache) >= 256:
                self.cache.pop(next(iter(self.cache)))
            self.cache[key] = distances
        return self.cache[key]


def _towards(context: _SearchContext, enemy: _Enemy, player: Pos, occupied: frozenset[Pos],
             reverse: bool) -> Pos:
    """Shortest known legal route, with two deterministic tie/order hypotheses."""
    distances = context.distances(player, occupied)
    choices = sorted((p for p in context.neighbors[enemy.pos]
                      if p not in occupied and p != player and p in distances), reverse=reverse)
    return min(choices, key=lambda p: distances[p]) if choices else enemy.pos


def _step(state: State, world: _World, delta: Pos, scenario: _Scenario,
          context: _SearchContext, kind: str = "step") -> _World | None:
    if world.hp <= 0:  # Death is absorbing; a later strike can never erase it.
        return world
    target = (world.pos[0] + delta[0], world.pos[1] + delta[1])
    if not state.topology.allows(world.pos, target):
        return None
    enemies = list(world.enemies)
    victim = next((i for i, monster in enumerate(enemies) if monster.pos == target), None)
    if (kind == "move" and victim is not None) or (kind == "melee" and victim is None):
        return None
    if victim is None:
        world = replace(world, pos=target, moves=world.moves + 1,
                        revisits=world.revisits + int(target in world.visited),
                        visited=world.visited + (target,))
    else:
        enemy = enemies[victim]
        damage = state.damage * scenario.player_damage_scale
        hp = enemy.hp - damage
        world = replace(world, damage_dealt=world.damage_dealt + min(enemy.hp, damage),
                        kills=world.kills + int(hp <= 0))
        if hp <= 0:
            enemies.pop(victim)
        else:
            enemies[victim] = replace(enemy, hp=hp)

    # Each micro-action is either movement or one contact attack. Fractional
    # credits accumulate; slow monsters do not unrealistically attack every turn.
    indexes = sorted(range(len(enemies)), key=lambda i: enemies[i].model.key,
                     reverse=scenario.reverse_order)
    for index in indexes:
        enemy = enemies[index]
        credit = enemy.credit + enemy.model.speed / state.speed
        count = int(credit)
        enemy = replace(enemy, credit=credit - count)
        for _ in range(count):
            if world.pos in context.neighbors[enemy.pos]:
                hp = world.hp - enemy.model.damage * scenario.enemy_damage_scale
                world = replace(world, hp=hp, min_hp=min(world.min_hp, hp))
                if hp <= 0:
                    enemies[index] = enemy
                    return replace(world, enemies=tuple(enemies))
            else:
                occupied = frozenset(other.pos for i, other in enumerate(enemies) if i != index)
                enemy = replace(enemy, pos=_towards(context, enemy, world.pos,
                                                    occupied, scenario.reverse_order))
            enemies[index] = enemy
        enemies[index] = enemy
    return replace(world, enemies=tuple(enemies))


def _utility(state: State, world: _World) -> float:
    if world.min_hp <= 0:
        return -1_000_000.0  # No terminal progress/kill bonus can offset intermediate death.
    lost = max(0.0, (state.hp - world.min_hp) / state.hp)
    risk = 120 * lost + 60 * lost * lost + 100 * max(0.0, lost - 0.75)
    progress = 5 * world.damage_dealt / state.damage + 12 * world.kills
    return progress - risk - 0.8 * world.moves - 6 * world.revisits


def _score(state: State, branch: _Branch) -> float:
    utilities = tuple(_utility(state, world) for world in branch.worlds)
    return min(utilities) + 0.05 * sum(utilities) / len(utilities)


def _advance(state: State, branch: _Branch, delta: Pos, context: _SearchContext,
             kind: str = "step") -> _Branch | None:
    worlds = tuple(_step(state, world, delta, scenario, context, kind)
                   for world, scenario in zip(branch.worlds, _SCENARIOS, strict=True))
    if any(world is None for world in worlds):
        return None
    return _Branch(tuple(world for world in worlds if world is not None),
                   branch.commands + (delta,))


def _search_root(state: State, action: Action, config: Config,
                 context: _SearchContext) -> RootMetrics:
    initial = _Branch(tuple(_initial(state, scenario) for scenario in _SCENARIOS), ())
    delta = (action.target[0] - state.player_pos[0], action.target[1] - state.player_pos[1])
    first = _advance(state, initial, delta, context, action.kind)
    assert first is not None  # validated before any roots are searched
    beam = [first]
    nodes, reached = 1, 1
    for depth in range(2, config.depth + 1):
        children = []
        exhausted = False
        for branch in beam:
            if all(world.hp <= 0 for world in branch.worlds):
                children.append(branch)  # absorbing terminal states retain their lethal score
                continue
            for direction in _DIRECTIONS:
                if nodes >= config.max_nodes_per_root:
                    exhausted = True
                    break
                child = _advance(state, branch, direction, context)
                if child is not None:
                    nodes += 1
                    children.append(child)
            if exhausted:
                break
        if exhausted or not children:
            break  # keep the last completely explored horizon; caller refuses partial comparison
        beam = sorted(children, key=lambda child: (-_score(state, child), child.commands))[
            :config.beam_width]
        reached = depth
    best = min(beam, key=lambda branch: (-_score(state, branch), branch.commands))
    minimum = min(world.min_hp for world in best.worlds)
    return RootMetrics(action.key, _score(state, best), minimum, state.hp - minimum,
                       sum(world.min_hp <= 0 for world in best.worlds),
                       tuple(world.hp for world in best.worlds), nodes, reached, best.commands)


def _valid(state: State, actions: tuple[Action, ...], baseline_key: Hashable,
           config: Config) -> bool:
    if (not isinstance(state, State) or not isinstance(state.topology, Topology)
            or not 1 <= config.depth <= 3 or not 1 <= config.beam_width <= 12
            or not 1 <= config.max_nodes_per_root <= 256
            or not 1 <= config.max_monsters <= 6 or not 1 <= config.max_cells <= 121
            or not 1 <= len(actions) <= 8 or not 1 <= len(state.monsters) <= config.max_monsters
            or not 1 <= len(state.topology.cells) <= config.max_cells
            or len(state.topology.diagonals) > 8 * len(state.topology.cells)
            or state.player_pos not in state.topology.cells):
        return False
    positions = (*state.topology.cells, state.player_pos,
                 *(monster.pos for monster in state.monsters),
                 *(action.target for action in actions))
    if any(not isinstance(pos, tuple) or len(pos) != 2
           or any(not isinstance(axis, int) for axis in pos) for pos in positions):
        return False
    numbers = (state.hp, state.damage, state.speed, config.score_margin,
               config.min_damage_reduction, config.min_damage_fraction,
               *(value for monster in state.monsters
                 for value in (monster.hp, monster.damage, monster.speed)))
    if any(not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0
           for value in numbers):
        return False
    if (len({monster.key for monster in state.monsters}) != len(state.monsters)
            or len({monster.pos for monster in state.monsters}) != len(state.monsters)
            or any(not isinstance(monster.key, str) or not monster.key
                   or monster.pos not in state.topology.cells or monster.pos == state.player_pos
                   or monster.speed / state.speed > 3 for monster in state.monsters)):
        return False
    if (len({action.key for action in actions}) != len(actions)
            or baseline_key not in {action.key for action in actions}):
        return False
    occupied = {monster.pos for monster in state.monsters}
    return all(action.key is not None and action.kind in ("move", "melee")
               and state.topology.allows(state.player_pos, action.target)
               and ((action.target in occupied) == (action.kind == "melee")) for action in actions)


def choose_action(state: State | None, root_actions: Sequence[Action], baseline_key: Hashable,
                  config: Config = _DEFAULT_CONFIG) -> Decision:
    """Return an existing safer key, or ``None`` to preserve the old policy.

    Each root receives its own equal transition budget. A transition advances
    both response scenarios; traces expose nodes, completed horizon, worst
    intermediate health, and the chosen relative command sequence. Recompute
    after every real observation instead of committing the future commands.
    """
    try:
        actions = tuple(root_actions)
        if not _valid(state, actions, baseline_key, config):
            return Decision(None, "unsupported_state_or_actions")
    except (TypeError, ValueError, AttributeError, IndexError):
        return Decision(None, "unsupported_state_or_actions")
    assert state is not None
    context = _SearchContext(state.topology)
    roots = tuple(_search_root(state, action, config, context) for action in actions)
    if any(root.depth_reached < config.depth for root in roots):
        return Decision(None, "incomplete_horizon", roots)
    baseline = next(root for root in roots if root.key == baseline_key)
    best = max(roots, key=lambda root: (root.score, root.key == baseline_key))
    if best.key == baseline_key:
        return Decision(None, "baseline_preferred", roots)
    if best.score < baseline.score + config.score_margin or best.lethal_scenarios:
        return Decision(None, "insufficient_safety_margin", roots)
    reduction = baseline.worst_damage - best.worst_damage
    required = max(config.min_damage_reduction, state.hp * config.min_damage_fraction)
    if not baseline.lethal_scenarios and reduction < required:
        return Decision(None, "insufficient_risk_reduction", roots)
    return Decision(best.key, "safer_multi_turn_plan", roots)
