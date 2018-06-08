# config.py file
c = get_config()

import os
import dockerspawner
pjoin = os.path.join
notebook_dir = '/notebooks'
network_name = os.environ['DOCKER_NETWORK_NAME']

c.JupyterHub.log_level = 10

runtime_dir = os.path.join('/srv/jupyterhub')
ssl_dir = pjoin(runtime_dir, 'ssl')
if not os.path.exists(ssl_dir):
   os.makedirs(ssl_dir)

# Allows multiple single-server per user
c.JupyterHub.allow_named_servers = True

# The docker instances need access to the Hub, so the default loopback port doesn't work:
from jupyter_client.localinterfaces import public_ips
c.JupyterHub.hub_ip = public_ips()[0]
print("IP is now ",c.JupyterHub.hub_ip)
c.JupyterHub.port = 443
c.JupyterHub.ssl_key = pjoin(ssl_dir, 'ssl.key')
c.JupyterHub.ssl_cert = pjoin(ssl_dir, 'ssl.pem')

# put the JupyterHub cookie secret and state db
# in /var/run/jupyterhub
c.JupyterHub.cookie_secret_file = pjoin(runtime_dir, 'cookie_secret')
#c.JupyterHub.db_url = pjoin(runtime_dir, 'jupyterhub.sqlite')

# use GitHub OAuthenticator for local users
#c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
#c.GitHubOAuthenticator.oauth_callback_url = 'https://scott.ai/hub/oauth_callback'
#c.GitHubOAuthenticator.client_id = '91b6655938d7c5baba1c'
#c.GitHubOAuthenticator.client_secret = '695cf311902e5aa13a0ae904c2b2e8b13040c7a0'


# use Google OAuthenticator for local users
c.JupyterHub.authenticator_class = 'oauthenticator.GoogleOAuthenticator'
c.GoogleOAuthenticator.oauth_callback_url = 'https://scott.ai/hub/oauth_callback'
c.GoogleOAuthenticator.client_id = '173278311477-ehlhp48bv613ivolkd0cms4u79voa0b6.apps.googleusercontent.com'
c.GoogleOAuthenticator.client_secret = 'G_SKaQIjYGOWw6rV3cBwJ1QD'

# create system users that don't exist yet
c.LocalAuthenticator.create_system_users = True

# specify users and admin
c.Authenticator.whitelist = {'drscott173', 'scott.penberthy@gmail.com'}
c.Authenticator.admin_users = {'drscott173', 'scott.penberthy@gmail.com'}

# no memory limit
#c.Spawner.notebook_dir = 'notebooks'
#c.Spawner.mem_limit = '128G'
        
# Connect containers to this Docker network
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Spawn notebooks in a container
# Pass the network name as argument to spawned containers
# and ensure we use Nvidia for GPU access

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = 'gcr.io/udacity-fcn/singleuser'
c.DockerSpawner.extra_host_config = {"runtime":"nvidia",
                                     'network_mode': network_name }

# use safe volume names
def use_safe_volumes(template, spawner):
   return template.format(username=spawner.escaped_name)

c.DockerSpawner.format_volume_name = use_safe_volumes
c.DockerSpawner.volumes = {'jh-user-{username}': notebook_dir }

# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True

# Whitlelist users and admins
c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()
c.JupyterHub.admin_access = True

# Use PostGres
import os;
c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
       host=os.environ['POSTGRES_HOST'],
       password=os.environ['POSTGRES_PASSWORD'],
       db=os.environ['POSTGRES_DB'],
   )



# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080
