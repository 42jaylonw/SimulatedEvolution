import string
from dataclasses import dataclass

from sim.creatures import Creature
@dataclass
class Pheremone:
    strength: float
    source: Creature
    genome: [string] # WIP - maybe not this type of string