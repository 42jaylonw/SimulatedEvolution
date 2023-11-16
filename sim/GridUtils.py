import math

"""
    Gets positions radiating outwards in a circle from the center
    :param
        layer_system: the LayerSystem of the SimSpace to get the grid positions from
        center_pos: the position of the center of the circle
        radius: radius of the circle
        do_obstructions: if True, walls will block from center
    :output
        List of tuples (pos, dist), where pos is the position and dist is the distance from the center
"""
def get_circle_coord_dist_pairs(layer_system, center_pos, radius, do_obstructions=True):
    emit_position_pairs = []
    emit_positions = []
    for angle in range(0, 360, 1):
        for r in range(0, radius, 1):
            x = int(round(r * math.sin(math.radians(angle)) + center_pos[0]))
            y = int(round(r * math.cos(math.radians(angle)) + center_pos[1]))
            emit_pos = [x, y]
            pos_dist_pair = (emit_pos, r)
            if layer_system.out_of_bounds(emit_pos) or (do_obstructions and layer_system.has_wall(emit_pos)):
                break
            if emit_pos not in emit_positions:
                emit_positions.append(emit_pos)
                emit_position_pairs.append(pos_dist_pair)
    return emit_position_pairs


# Checks whether the position is out of bounds of given bounds or not (True if out of bounds, False if within bounds)
# Input: bounds -> grid bounds to check
#        pos -> position in sim to check
# Output: bool
def out_of_bounds(dim, pos):
    """
        :param:
            pos: [x, y] position that is checked to see if outside of bounds
        :return:
            True: pos is outside of bounds of sim space
            False: pos is within bounds of sim space
    """
    return pos[0] < 0 or pos[0] > dim[0] - 1 or pos[1] < 0 or pos[1] > dim[1] - 1