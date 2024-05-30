# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, random, re
import inspect
from os import environ as env

from novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session


prod_flavor = "ssc.medium"
dev_flavor = "ssc.xlarge"
private_net = "UPPMAX 2024/1-4 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "Ubuntu 20.04 - 2023.12.07"

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print ("user authorization completed.")

image = nova.glance.find_image(image_name)

prod_flavor = nova.flavors.find(name=prod_flavor)
dev_flavor = nova.flavors.find(name=dev_flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
userdata=""
cfg_file_path =  os.getcwd()+'/cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    with open(cfg_file_path, "r") as f:
        userdata = f.read()
else:
    sys.exit("cloud-cfg.txt is not in current working directory")

secgroups = ['default']

print ("Creating instances ... ")
instance_prod = nova.servers.create(name="prod_server_1337", image=image, flavor=prod_flavor, key_name='alex',userdata=userdata, nics=nics,security_groups=secgroups)
instance_dev = nova.servers.create(name="dev_server_1337", image=image, flavor=dev_flavor, key_name='alex',userdata=userdata, nics=nics,security_groups=secgroups)
instance_worker_1 = nova.servers.create(name="worker_1_1337", image=image, flavor=dev_flavor, key_name='alex',userdata=userdata, nics=nics,security_groups=secgroups)
instance_worker_2 = nova.servers.create(name="worker_2_1337", image=image, flavor=dev_flavor, key_name='alex',userdata=userdata, nics=nics,security_groups=secgroups)
instance_worker_3 = nova.servers.create(name="worker_3_1337", image=image, flavor=dev_flavor, key_name='alex',userdata=userdata, nics=nics,security_groups=secgroups)

print ("waiting for 10 seconds.. ")
time.sleep(10)

servers = [
    instance_prod,
    instance_dev,
    instance_worker_1,
    instance_worker_2,
    instance_worker_3
]

status_list = ['BUILD']

while 'BUILD' in [server.status for server in servers]:
    print ("Building servers...")
    time.sleep(5)
    servers = [nova.servers.get(server.id) for server in servers]

print("Finished building.")
ip_address_prod = None

def get_ip_address(instance):
    for network in instance.networks[private_net]:
        if re.match('\d+\.\d+\.\d+\.\d+', network):
            return network
    return None

ip_addresses = [get_ip_address(server) for server in servers]

ip_address_prod = ip_addresses[0]
ip_address_dev = ip_addresses[1]
ip_address_worker_1 = ip_addresses[2]
ip_address_worker_2 = ip_addresses[3]
ip_address_worker_3 = ip_addresses[4]

with open("/ansible/hosts_template", "r") as f:
    hosts_content = f.read()

hosts_content = hosts_content.replace("<prod_ip>", ip_address_prod)
hosts_content = hosts_content.replace("<dev_ip>", ip_address_dev)
hosts_content = hosts_content.replace("<worker1_ip>", ip_address_worker_1)
hosts_content = hosts_content.replace("<worker2_ip>", ip_address_worker_2)
hosts_content = hosts_content.replace("<worker3_ip>", ip_address_worker_3)

with open("/ansible/hosts", "w") as f:
    f.write(hosts_content)
