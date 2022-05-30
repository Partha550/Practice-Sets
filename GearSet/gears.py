from math import pi


class Arm:

    def __init__(self, length):
        self.length = length


class Gear:

    def __init__(self, diameter: float, teeth: int, direction: str = 'external'):
        self.diameter = diameter
        self.teeth = teeth
        self.direction = direction
        self.module = (self.diameter/self.teeth)

    @classmethod
    def by_module(cls, module: float, diameter: float, direction: str = 'external'):
        teeth = (diameter/module)
        if not float(teeth).is_integer():
            raise ValueError("Invalid input")
        return cls(diameter, int(teeth), direction)

    def __str__(self):
        return f"{self.direction} Gear, M-{self.module}"


class GearTrain:

    def __init__(self, gear):
        self.gears = [gear]
        gear.fixed_shaft = True
        gear.mesh_attachment = []
        gear.shaft_attachment = []
        self.driver = None
        self.follower = None
        self.velocity_ratio = None

    @staticmethod
    def _equal_module(gear_1, gear_2):
        if gear_1.module == gear_2.module:
            return True
        return False

    def add_gear_in_mesh(self, new_gear, with_, fixed_shaft=True, is_fixed=False):
        if with_ not in self.gears:  # Checks if the gear is already exists in geartrain. 
            raise ValueError("The gear is not in gearset")
        else:
            if self._equal_module(new_gear, with_): # Check for module equality
                self.gears.append(new_gear)
                new_gear.mesh_attachment = [with_]
                with_.mesh_attachment.append(new_gear)
                new_gear.fixed_shaft = fixed_shaft
                new_gear.is_fixed = is_fixed
            else:
                raise ValueError(f"modules of two gears are different")

    def add_gear_with_shaft(self, new_gear, with_):
        if with_ not in self.gears:
            raise ValueError("The gear is not in gearset")
        else:
            self.gears.append(new_gear)
            with_.shaft_attachment.append(new_gear)
            new_gear.shaft_attachment = [with_]

    def add_driver(self, gear, velocity):
        self.driver = gear
        self.gears.append(gear)
        self.driver.velocity = velocity

    def set_follower(self, gear):
        self.follower = gear

    @property
    def output_velocity(self):
        if self.follower == None:
            raise ValueError("follower isn't defined yet")
        return self.follower.velocity

