from __future__ import print_function
import paramiko


def run_cmd_remote(remote_server, cmd, asroot=False):
    """
    run command in a remote server
    :param remote_server:
    :param cmd:
    :param asroot:
    :return:
    """
    ip = str(remote_server["host"])
    name = str(remote_server["user"])
    pwd = str(remote_server["passwrd"])

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    port = 22
    ssh.connect(hostname=ip, port=port, username=name, password=pwd)
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)

    if asroot:
        stdin.write(pwd + "\n")
        stdin.flush()

    print("execute command %s on host %s." % (cmd, ip))
    output = [line.encode("utf-8").strip("\r\n") for line in stdout]
    error = [line.encode("utf-8").strip("\r\n") for line in stderr]

    ssh.close()
    print("output from the command : %s, error from the command : %s." % (str(output), str(error)))
    return output, error


class Cleaner(object):
    def __init__(self, host="localhost", user="root", passwrd=""):
        self.remote_server = {
            "host": host,
            "user": user,
            "passwrd": passwrd
        }

    def clean_tmp_data(self):
        code_path = "/tmp/pai-root/code/"
        cmd = "ls {0}".format(code_path)
        out, err = run_cmd_remote(self.remote_server, cmd, False)
        if len(out) > 0:
            self.clean_paths([code_path + line for line in out])

        log_path = "/tmp/pai-root/log/"
        cmd = "ls {0}".format(log_path)
        out, err = run_cmd_remote(self.remote_server, cmd, False)
        if len(out) > 0:
            self.clean_paths([log_path + line for line in out])

    def clean_docker_cache(self):
        cmd = "sudo docker system prune -a -f"
        run_cmd_remote(self.remote_server, cmd, True)

    def clean_paths(self, paths):
        print("will clean the paths: %s" % str(paths))
        for path in paths:
            cmd = "echo $(( $(date +%s) - $(stat -c %Y {0}) ))".format(path)
            out, err = run_cmd_remote(self.remote_server, cmd)

            if len(err) > 0 or len(out) == 0:
                print("error occurs when cleaning path, the error is: %s" % str(err))
                return

            try:
                past_hour = int(out[0]) / 3600
            except ValueError:
                print("failed to parse the past time: %s" % str(out))
                past_hour = 0

            if past_hour >= 24:
                print("this directory has not been accessed in %s hours and will be deleted." % past_hour)
                cmd = "sudo rm -fr {0}".format(path)
                _, err = run_cmd_remote(self.remote_server, cmd, True)
                if len(err) > 0:
                    print("failed to delete the {0}, the error is : {1}".format(path, err))
