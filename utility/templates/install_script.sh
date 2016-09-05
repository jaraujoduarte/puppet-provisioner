version=$(/usr/local/bin/puppet --version)
# If puppet is not installed
if [ -z $version ]; then
  # Backup and remove original yum repos
  # It is assumed that there is no internet access for the node
  /bin/cp -R /etc/yum.repos.d/ /
  /bin/rm -rf /etc/yum.repos.d/*

  # Create workspace
  WORKSPACE=/home/{{ dic['ssh_username_target'] }}/puppet_install
  mkdir $WORKSPACE
  echo 'created workspace'

  # Download install script
  curl -k -o $WORKSPACE/install.bash https://{{ dic['puppet_master'] }}:8140/packages/current/install.bash
  echo 'downloaded install script'

  # Set script as executable
  chmod 777 $WORKSPACE/install.bash
  echo 'install script set as executable'

  # Execute script
  sudo $WORKSPACE/install.bash
  echo 'puppet agent installed'
else
  echo 'puppet already installed on node'
fi
