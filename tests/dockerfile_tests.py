import unittest
from tow.dockerfile import Dockerfile


class DockerfileTest(unittest.TestCase):

    def test_parse_spaced_envs(self):
        d = Dockerfile("Dockerfile")
        d._Dockerfile__dockerfile = ["ENV test 1"]
        envs = d.envs()
        self.assertEqual(envs, {"test": "1"})

    def test_parse_many_envs(self):
        d = Dockerfile("Dockerfile")
        d._Dockerfile__dockerfile = ["ENV test 1", "ENV test2=2", "ENV test3 3"]
        envs = d.envs()
        self.assertEqual(envs, {"test": "1", "test2": "2", "test3": "3"})

    def test_parse_multiline(self):
        d = Dockerfile("Dockerfile")
        d._Dockerfile__dockerfile = ['ENV myName="John Doe" myDog=Rex\\ The\\ Dog \\',
                                     'myCat=fluffy']
        envs = d.envs()
        self.assertEqual(envs, {"myName": "John Doe",
                                "myDog": "Rex\\ The\\ Dog", "myCat": "fluffy"})

    def test_add_copy(self):
        d = Dockerfile("Dockerfile")
        d._Dockerfile__dockerfile = ["FROM ubuntu"]
        mapping = ("/tets1", "/test2")
        d.add_copy([mapping])
        self.assertListEqual(d._Dockerfile__dockerfile, ["FROM ubuntu", "COPY %s %s" % mapping])

    def test_add_copy_before_entrypoint(self):
        d = Dockerfile("Dockerfile")
        d._Dockerfile__dockerfile = ["FROM ubuntu", "ENTRYPOINT [/bin/sh]"]
        mapping = ("/tets1", "/test2")
        d.add_copy([mapping])
        self.assertListEqual(d._Dockerfile__dockerfile, ["FROM ubuntu",
                                                         "COPY %s %s" % mapping, "ENTRYPOINT [/bin/sh]"])

    def test_add_copy_before_entrypoint_or_cmd(self):
        d = Dockerfile("Dockerfile")
        d._Dockerfile__dockerfile = ["FROM ubuntu", "ENTRYPOINT [/bin/sh]", "CMD [/bin/sh]"]
        mapping = ("/tets1", "/test2")
        d.add_copy([mapping])
        self.assertListEqual(d._Dockerfile__dockerfile, ["FROM ubuntu",
                                                         "COPY %s %s" % mapping,
                                                         "ENTRYPOINT [/bin/sh]", "CMD [/bin/sh]"])

    def test_find_entrypoint_or_cmd(self):
        d = Dockerfile("Dockerfile")
        d._Dockerfile__dockerfile = ['FROM ubuntu', 'ENTRYPOINT ["/bin/sh"]', 'CMD ["-c"]']
        self.assertEqual(d.find_entrypoint_or_cmd(), ("/bin/sh", "-c"))

    def test_find_entrypoint_or_cmd_shell_style(self):
        d = Dockerfile("Dockerfile")
        d._Dockerfile__dockerfile = ['FROM ubuntu', 'ENTRYPOINT /bin/sh', 'CMD ["-c"]']
        self.assertEqual(d.find_entrypoint_or_cmd(), ("/bin/sh", "-c"))

    def test_find_entrypoint_or_cmd_cmd_only(self):
        d = Dockerfile("Dockerfile")
        d._Dockerfile__dockerfile = ['FROM ubuntu', 'CMD ["/bin/sh", "-c", "-x"]']
        self.assertEqual(d.find_entrypoint_or_cmd(), (None, "/bin/sh -c -x"))

    def test_find_entrypoint_or_cmd_entrypoint_only(self):
        d = Dockerfile("Dockerfile")
        d._Dockerfile__dockerfile = ['FROM ubuntu', 'ENTRYPOINT ["/bin/sh"]']
        self.assertEqual(d.find_entrypoint_or_cmd(), ("/bin/sh", None))

    def test_find_entrypoint_or_cmd_none(self):
        d = Dockerfile("Dockerfile")
        d._Dockerfile__dockerfile = ['FROM ubuntu']
        self.assertEqual(d.find_entrypoint_or_cmd(), (None, None))
