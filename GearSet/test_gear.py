import unittest
from gears import Gear, GearTrain

gear_a = Gear.by_module(2, 40)
gear_b = Gear.by_module(2, 100)
gear_c = Gear.by_module(2, 50)
gear_d = Gear.by_module(2, 150)
gear_e = Gear.by_module(2, 52)
gear_f = Gear.by_module(2, 130)


class TestGearTrain(unittest.TestCase):

    def test_gear_train(self):
        gearset = GearTrain()
        gearset.add_driver(gear_a, 975)
        gearset.attach_to_gear(gear_b, gear_a)
        gearset.attach_to_shaft(gear_c, gear_b)
        gearset.attach_to_gear(gear_d, gear_c)
        gearset.attach_to_shaft(gear_e, gear_d)
        gearset.attach_to_gear(gear_f, gear_e)
        gearset.set_follower(gear_f)
        result = gearset.output_velocity
        self.assertEqual(result, -52)


if __name__ == "__main__":
    unittest.main()
