from dataclasses import dataclass

from sim.creatures import Creature

# Pheremone: a struct-like object that represents a strength value and a reference to its source Creature
# Emitted by Consumers, and handled by LayerSystem
@dataclass
class Pheremone:
    strength: float
    source: Creature
