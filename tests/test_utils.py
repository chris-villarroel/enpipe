import unittest
import os
import yaml
from epipe import epipe

class TestUtils(unittest.TestCase):

    def setUp(self):
        # This method is called before each test
        self.fixture_dir = os.path.join(os.getcwd(), 'tests', 'fixtures')
        os.makedirs(self.fixture_dir, exist_ok=True)

        # To test this function, you'll need a sample YAML config file and .env file
        self.sample_yaml_path = os.path.join(self.fixture_dir, 'sample.yaml')
        with open(self.sample_yaml_path, 'w') as f:
            yaml.safe_dump({'version': '{version}'}, f)

        self.sample_env_path = os.path.join(self.fixture_dir, '.env')
        with open(self.sample_env_path, 'w') as f:
            f.write("version=1.0.0\n")

    def test_read_config(self):
        config = epipe.read_config(self.sample_yaml_path)
        self.assertEqual(config['version'], '1.0.0')

    def test_read_env_variable(self):
        version = epipe.read_env_variable(self.sample_env_path, 'version')
        self.assertEqual(version, '1.0.0')



if __name__ == "__main__":
    unittest.main()

