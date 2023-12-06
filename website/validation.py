

# validate the user input
def validateSimulationParameters(grid_size, num_generations=1, num_consumers=0, num_producers=0):
        print("validate:", num_generations)
        if num_consumers is None:
             num_consumers = 0
        if num_producers is None:
             num_producers = 0
        if num_generations is None:
             num_generations = 1
        # Check for non numeric input
        if not is_numeric(grid_size) or not is_numeric(num_consumers) or not is_numeric(num_producers) or not is_numeric(num_generations):
             return 'Non-numerals'

        grid_size = int(grid_size)
        num_consumers = int(num_consumers)
        num_producers = int(num_producers)
        num_generations = int(num_generations)
        # Check for valid numeric input
        if grid_size <= 0 or grid_size > 50:
            return f'Invalid size: {grid_size}. Size must be within range 1-50'
        
        if num_consumers < 0 or num_producers < 0:
             return 'Number of creatures must be positive'
        if num_generations <= 0:
             return 'Number of generations must be positive'
        return 'OK'

# Check if value is numeric
def is_numeric(val):
      if val is None:
           return False
      try:
        int(val)
        return True
      except ValueError:
           return False 