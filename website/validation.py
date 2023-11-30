

# validate the user input
def validateSimulationParameters(grid_size, num_consumers=0, num_producers=0):
        if num_consumers is None:
             num_consumers = 0
        if num_producers is None:
             num_producers = 0
        print(f'VALIDATING gridSize: {grid_size}, consumers: {num_consumers}, producers: {num_producers}')
        if not is_numeric(grid_size) or not is_numeric(num_consumers) or not is_numeric(num_producers):
             return 'Non-numerals'
        grid_size = int(grid_size)
        num_consumers = int(num_consumers)
        num_producers = int(num_producers)

        if grid_size <= 0 or grid_size > 50:
            return f'Invalid size: {grid_size}. Size must be within range 1-50'
        
        if num_consumers < 0 or num_producers < 0:
             return 'Number of creatures must be positive'
        print(grid_size, " PASS")
        return 'OK'

def is_numeric(val):
      if val is None:
           return False
      try:
        int(val)
        return True
      except ValueError:
           return False 