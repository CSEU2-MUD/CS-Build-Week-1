import random
from util.planet_names import planets

class Room:
    def __init__(self, id, name, x, y, atmosphere, moons, composition, density, temperature ):
        self.id = id
        self.name = name
        self.description = f"{name} has {atmosphere} atmosphere, {composition} composition, {moons} moons orbitating around it, a density of {density} gm/cm³, and a temperature of circa {temperature}°"
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
        self.atmosphere = atmosphere
        self.moons = moons
        self.composition = composition
        self.density = density
        self.temperature = temperature
        
    def __repr__(self):
        return f"({self.x}, {self.y})"
    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
    
    

    def get_neighbours(self, x, y, size_x, size_y):      
        '''
        Get the neighbours of a room
        '''
        neighbours = [None, None, None, None]
        if y < size_y - 1 and self.grid[y +1][x]:
            neighbours[0] = self.grid[y +1][x]
        elif y == size_y -1:
            neighbours[0] = 'wall'

        if y > 0 and self.grid[y - 1][x]:
            neighbours[1] = self.grid[y - 1][x]
        elif y == 0:
            neighbours[1] = 'wall'
    
        if x < size_x - 1 and self.grid[y][x + 1]:
            neighbours[3] = self.grid[y][x + 1]
        elif x == size_x -1:
            neighbours[3] = 'wall'

        if x > 0 and self.grid[y][x - 1]:
            neighbours[2] = self.grid[y][x - 1]
        elif x == 0:
            neighbours[2] = 'wall'
        return neighbours
                 

        
    def generate_rooms(self, size_x, size_y, num_rooms,):
        '''
        Generate a (x, y) matrix with n rooms in it
        Note that the matrix should be big enough to contains the number of  rooms
        The rooms are procedurally generated 
        '''                                
        atmospheres = ['no', 'hidrogen', 'oxygen', 'helium', 'carbon dioxide']
        compositions = ['rocky', 'gaseous']                     
        self.grid = [None] * size_y                                                         # Initialize the grid          
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x

        x = 0                                                                               # starting point on a random cell in the left column
        y = random.randrange(self.height)
        room_count = 0
        directions = ['n', 's', 'w', 'e']
        start_room = Room(room_count, "Earth", x, y, atmospheres[2], 1, compositions[0], 5.5, 30)  # generate the starting room
        self.grid[y][x] = start_room
        previous_room = start_room

        # While there are rooms to be created...
        while x < size_x - 1:                                                                 # First loop: If we reach the right column we end the loop
            neighbours = self.get_neighbours(x, y, size_x, size_y)
            direction = directions[random.randint(0,3)]                                       # We pick a random direction
            if not None in neighbours:                                                        # If the room hasn't a spot to be placed break the loop
                break
            elif direction == 'n' and y < size_y - 1 and not self.grid[y +1][x]:              # Calculate the direction of the room to be created
                y += 1
            elif direction == 's' and y > 0 and not self.grid[y -1][x]:   
                y -= 1        
            elif direction == 'w' and x > 0  and not self.grid[y][x- 1]:                           
                x -= 1
            elif direction == 'e' and x < size_x - 1 and not self.grid[y][x + 1]: 
                x += 1
            else:                                                                               # if the spot is taken we go back to the beginning of the loop
                continue                         
            room_name = planets[random.randrange(0, len(planets))]                                              
            room_atm = atmospheres[random.randrange(0, len(atmospheres))]
            room_moons = random.randint(0, 5)
            room_cmp = compositions[random.randrange(0, len(compositions))]
            room_dnsty = random.uniform(0.1, 10)
            room_tmp = random.randint(-121, 975)
            room_count += 1
            room = Room(room_count, room_name, x, y, room_atm, room_moons, room_cmp, room_dnsty, room_tmp) # Create a room in the given direction
            self.grid[y][x] = room                                                              # Save the room in the World grid
            previous_room.connect_rooms(room, direction)                                        # Connect the new room to the previous room
            previous_room = room
        
        while room_count < num_rooms:                                                           # Second loop: While we don't have enough rooms 
            x = random.randrange(self.width)                                                    # We pick a random spot in the grid
            y = random.randrange(self.height)
            if self.grid[y][x]:                                                                 # If we have a room there
                previous_room = self.grid[y][x]                                                 # We repeat the same logic as the first loop
                direction = directions[random.randint(0,3)]
                if direction == 'n' and y < size_y - 1 and not self.grid[y +1][x]: 
                    y += 1
                elif direction == 's' and y > 0 and not self.grid[y -1][x]:   
                    y -= 1        
                elif direction == 'w' and x > 0  and not self.grid[y][x- 1]:                           
                    x -= 1
                elif direction == 'e' and x < size_x - 1 and not self.grid[y][x + 1]: 
                    x += 1
                else:
                    continue
                room_name = planets[random.randrange(0, len(planets))]                                              
                room_atm = atmospheres[random.randrange(0, len(atmospheres))]
                room_moons = random.randint(0, 5)
                room_cmp = compositions[random.randrange(0, len(compositions))]
                room_dnsty = random.uniform(0.1, 10)
                room_tmp = random.randint(-121, 975)
                room_count += 1
                if room_count == num_rooms:                                                      # during the last iteration
                    end_room = Room(room_count, room_name, x, y, room_atm, room_moons, room_cmp, room_dnsty, room_tmp) # we set the end room
                    self.grid[y][x] = end_room
                    previous_room.connect_rooms(end_room, direction)
                    break
                room = Room(room_count, room_name, x, y, room_atm, room_moons, room_cmp, room_dnsty, room_tmp)
                self.grid[y][x] = room
                previous_room.connect_rooms(room, direction)                                    


    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid) # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


#TO TEST THE CLASS COMMENT OUT THIS CODE
# w = World()
# num_rooms = 500
# width = 25
# height = 25
# w.generate_rooms(width, height, num_rooms)
# w.print_rooms()
# one_connection = 0
# two_connection = 0
# three_connection = 0
# four_connection = 0

# for row in w.grid:
#     for room in row:
#         if room:
#             count = [room.n_to, room.s_to, room.e_to, room.w_to]
#             result = count.count(None)
#             if result == 0:
#                 four_connection += 1
#             if result == 1:
#                 three_connection += 1
#             if result == 2:
#                 two_connection += 1
#             if result == 3:
#                 one_connection +=1

# print(f'one connection: {one_connection}')
# print(f'two connection: {two_connection}')
# print(f'three connection: {three_connection}')
# print(f'four connection: {four_connection}')

            
            

# print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
