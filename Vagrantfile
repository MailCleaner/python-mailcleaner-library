Vagrant.require_version ">= 1.9.3"

PROJECT = "python-mailcleaner-library"
PROJECT_DIRECTORY = "/home/vagrant/" << PROJECT
SHARED_FOLDER = PROJECT

vagrant_root = File.dirname(__FILE__)

Vagrant.configure("2") do |config|
  config.vm.box = "packer/debian-8.9.0-amd64"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.hostname = PROJECT

  # Mount project directory
  config.vm.synced_folder ".", PROJECT_DIRECTORY

  config.vm.provider "virtualbox" do |v|
    v.name = PROJECT
    v.customize ["modifyvm", :id, "--memory", 1024, "--cpus", 2, "--vram", 16]
  end
end
