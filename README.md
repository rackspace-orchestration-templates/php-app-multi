[![Circle CI](https://circleci.com/gh/rackspace-orchestration-templates/php-app-multi.png?style=badge)](https://circleci.com/gh/rackspace-orchestration-templates/php-app-multi)
Description
===========

Heat template to deploy a load balancer and multiple servers running a PHP app under apache


Instructions
===========

#### Getting Started
If you're new to PHP, the [Getting
Started](http://www.php.net/manual/en/getting-started.php) page can walk you
through the basics of PHP and it's uses.

#### Logging in via SSH
The private key provided in the passwords section can be used to login as
root via SSH. We have an article on how to use these keys with [Mac OS X and
Linux](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-linuxmac)
as well as [Windows using
PuTTY](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-windows).

#### Deploying Your Code
If your deployment has multiple application servers, deployment tools such as
Capistrano, Phing, or even git can simplify the deployment process. It's best
to evaluate all options independently to determine which tool works best for
your use case. There are other methods for deployment including using
configuration and infrastructure management tools like
[Chef](http://docs.opscode.com/resource_deploy.html#deploy-strategies).

#### Details of Your Setup
This deployment was stood up using
[chef-solo](http://docs.opscode.com/chef_solo.html). Once the deployment is
up, chef will not run again, so it is safe to modify configurations.

[PHP](http://www.php.net/) was installed using the packaged version for your
operating system. Newer versions of PHP will be available with newer versions
of the operating system. We recommend using the packaged version as opposed
to a source based installation for easier long term managmement, patching,
and supportability.

All web content will be served by [Apache](http://httpd.apache.org/).  The
configuration can be found in /etc/apache2/sites-enabled. The name of the
configuration file will be the same as the name of the site provided as a
part of this deployment. Any changes made to this configuration will require
a restart of Apache. By default, the Document Root for your site will be
/var/www/vhosts/application/.

[Memcached](http://memcached.org/) is installed to handle object caching. By
default, Memcached is configured to listen on localhost, port 11211.
Memcached is most commonly used to cache object information so that they can
be called from memory as opposed to querying a backend database. The
configuration can be found in /etc/memcached.conf. Any changes made to the
configuration file will require a the memcached service to be restarted.

#### Adding PHP Modules or Extensions
There are several options for adding support to PHP. We recommend leveraging
as many packaged modules as possible. Use the system package manager to
search for an install modules. Here's an example of how to search for
availalbe modules of PHP 5 on Ubuntu:
```bash
root@app01:~# apt-cache search php5-
php5-cgi - server-side, HTML-embedded scripting language (CGI binary)
php5-cli - command-line interpreter for the php5 scripting language
php5-common - Common files for packages built from the php5 source
php5-curl - CURL module for php5
php5-dbg - Debug symbols for PHP5
php5-dev - Files for PHP5 module development
php5-gd - GD module for php5
php5-gmp - GMP module for php5
php5-ldap - LDAP module for php5
php5-mysql - MySQL module for php5
...
```
Once you find the appropriate package, the package manager can be used to
handle the installation. Here's an example on how we would install the
php5-gd package on Ubuntu:
```bash
apt-get install -y php5-gd
```
If you're looking to install something that is not found in the default
repositories, you can use [PECL](http://pecl.php.net/),
[PEAR](http://pear.php.net/), or
[phpize](http://php.net/manual/en/install.pecl.phpize.php) to complete the
installation. Follow any instructions provided with the application you are
installing for more detail on how to best install the necessary modules or
extensions.

#### Updating PHP
Since the PHP installation was done using the package manager for the
operating system, the update can also be performed by the package manager. If
you're looking for a different major or minor version of PHP, you may want to
consider running a different version of the operating system. Most operating
systems lock in specific major, minor, and release versions, and they only
release updates for bugs or security fixes.

#### Scaling Out
If you'd like to grow this configuration, the easiest way would be to take a
snapshot of one of your PHP server and [build a new server with that
image](http://www.rackspace.com/knowledge_center/article/cloud-essentials-4-creating-an-image-backup-cloning-and-restoring-a-server-from-a-saved).
Once the new server is up, [add the new server to your load
balancer](http://www.rackspace.com/cloud/load-balancing/screenshots/).


Requirements
============
* A Heat provider that supports the following:
  * OS::Heat::ResourceGroup
  * OS::Nova::KeyPair
  * Rackspace::Cloud::LoadBalancer
* An OpenStack username, password, and tenant id.
* [python-heatclient](https://github.com/openstack/python-heatclient)
`>= v0.2.8`:

```bash
pip install python-heatclient
```

We recommend installing the client within a [Python virtual
environment](http://www.virtualenv.org/).

Parameters
==========
Parameters can be replaced with your own values when standing up a stack. Use
the `-P` flag to specify a custom parameter.

* `server_hostname`: Server Name (Default: php)
* `https_port`: HTTPS Port (Default: 443)
* `image`: Required: Server image used for all servers that are created as a part of
this deployment.
 (Default: Ubuntu 12.04 LTS (Precise Pangolin) (PVHVM))
* `child_template`: Location of child template for provisioning PHP web nodes. (Default: https://raw.github.com/rackspace-orchestration-templates/php-app-multi/master/php-app-single.yaml)
* `load_balancer_hostname`: Hostname for the Load Balancer (Default: PHP-Load-Balancer)
* `repo`: Optional: URL to your git repository. Use the https syntax for public
repositories, use git@ syntax for private repositories.
 (Default: '')
* `memcached_size`: Memcached memory size limit (Default: 128)
* `flavor`: Required: Rackspace Cloud Server flavor to use. The size is based on the
amount of RAM for the provisioned server.
 (Default: 4 GB General Purpose v1)
* `packages`: Optional: Additional system packages to install. For a list of available
packages, see: http://packages.ubuntu.com/precise/allpackages
 (Default: '')
* `server_count`: Required: Number of servers to spin up as a part of this deployment.
 (Default: 2)
* `kitchen`: URL for the kitchen to use (Default: https://github.com/rackspace-orchestration-templates/php-app-multi)
* `http_port`: HTTP Port (Default: 80)
* `url`: URL for your site (Default: http://example.com)
* `destination`: Path to setup your application on your servers. (Default: /var/www/vhosts/application)
* `public`: The public facing directory of your application relative to the
destination.
 (Default: /)
* `deploy_key`: Optional: If you specified a private repository, provide your private
deploy key here.
 (Default: '')
* `chef_version`: Version of chef client to use (Default: 11.12.8)
* `revision`: Optional: Git Branch/Ref to deploy. Default: HEAD
 (Default: HEAD)

Outputs
=======
Once a stack comes online, use `heat output-list` to see all available outputs.
Use `heat output-show <OUTPUT NAME>` to get the value of a specific output.

* `private_key`: SSH Private Key 
* `load_balancer_ip`: Load Balancer IP 
* `server_public_ips`: Server IPs 

For multi-line values, the response will come in an escaped form. To get rid of
the escapes, use `echo -e '<STRING>' > file.txt`. For vim users, a substitution
can be done within a file using `%s/\\n/\r/g`.
