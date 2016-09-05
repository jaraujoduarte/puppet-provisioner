import uuid
import paramiko

def ssh_bind(target, m_username, m_password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(target, username=m_username, password=m_password)
    return ssh

def ssh_exec(ssh=None, sudo=False, sudo_pass=None, command=None):
    if sudo:
        command = 'sudo %s' % command

    print '---command: %s' % command
    stdin, stdout, stderr = ssh.exec_command(command, get_pty=sudo)

    if sudo:
        stdin.write(sudo_pass + '\n')
        stdin.flush()

    # print 'stdout---'
    for line in iter(lambda: stdout.readline(2048), ""):
        print line.replace(u"\u2018", "'").replace(u"\u2019", "'")

    # print 'stderr---'
    for line in iter(lambda: stderr.readline(2048), ""):
        print line.replace(u"\u2018", "'").replace(u"\u2019", "'")

def sftp_put(ssh=None, local=None, remote=None):
    ftp = ssh.open_sftp()
    ftp.put(local, remote)
    ftp.close()

def sftp_remove(ssh=None, remote=None):
    ftp = ssh.open_sftp()
    ftp.remove(remote)
    ftp.close()

def exec_file(ssh=None, file_path=None,\
    m_sudo=False, m_sudo_pass=None):
    target_script_path = '/tmp/remote-%s' % uuid.uuid4().hex
    sftp_put(ssh, file_path, target_script_path)
    ssh_exec(ssh, command='chmod 777 %s' % target_script_path)
    ssh_exec(ssh, sudo=m_sudo, sudo_pass=m_sudo_pass,\
        command=target_script_path)
    sftp_remove(ssh, target_script_path)
