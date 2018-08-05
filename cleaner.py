import paramiko


def run_cmd_remote(remote_server, cmd, asroot=False):
    """
    run command in a remote server
    :param remote_server:
    :param cmd:
    :param asroot:
    :return:
    """
    ip = str(remote_server["ip"])
    name = str(remote_server["name"])
    pwd = str(remote_server["password"])

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    port = 22
    ssh.connect(hostname=ip, port=port, username=name, password=pwd)
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)

    if asroot:
        stdin.write(pwd + "\n")
        stdin.flush()

    print("execute command %s on host %s." % (cmd, ip))
    output = ""
    for msg in stdout:
        output += msg
    error = ""
    for msg in stderr:
        error += msg
    ssh.close()
    print("output from the command : %s error from the command : %s." % (output, error))
    return output, error


def clean_docker_cache(remote_server):
    cmd = "sudo docker system prune -a -f"
    run_cmd_remote(remote_server, cmd, True)


def clean_paths(remote_server, paths):
    print("will clean the paths: %s" % str(paths))
    for path in paths:
        cmd = "$(( $(data +%s) - $(stat -c %Y {0}) ))".format(path)
        stdout, stderr = run_cmd_remote(remote_server, cmd)
        output = stdout.read().encode('utf-8').strip("\n")
        try:
            past_hour = int(output) / 3600
        except ValueError:
            print("failed to parse the past time: %s" % output)
            past_hour = 0

        if past_hour >= 24:
            print("this directory has not been accessed in %s hours and will be deleted." % past_hour)
            cmd = "sudo rm -fr {0}".format(path)
            stdout, stderr = run_cmd_remote(remote_server, cmd, True)
            error = stderr.read()
            if len(error) > 0:
                print("failed to delete the {0}, the error is : {1}".format(path, error))


def clean_tmp_dir(remote_server):
    cmd = "ls /tmp/pai-root/code"
    stdout, stderr = run_cmd_remote(remote_server, cmd, False)

    lines = [line.encode('utf-8').strip("\n") for line in stdout]
    clean_paths(lines)

    cmd = "ls /tmp/pai-root/log"
    stdout, stderr = run_cmd_remote(remote_server, cmd, False)

    lines = [line.encode('utf-8').strip("\n") for line in stdout]
    clean_paths(lines)


if __name__ == "__main__":
    print("start to run the cleaner")
    config = {"ip": "10.190.151.29", "name": "zhdo", "password": "Pass_word"}
    clean_docker_cache(config)
