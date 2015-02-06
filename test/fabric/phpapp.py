import re
from fabric.api import env, run, hide, task
from envassert import detect, file, group, port, process, service, user
from hot.utils.test import get_artifacts


def apache2_is_responding(search):
    with hide('running', 'stdout'):
        wget_cmd = (
            "wget --quiet --output-document - --header='Host: example.com' "
            "http://localhost/"
        )
        homepage = run(wget_cmd)
        if re.search(search, homepage):
            return True
        else:
            return False


@task
def check():
    env.platform_family = detect.detect()

    assert file.exists("/etc/apache2/sites-enabled/example.com.conf"), \
        "/etc/apache2/sites-enabled/example.com.conf does not exist"

    assert port.is_listening(80), "port 80/apache2 is not listening"
    assert port.is_listening(11211), "port 11211/memcached is not listening"

    assert user.exists("memcache"), "user memcache does not exist"

    assert group.is_exists("memcache"), "group memcache does not exist"

    assert process.is_up("apache2"), "apache2 process is not up"
    assert process.is_up("memcached"), "memcached process is not up"

    assert service.is_enabled("apache2"), "redismaster is not enabled"
    assert service.is_enabled("memcached"), "memcached is not enabled"

    assert apache2_is_responding('Welcome to example.com'), \
        "php app did not respond as expected"


@task
def artifacts():
    env.platform_family = detect.detect()
    get_artifacts()
