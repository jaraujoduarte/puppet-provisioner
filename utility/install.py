import os
import io
import yaml
from jinja2 import Environment, FileSystemLoader
import lib.misc as misc

def main():
    # Get input
    with open('input/install.yml') as input_file:
        data = input_file.read()

    my_input = yaml.load(data)

    # PREPS
    env = Environment(loader=FileSystemLoader('templates'))
    install_template = env.get_template('install_script.sh')
    install_template.render(dic=my_input)

    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    with io.open('tmp/puppet-provisioner.sh', 'w', newline="\n") as f:
        f.write(install_template.render(dic=my_input))

    # ON THE TARGET
    print 'On the target node...'
    ssh = misc.ssh_bind(my_input['target'],\
        my_input['ssh_username_target'], my_input['ssh_password_target'])

    # Provision puppet
    misc.exec_file(ssh=ssh, file_path='tmp/puppet-provisioner.sh',\
        m_sudo=True, m_sudo_pass=my_input['ssh_password_target'])

    # Create rol file
    for rol in my_input['roles']:
        misc.ssh_exec(ssh, sudo=True, sudo_pass=my_input['ssh_password_target'],\
            command='/bin/touch /%s.fact' % rol)

    # ON THE MASTER
    print 'On the puppet master...'
    ssh = misc.ssh_bind(my_input['puppet_master'],\
        my_input['ssh_username_master'], my_input['ssh_password_master'])

    misc.ssh_exec(ssh, sudo=True, sudo_pass=my_input['ssh_password_target'],\
        command='/opt/puppetlabs/bin/puppet cert sign %s' % my_input['target'])

if __name__ == '__main__':
    main()
