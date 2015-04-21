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
        print d._Dockerfile__dockerfile
        self.assertListEqual(d._Dockerfile__dockerfile, ["FROM ubuntu",
                                                         "# TOW COPY BLOCK FROM MAPPING FILE START",
                                                         "COPY %s %s" % mapping,
                                                         "# TOW COPY BLOCK FROM MAPPING FILE END"])

    def test_add_copy_after_from(self):
        d = Dockerfile("Dockerfile")
        d._Dockerfile__dockerfile = ["FROM ubuntu", "ENTRYPOINT [/bin/sh]"]
        mapping = ("/tets1", "/test2")
        d.add_copy([mapping])
        print d._Dockerfile__dockerfile
        self.assertListEqual(d._Dockerfile__dockerfile, ["FROM ubuntu",
                                                         "# TOW COPY BLOCK FROM MAPPING FILE START",
                                                         "COPY %s %s" % mapping,
                                                         "# TOW COPY BLOCK FROM MAPPING FILE END",
                                                         "ENTRYPOINT [/bin/sh]"])


    def test_add_copy_after_maintainer(self):
        d = Dockerfile("Dockerfile")
        d._Dockerfile__dockerfile = ["FROM ubuntu", "MAINTAINER test","ENTRYPOINT [/bin/sh]"]
        mapping = ("/tets1", "/test2")
        d.add_copy([mapping])
        print d._Dockerfile__dockerfile
        self.assertListEqual(d._Dockerfile__dockerfile, ["FROM ubuntu",
                                                         "MAINTAINER test",
                                                         "# TOW COPY BLOCK FROM MAPPING FILE START",
                                                         "COPY %s %s" % mapping,
                                                         "# TOW COPY BLOCK FROM MAPPING FILE END",
                                                         "ENTRYPOINT [/bin/sh]"])

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
