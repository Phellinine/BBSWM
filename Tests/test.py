import unittest
import desktop_message


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


class DesktopMessage(unittest.TestCase):
    def test_simple(self):
        desktop_message.simple("test", "sss")
        print("dd")
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
