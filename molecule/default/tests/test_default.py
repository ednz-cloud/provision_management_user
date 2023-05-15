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
    """Validate that ubuntu user is not sudoer"""
    etc_sudoers_d_ubuntu = host.file("/etc/sudoers.d/ubuntu")
    assert not etc_sudoers_d_ubuntu.exists

def test_ubuntu_no_ssh(host):
    """Validate that ubuntu user has no authorized_keys"""
    opt_ubuntu_authorized_keys = host.file("/home/ubuntu/.ssh/authorized_keys")
    assert not opt_ubuntu_authorized_keys.exists
