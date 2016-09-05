# Example custom fact to be picked up by puppet
# The produced file would be placed by the utility/install.py script
Facter.add('web_server') do
  setcode do
    File.exist? "/web_server.fact"
  end
end
