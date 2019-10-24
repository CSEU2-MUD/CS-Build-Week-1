from django.contrib.auth.models import User
from adventure.models import Player, Room
from map_generator import World
world = World()
world.generate_rooms(25, 25, 500)

Room.objects.all().delete()
starting_room = None
for column in world.grid:
  for room in column:
    if room and room != 'wall':

      r = Room(room.name, room.description)
      r.save()
      if room.n_to:
        r.connectRooms(room.n_to, 'n')
      if room.s_to:
        r.connectRooms(room.s_to, 's')
      if room.e_to:
        r.connectRooms(room.e_to, 'e')
      if room.w_to:
        r.connectRooms(room.w_to, 'n')
      if room.id == 0:
        starting_room = room

players=Player.objects.all()
for p in players:
  p.currentRoom=starting_room.id
  p.save()
