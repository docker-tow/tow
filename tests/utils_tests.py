import unittest
from tow.utils import get_env_args
import os


class UtilsTest(unittest.TestCase):

    def test_get_env_args(self):
        envs = get_env_args(["-e", "test=1"])
        self.assertEqual(envs, {"test": "1"})

    def test_get_env_args_without_val(self):
        os.environ["test"] = "1"
        envs = get_env_args(["-e", "test"])
        self.assertEqual(envs, {"test": "1"})

    def test_get_env_args_by_envs(self):
        envs = get_env_args(["--env", "test=1"])
        self.assertEqual(envs, {"test": "1"})

    def test_get_env_args_by_envs_without_val(self):
        os.environ["test"] = "1"
        envs = get_env_args(["--env", "test"])
        self.assertEqual(envs, {"test": "1"})

    def test_get_env_args_by_envs_array(self):
        os.environ["test"] = "1"
        envs = get_env_args(["--env", "test", "test2=2"])
        self.assertEqual(envs, {"test": "1", "test2": "2"})

    def test_get_env_args_by_envs_array_and_start_next_command(self):
        os.environ["test"] = "1"
        envs = get_env_args(["--env", "test", "test2=2", "-v", "/t:/t"])
        self.assertEqual(envs, {"test": "1", "test2": "2"})
