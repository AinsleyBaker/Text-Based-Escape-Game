import unittest
import EscapeGame as game

class TestEscapeGame(unittest.TestCase):

    def setUp(self):
        """Setting up testing environment"""
        game.load_rooms() 
        self.ITEM_COST = {
        "usb": 10,
        "book": 20,
        "stool": 40,
        "mop": 10,
        "crowbar": 20   }

    def test_describe_items(self):
        """Unittest for describe function"""
        expected = "You can see: table stool($40)"
        self.assertEqual(game.describe_items("central"), expected)
        expected = "You can see: mop($10) crowbar($20)"
        self.assertEqual(game.describe_items("janitor"), expected)
        expected = "You can see: computer"
        self.assertEqual(game.describe_items("computer"), expected)
        expected = "You can see: bookshelf"
        self.assertEqual(game.describe_items("reading"), expected)

    """Unittest for each move function"""
    def test_move_central(self):
        self.assertEqual(game.move_central("north"), "reading")
        self.assertEqual(game.move_central("east"), "janitor")
        self.assertEqual(game.move_central("south"), "")

    def test_move_janitor(self):
        self.assertEqual(game.move_janitor("west"), "central")
        self.assertEqual(game.move_janitor("north"), "")

    def test_move_computer(self):
        self.assertEqual(game.move_computer("east"), "reading")
        self.assertEqual(game.move_computer("west"), "")

    def test_move_reading(self):
        states = {"door_locked": True, "end_locked": True}

        self.assertEqual(game.move_reading("west", states), "")
        self.assertEqual(game.move_reading("south", states), "central")

        states["door_locked"] = False
        self.assertEqual(game.move_reading("west", states), "computer")

        states["end_locked"] = False
        self.assertEqual(game.move_reading("east", states), "end")

    def test_get(self):
        """Unittest for get function"""
        carrying = []
        cash = 100

        # Test picking up a valid item with enough cash
        cash = game.get("stool", carrying, cash, "central")
        self.assertEqual(carrying, ["stool"])
        self.assertEqual(cash, 60)

        # Test picking up a non-existent item
        cash = game.get("chair", carrying, cash, "central")
        self.assertEqual(carrying, ["stool"])
        self.assertEqual(cash, 60)

        # Test picking up an item when inventory is full
        carrying = ["book", "crowbar", "usb"]
        cash = game.get("stool", carrying, cash, "central")
        self.assertEqual(carrying, ["book", "crowbar", "usb"])
        self.assertEqual(cash, 60)

        # Test picking up an item with not enough cash
        cash = 20
        carrying = []
        cash = game.get("stool", carrying, cash, "central")
        self.assertEqual(carrying, [])
        self.assertEqual(cash, 20)

    def test_drop(self):
        """Unittest for drop function"""
        room = "central"
        carrying = ["usb", "crowbar", "book"]
        cash = 60

        # Test dropping a valid item
        cash = game.drop("book", carrying, cash, room)
        self.assertEqual(carrying, ["usb", "crowbar"])
        self.assertEqual(cash, 70)

        # Test dropping an item not in inventory
        cash = game.drop("mop", carrying, cash, room)
        self.assertEqual(carrying, ["usb", "crowbar"])
        self.assertEqual(cash, 70)

    def test_file_read(self):
        """Unittest for file_read function"""

        # Test a valid start position
        expected = "Find a computer to insert usb drive."
        self.assertEqual(game.file_read("5").strip().replace("\n", " "), expected)
        expected = "You bump your head on the projector and fall off the stool."
        self.assertEqual(game.file_read("10").strip().replace("\n", " "), expected)

        #Test an invalid start position
        expected = "Invalid start position: Must be an integer between 1-19"
        self.assertEqual(game.file_read("0"), expected)
        self.assertEqual(game.file_read("20"), expected)
        self.assertEqual(game.file_read("dog"), expected)




if __name__ == "__main__":
    unittest.main()