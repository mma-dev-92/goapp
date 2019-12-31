import unittest
import os


if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.getcwd(), 'test')
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
