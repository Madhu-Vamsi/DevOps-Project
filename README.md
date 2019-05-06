




# DevOps-Project : Milestone 3 + Special Milestone
The following are the team members along with their contribution :
 - Purva Vasudeo(ppvasude) :  Microservice, Docker image setup, Kubernetes Setup, Chaos Monkey
 - Hiral Singadia(hasingad) : Microservice, Docker image setup, Kubernetes Setup, Chaos Monkey
 - Jeremiah Dsouza(jdsouza) : Deploy, Redis 
 - Madhu Vamsi Kalyan Machavarapu(mmachav) : Deploy, Redis 

Complete Project demo: [LINK](https://youtu.be/aQ3kEO4lEGE)

Milestone video demo: [LINK](https://drive.google.com/file/d/1MPdE0n4uZHT8hKXxkSdfwFQ5XtpySj7q/view?usp=sharing)
 
## Deploy and Infra Milestone
Run command:

> sudo ansible-playbook -i inventory deploy-master-plabook.yml

After the microservice is setup a timeout of 5 mins is given to replace the external IP in the checkbox.io application code.

Please refer to the previous milestone branches for the initial set up.

### Deploy Component
For this task, we have configured a machine on AWS and deployed iTrust and checkbox applications on that machine. The playbooks responsible for this task are below with their functions : 
- **/ansible_srv/helper-playbooks/deployment-milestone.yml**:
This playbook does the initial setup required for the deployment task, on the Jenkins server. It will download the required repositories, create the bare repositories, create the remotes and git hooks. It will then add our aws and github credentials as environment variables. We will require the following credentials in the variable file:
`aws_access` : AWS ACCESS KEY
`aws_secret` : AWS SECRET ACCESS KEY

- **/ansible_srv/helper-playbooks/trigger-iTrust.yml**:
This playbook will trigger the iTrust deployment. It will first run a python script to generate a random file in the iTrust repository. Then it will commit and push these changes to the production branch, which will trigger a jenkins build job due to the post-receive hook present. It will wait for the build job to get over, and then apply the war.patch file needed to generate the .war file. Next, it will prepare the .war file of the iTrust repository before running another ansible script that will setup an AWS instance using boto3 framework for python. This script will create the keypair (if needed), assign it a security group and store the ip address for the next tasks. It will then run a second ansible playbook that will install the dependencies needed for iTrust on the AWS instance, install jetty for hosting iTrust, copy the .war file to the required directory and complete all the configuration settings. 

- **/ansible_srv/helper-playbooks/trigger-checkbox.yml**:
This playbook will trigger the Checkbox deployment. It will first run a python script to generate a random file in the checkbox repository. Then it will commit and push these changes to the production branch, which will trigger a jenkins build job due to the post-receive hook present. It will wait for the build job to get over, before running another ansible script that will setup an AWS instance using boto3 framework for python. This script will create the keypair (if needed), assign it a security group and store the ip address for the next tasks. It will then run a second ansible playbook that will install the dependencies needed for checkbox on the AWS instance, copy the files to the required directory and complete all the configuration settings. 

**To see the deployed applications, enter the ip address of the machine along with the port number as follows:**
* ip_address:8080 - For iTrust
* ip_address:80 - For Checkbox

### Feature Flag Component
For this task, we will be using Redis to illustrate feature flags in iTrust application. We will use a Redis master to propogate changes to a Redis replica use a flag that will be set using the Redis CLI on the master machine. We will require the following playbooks for this task:
- **configure-redis**:
This playbook will spawn a new AWS instance and configure Redis on it. It will then use this machine as the master by modifying the configuration file present. It will use the IP address of the production server machine as the replica.
- **configure-redis-master**:
This playbook will configure Redis on the master server (being used as a configuration server). It will then modify the configuration file present.
- **configure-redis-slave**:
This playbook will configure Redis on the production server. It will then modify the configuration file present and use the IP address of the machine made in the previous playbook as its master.

Next, we need to enter into the master machine, and using the Redis CLI, we will set a feature flag. This will be propogated to the replica machine. The modified code of iTrust will then read this feature flag and check if it is true. Depending on this value, it will then choose to display that feature or not. 

For the iTrust Application to read the redis based in-memory database, the source code of iTrust has been modified (https://github.com/Madhu-Vamsi/iTrust2-v4). A java based dependency by the name "jedis" (maven coordinates provided below) has been added to pom.xml and pom-data.xml. 
Maven coordinates for Jedis:
```groupId: redis.clients```
```artifactId: jedis```
```version: 2.4.2```

Another change which was made is in the AdminController.java file. This file is responsible for the routing of the iTrust app.
The source code changed is responsible for communicating with redis server and check for "hospitals" flag. If the hospitals flag is true then admin/hospitals route becomes accesible and the admin can create/delete hospitals. If the flag is set to false then this page becomes inaccesible and the user is directed to index page. 

### Infrastructure component
We have extracted the functionality of the */api/design/survey* into a microservice which can run independently. This is the link to the microservice code - [LINK](https://github.com/ppvasude/checkbox-microservice). 
The playbooks responsible for this task are below with their functions :
 - **/ansible_srv/helper-playbooks/create-docker-image.yml** :
 This playbook will build the image as per the */ansible_srv/file-templates/DockerFile* and push it to docker hub. Please provide the below necessary credentials of docker in the variables file. 
`git_microservice_repo` : The git URL of the microservice repository. Make sure this is without the *https://*
    `git_username` : This is the username which should have access to above microservice repository.
    `git_password`: This is the password corresponding to the above username.
    `dockerhub_username` : This username will be used to authenticate to DockerHub.
    `dockerhub_password`: This password will be used to authenticate to DockerHub.
    `docker_image_name`: Name you want to give the image.

 
 - **/ansible_srv/helper-playbooks/setup-kubernetes.yml** : 
 We have made use of kubernetes to setup a cluster on AWS. This playbook will create the kubernetes cluster on AWS and assign a master to the cluster. It will download and install any dependencies needed by the cluster.
 
 - **/ansible_srv/helper-playbooks/deploy-microservice.yml** :
 This playbook will pull the image created by the *create-docker-image.yml* from DockerHub. It will create a LoadBalancer and deploy this pulled image into pods on the kubernetes cluster. To get final IP of the microservice, you will have to ssh into the master node and run the following command - 
 
>   kubectl get services
>   
In the response, you will get the External-IP of the service as given below:

![image](https://media.github.ncsu.edu/user/10894/files/91405f00-6853-11e9-8152-18568e0b1f6e)

Copy the IP and paste it in /server-side/site/server.js of this [GitHub Repo
](https://github.com/ppvasude/checkbox.io.git), which has been adopted to hit the microservice. An example snapshot is given below:

![image](https://media.github.ncsu.edu/user/10894/files/b6649d00-6781-11e9-9a29-1422187132a4)
Similarly you can get the deployments and pods by running :

> kubectl get pods

> kubectl get deployments

The number of pods we have created is 3. This can be changed by changing the `--replicas=3`.
Now, when you deploy this checkbox application on cloud, you will be able to hit the microservice and get the markdown rendered text correctly!

## Special Milestone - Chaos Monkey

Run command :
> sudo ansible-playbook helper-playbooks/chaos-monkey.yml

 - **/ansible_srv/chaos-monkey/main.js** :
 This is the chaos monkey script. It makes use of the javascript aws-sdk.
 The script will dynamically fetch all instances associated with one cluster. Then it will do a random selection of a node in that cluster of nodes and delete it. This is as shown in below image.
![image](https://media.github.ncsu.edu/user/10894/files/001bb900-6850-11e9-8001-d460891af76e)
Then you can check if the service provided by the cluster is still available.
 
 - **/ansible_srv/helper-playbooks/chaos-monkey.yml** :
This playbook is responsible for making user specific changes to the chaos monkey script and running it. It is responsible for setting the AWS region of your cluster, name of your cluster and other credentials associated with accessing AWS. It should print the Instance-id of the instance it deletes. This is as shown in the image.

![image](https://media.github.ncsu.edu/user/10894/files/ba5ef080-684f-11e9-98ad-c0ab699b98bf)


