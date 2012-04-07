# World is an ordered list of chunks.
# current chunk is where the current player is
# simulate the current, previous and next chunks

from entity import Entity
from panda3d.core import Point2, Point3, BoundingBox, BoundingSphere, Vec3
from player import Player
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
chunklength = 200



class World():
  def __init__(self, app):

    self.player = Player(app)
    self.player.initialise()

    self.chunks = list()

    self.worldSize = 6
     
    self.chunks.append(Chunk(app, 0, self.player, start = True)) 

    for i in range (0, self.worldSize-1):
      self.chunks.append(Chunk(app, i, self.player))

    self.chunks.append(Chunk(app, self.worldSize-1, self.player,end = True))
    
    self.currentChunk = 0

    # the lower rail
    shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
    self.groundNode = BulletRigidBodyNode('Ground')
    self.groundNode.addShape(shape)
    self.groundnp = render.attachNewNode(self.groundNode)
    self.groundnp.setPos(0, 0, -6)
    app.bw.attachRigidBody(self.groundNode)

    shape2 = BulletPlaneShape(Vec3(0, 0, -1), 1)
    self.skyNode = BulletRigidBodyNode('Sky')
    self.skyNode.addShape(shape2)
    self.skynp = render.attachNewNode(self.skyNode)
    self.skynp.setPos(0, 0, 6)
    app.bw.attachRigidBody(self.skyNode)

  # add something to a chunk  
  def addEntity(self, entity, chunk=None):
    if chunk == None:
      chunk = self.currentChunk
    self.chunks[chunk].addEntity(entity)


  def update(self, timer):
    self.player.update(timer)
    self.chunks[self.currentChunk].update(timer)

    if self.currentChunk > 0:
      self.chunks[self.currentChunk-1].update(timer)
    if self.currentChunk < self.worldSize:
      self.chunks[self.currentChunk+1].update(timer)

class Chunk():
  chunklength = 200
  def __init__(self, app, rank, player, start=False, end=False):
    # store enemies, bits of terrain and projectiles in entities
    # so we can do some collision detection
    self.player = player
    self.rank = rank
    self.app = app
    self.entities = list()

    self.bg = self.app.loadObject("stars", depth=100, scaleX=200, scaleY=200.0, pos=Point2(rank*200.0,0))
    # indestructible rails top and bottom
    for i in range(-10, 10):
      self.entities.append(Rail(app, rank * chunklength + i * 10, top=1))
      self.entities.append(Rail(app, rank * chunklength + i * 10, top=-1))

    self.entities.append(Wall(app, Point2(0,0)))
    if(start):
      #put a wall at the start
      startrail1 = Rail(app, -100, top=0.6)
      startrail1.obj.setHpr(Point3(0,0,90))
      self.entities.append(startrail1)
      startrail2 = Rail(app, -100, top=0)
      startrail2.obj.setHpr(Point3(0,0,90))
      self.entities.append(startrail2)
      startrail3 = Rail(app, -100, top=-0.6)
      startrail3.obj.setHpr(Point3(0,0,90))
      self.entities.append(startrail3)

      shape = BulletPlaneShape(Vec3(1, 0, 0), 1)
      self.startRailNode = BulletRigidBodyNode('startRail')
      self.startRailNode.addShape(shape)
      self.startrailnp = render.attachNewNode(self.startRailNode)
      self.startrailnp.setPos(-90, 0, 0)
      app.bw.attachRigidBody(self.startRailNode)

      # load a background for unplayable area
      prebg = self.app.loadObject("stars", depth=100, scaleX=200, scaleY=200.0, pos=Point2(-200,0))

    if(end):
      #put a door at the end
      return
    
  def update(self, timer):
    # this has all the bits of wall
    # maybe the enemies too
    # possibly projectiles.
    for entity in self.entities:
      entity.update(timer)

  def addEntity(self, entity):
    self.entities.append(entity)

class Rail(Entity):
  def __init__(self, app, posX, top=1):
    super(Rail, self).__init__()

    self.obj = app.loadObject("rail", depth=55, scaleX=10.0, scaleY=1.0, pos=Point2(0+posX,top*14.5))

  # Rails don't do much 
  def update(self, timer):
    return

class Wall(Entity):
  def __init__(self, app, pos):
    super(Wall, self).__init__()
    self.health = 100

    shape = BulletBoxShape(Vec3(0.25,1.0,0.25))
    self.bnode = BulletRigidBodyNode()
    self.bnode.addShape(shape)
    self.np = app.render.attachNewNode(self.bnode)
    self.np.setPos(-80,20,0)
    app.bw.attachRigidBody(self.bnode)

    self.obj = app.loadObject("wall", depth = -1)
    self.obj.reparentTo(self.np)
    self.obj.setScale(0.5)

  def update(self, timer):
    if self.health < 0:
      self.obj.remove()



