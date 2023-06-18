"""Role testing files using testinfra."""


def test_hosts_file(host):
    """Validate /etc/hosts file."""
    etc_hosts = host.file("/etc/hosts")
    assert etc_hosts.exists
    assert etc_hosts.user == "root"
    assert etc_hosts.group == "root"

def test_ubuntu_user_group(host):
    """Validate ubuntu user and group."""
    ubuntu_group = host.group("ubuntu")
    ubuntu_user = host.user("ubuntu")
    assert ubuntu_group.exists
    assert ubuntu_user.exists
    assert ubuntu_user.group == "ubuntu"
    assert ubuntu_user.shell == "/bin/bash"

def test_ubuntu_sudoer(host):
    """Validate that ubuntu user is sudoer"""
    etc_sudoers_d_ubuntu = host.file("/etc/sudoers.d/ubuntu")
    assert etc_sudoers_d_ubuntu.exists
    assert etc_sudoers_d_ubuntu.user == "root"
    assert etc_sudoers_d_ubuntu.group == "root"
    assert etc_sudoers_d_ubuntu.mode == 0o440
    assert etc_sudoers_d_ubuntu.contains("ubuntu ALL=NOPASSWD:SETENV: ALL")

def test_ubuntu_ssh_authorized_keys(host):
    """Validate that ubuntu user has authorized_keys"""
    opt_ubuntu_authorized_keys = host.file("/home/ubuntu/.ssh/authorized_keys")
    assert opt_ubuntu_authorized_keys.exists
    assert opt_ubuntu_authorized_keys.user == "ubuntu"
    assert opt_ubuntu_authorized_keys.group == "ubuntu"
    assert opt_ubuntu_authorized_keys.mode == 0o600
    assert opt_ubuntu_authorized_keys.contains("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIClfmTk73wNNL2jwvhRUmUuy80JRrz3P7cEgXUqlc5O9 ubuntu@instance")
