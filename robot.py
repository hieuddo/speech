import ai2thor.controller
import numpy as np

class Robot:

    moves = {'a': 'MoveLeft', 'w': 'MoveAhead', 'd': 'MoveRight', 's': 'MoveBack'}
    rotates = {'j': -15, 'l': 15}
    looks = {'i': -15, 'k': 15}

    def __init__(self,):
        self.rotation = 0
        self.horizon = 30
        
        self.controller = ai2thor.controller.Controller()

        # Kitchens: FloorPlan1 - FloorPlan30
        # Living rooms: FloorPlan201 - FloorPlan230
        # Bedrooms: FloorPlan301 - FloorPlan330
        # Bathrooms: FloorPLan401 - FloorPlan430
            
    def start(self):
        self.controller.start(player_screen_width=1280,
                player_screen_height=720)
        self.controller.reset('FloorPlan29')
        self.event = self.controller.step(dict(action='Initialize', gridSize=0.25))
        self.event = self.controller.step(dict(action='TeleportFull', x=0.5, y=0.9313, z=-0.5, rotation=self.rotation, horizon=self.horizon))
    
    def randomFloor(self):
        floor = np.random.randint(4)
        if floor > 0:
            floor +=1
        sence = floor*100+np.random.randint(1,31)
        return 'FloorPlan' + str(sence)

    def getFrame(self):
        return self.event.cv2img

    def stop(self):
        self.controller.stop()

    def apply(self, action):
        if action in self.moves:
            self.event = self.controller.step(dict(action=self.moves[action]))
            print(self.event.metadata['agent']['position'])
            
        elif action in self.rotates:
            self.rotation += self.rotates[action]
            self.event = self.controller.step(dict(action='Rotate', rotation=self.rotation))
            
        elif action in self.looks:
            self.horizon += self.looks[action]
            self.event = self.controller.step(dict(action='Look', horizon=self.horizon))
        elif action == 'f':
            self.event = self.controller.reset(self.randomFloor())
            self.rotation = self.event.metadata['agent']['rotation']['y']

    def pickup(self, object_name):
        obj_list = self.event.metadata['objects']
        for obj in obj_list:
            if obj['objectType'] == object_name:
                if obj['visible']:
                    self.event = self.controller.step(dict(action='PickupObject', objectId=obj['objectId']))
                else: print('{} is not visible'.format(object_name))
                break

    def dropObject(self):
        self.event = self.controller.step(dict(action='MoveHandAhead', moveMagnitude = 0.2))
        # self.event = self.controller.step(dict(action='DropHandObject'))
        self.event = self.controller.step(dict(action='ThrowObject', moveMagnitude= 50.0))