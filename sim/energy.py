class EnergyBar:

    def __init__(self, initial_energy=50.0, max_energy=100.0, satiation_level=85.0, size=1.0):
        self.current_energy = initial_energy
        self.max_energy = max_energy
        self.size = size

    def consume_energy(self, movement_cost=0):
        """
        Called on a time step.
        Lowers energy level based on metabolism and movement cost.
        """
        energy_consumption = float(self.size * 0.10)
        self.current_energy -= energy_consumption + movement_cost
        if self.current_energy < 0:
            self.current_energy = 0

    def replenish_energy(self, energy):
        """
        Adds energy to the creature.
        Added energy does not go above a creature's max energy.
        """
        self.current_energy = min(self.max_energy, self.current_energy + energy)

    def is_empty(self)
        """
        Returns true if there is no more energy left.
        """
        return self.current_energy == 0

    def is_satiated(self)
        """
        Returns true if the creature is 'satiated'.
        A 'satiated' creature has energy above a given satiation threshold.
        This can be used to determine when the creature stops looking for food
        and starts looking for mates.
        """
        return self.current_energy >= self.satiation_level

    def movement_cost(self, elevation_curr=0.0, elevation_next=0.0, difficulty=1.0)
        """
        Calculates the cost of moving (in energy) based on the difference in elevation
        between two locations. 
        Difficulty, an abstraction for harsh weather conditions/genetic efficiency/etc,
        acts as a multiplier to the cost of moving.

        Movement can never cost more than 5 energy or less than 0.1 energy.

        On flat ground, default difficulty, and normal conditions, a movement should cost 0.5 energy.
        """
        incline_mult_scaling = 0.1
        decline_mult_scaling = 0.05

        elevation_diff = float(elevation_next) - float(elevation_curr)
        elevation_multiplier = 1.0

        if elevation_diff > 0:
            elevation_multiplier = 1.0 + (elevation_diff * incline_mult_scaling)
        elif elevation_diff < 0:
            elevation_multiplier = 1.0 - (elevation_diff * decline_mult_scaling)

        energy_cost = 0.5 * difficulty * elevation_multiplier
        return energy_cost

