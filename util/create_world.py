from django.contrib.auth.models import User
from adventure.models import Player, Room
from map_generator import World
world = World()
world.generate_rooms(25, 25, 500)

Room.objects.all().delete()

for column in world.grid:
  for room in column:
    if room and room != 'wall':
      r = Room(room.name, room.description, room.n_to, room.s_to, room.e_to, room.w_to)
      r.save()
      if room.id = 0:
        for p in players:
          p.currentRoom=r.id
          p.save()

