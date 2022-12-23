import docker
import time

client = docker.from_env()
client.swarm.leave(force=True)


#--------------PART 1-------------------

# Initialize a swarm and printing ID,name,creation date
print("Initaiting a swarm ")
client.swarm.init()


print("Swarm ID: ", client.swarm.attrs['ID'])
print("Swarm Name: ", client.swarm.attrs['Spec']['Name'])
print("Swarm Creation Date: ", client.swarm.attrs['CreatedAt'])

#Creates a network and print ID,name,creation date
print("\nNetwork")
client.networks.create("se443_test_net", driver = "overlay", scope ="global", 
ipam = docker.types.IPAMConfig(pool_configs = [docker.types.IPAMPool(subnet = "10.10.10.0/24")]))

for net in client.networks.list():
    if net.name == "se443_test_net":
        print("Network ID: ", net.id)
        print("Network Name: ", net.name)
        print("Network Creation Date: ", net.attrs['Created'])
 
#Deploys a  broker service always restarting and print ID,name,replicas,creation date
print("\nDeploying a Broker Service")
client.services.create("eclipse-mosquitto", name = "Broker", restart_policy={"Name": "always"},).scale(3)

print("Service ID: ", client.services.list()[0].id)
print("Service Name: ", client.services.list()[0].name)
print("Service Creation Date: ", client.services.list()[0].attrs['CreatedAt'])
print("Service Num Of Replicas: ", client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])

#--------------PART 2-------------------

#Deploy a publisher service always restarting and print ID,name,replicas,creation date

client.services.create("efrecon/mqtt-client", name="Publisher",  restart_policy={"Name": "always"}, networks=["se443_test_net"], command='pub -h host.docker.internal -t Alfaisal_Uni -m "201270---Raghad---Al Sagga---065328363---Hello"').scale(3)
print("\nPublisher Service")
print("Publisher ID: ", client.services.list()[0].id)
print("Publisher Name: ", client.services.list()[0].name)
print("Publisher Creation Date: ", client.services.list()[0].attrs['CreatedAt'])
print("Publisher Num Of Replicas: ", 
client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])


#Deploy a Subscriber service always restarting and print ID,name,replicas,creation date

client.services.create("efrecon/mqtt-client", name="Subscriber",restart_policy={"Name": "always"}, networks=["se443_test_net"], command='sub -h host.docker.internal -t Alfaisal_Uni -v').scale(3)
print("\nSubscriber Service")
print("Subscriber ID: ",client.services.list()[0].id)
print("Subscriber Name: ",client.services.list()[0].name)
print("Subscriber Creation Date: ",client.services.list()[0].attrs['CreatedAt'])
print("Subscriber Num Of Replicas: ",client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])


#--------------Part 3-------------------

#will keep runniing for 5 min
time.sleep(300)
print("\n cleaning")

# Removing All deployed services(broker,publisher,subsriber),newtwork ans swarm 

print("\nRemoving Publisher", end="")
client.services.get("Publisher").remove()
print("\nPublisher successfully removed ")


print("\nRemoving Subscribe", end="")
client.services.get("Subscriber").remove()
print("\nSubscriber successfully removed")


print("\nRemoving Broker", end="")
client.services.get("Broker").remove()
print("\nBroker successfully removed")


print("\nRemoving Network", end="")
client.networks.get("se443_test_net").remove()
print("\nNetwork successfully removed")


print("\nRemoving Swarm", end="")
client.swarm.leave(force=True)
print("\nNetwork successfully removed")