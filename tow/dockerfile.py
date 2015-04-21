"""
TODO: add comments
"""
import re


class Dockerfile(object):

    def __init__(self, dockerfile_path):
        self.__dockerfile_path = dockerfile_path
        self.__dockerfile = None
        self.__envs = {}

    def _parse_dockerfile(self):
        if not self.__dockerfile:
            with open(self.__dockerfile_path, "r") as df:
                self.__dockerfile = [line.strip() for line in df.readlines()]

    def _parse_spaced_envs(self, env_line):
        envs = env_line.split(" ")
        env_name = envs[0]
        env_var = " ".join(envs[1:])
        return {env_name: env_var}

    def _parse_multiline_envs(self, env_line):
        result = {}
        while env_line and env_line != "\\":
            equal_index = re.search("\w+=", env_line)
            env_name = equal_index.group().split("=")[0]
            env_line = env_line[len(equal_index.group()):]
            # if starts from " parse text between quotes
            if env_line.startswith("\""):
                env_var = re.search("([\"'])(?:(?=(\\\\?))\\2.)*?\\1",
                                    env_line).group()
                env_line = env_line[len(env_var):]
                # remove around quotes
                env_var = re.sub(r'^"|"$', '', env_var)
            else:
                # read until space
                env_var_match = re.search(".*([^\\\\]\\s)",
                                          env_line)
                # if space doesn't found that mean that it's the last
                # variable in string
                if not env_var_match:
                    env_var = env_line
                else:
                    env_var = env_var_match.group()
                env_line = env_line[len(env_var):]
                env_var = env_var.strip()

            env_line = env_line.strip()
            result[env_name] = env_var

        is_multiline_envs = env_line.endswith("\\")
        return (result, is_multiline_envs)

    def _parse_exec_line(self, exec_line):
        if exec_line:
            command = exec_line[exec_line.find(" ") + 1:]
            # Handle array command
            if command.startswith("[") and command.endswith("]"):
                command = command[1:-1]
                return " ".join([sh.strip()[1:-1] for sh in command.split(",")])
            else:  # It's just shell notation
                return command.strip()
        return None

    def envs(self):
        if not self.__envs:
            self._parse_dockerfile()

            is_multiline_envs = False
            for dockerfile_line in self.__dockerfile:
                env_vars = {}
                dl = dockerfile_line.strip()
                if is_multiline_envs:
                    (env_vars, is_multiline_envs) = \
                        self._parse_multiline_envs(dl)
                elif dl.startswith("ENV"):
                    # First of all parse single line env variables with
                    # space separator
                    env_vars_line = dl[len("ENV"):].strip()
                    if not re.match("^\\w+=", env_vars_line):
                        env_vars = self._parse_spaced_envs(env_vars_line)
                    else:
                        (env_vars, is_multiline_envs) = \
                            self._parse_multiline_envs(env_vars_line)

                self.__envs.update(env_vars)
        return self.__envs

    def add_copy(self, file_mapping):
        copy_block = []
        for fm in file_mapping:
            src = fm[0]
            dst = fm[1]
            mask = fm[2] if len(fm) > 2 else None
            copy_block.append("COPY %s %s" % (src, dst))
            if mask:
                copy_block.append("RUN chmod %s %s" % (mask, dst))

        if copy_block:
            copy_block = ["# TOW COPY BLOCK FROM MAPPING FILE START"] +\
                copy_block +\
                ["# TOW COPY BLOCK FROM MAPPING FILE END"]

        position = len(self.__dockerfile)

        for i, dockerfile_line in enumerate(self.__dockerfile):
            if dockerfile_line.startswith("FROM") or dockerfile_line.startswith("MAINTAINER"):
                position = i

        position = position + 1
        self.__dockerfile = self.__dockerfile[:position] + copy_block + self.__dockerfile[position:]

    def find_entrypoint_or_cmd(self):
        """ This command find entrypoint or cmd blocks and
        return them in shell style
        """
        cmd = None
        entrypoint = None
        for dockerfile_line in self.__dockerfile:
            if dockerfile_line.startswith("CMD"):
                cmd = dockerfile_line
            elif dockerfile_line.startswith("ENTRYPOINT"):
                entrypoint = dockerfile_line
        return (self._parse_exec_line(entrypoint), self._parse_exec_line(cmd))

    def replace_entrypoint_or_cmd_by_tow_cmd(self, cmd):
        self.__dockerfile = [dockerfile_line
                             for dockerfile_line in self.__dockerfile
                             if (not dockerfile_line.startswith("CMD") and
                                 not dockerfile_line.startswith("ENTRYPOINT"))]

        position = len(self.__dockerfile)
        for i, dockerfile_line in enumerate(self.__dockerfile):
            if dockerfile_line.startswith("EXPOSE"):
                position = i
                break
        self.__dockerfile = self.__dockerfile[:position] + \
            ["ENTRYPOINT %s" % cmd] + self.__dockerfile[position:]

    def save(self, dockerfile_path):
        with open(dockerfile_path, "w+") as df:
            df.write("\n".join(self.__dockerfile))
