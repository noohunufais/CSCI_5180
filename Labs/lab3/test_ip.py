import unittest
from validateIP import check_ip

class TestCheckIP(unittest.TestCase):

    def test_invalid_ip(self):

        self.assertFalse(check_ip(''))  # Empty string
        self.assertFalse(check_ip(' '))  # Whitespace
        self.assertFalse(check_ip('256.256.256.256'))  # Out of range
        self.assertFalse(check_ip('1.2.3.4.5'))  # Too many segments
        self.assertFalse(check_ip('192.168.1.'))  # Incomplete segment
        self.assertFalse(check_ip('one.two.three.four'))  # Non-numeric characters

if __name__ == '__main__':
    unittest.main()
