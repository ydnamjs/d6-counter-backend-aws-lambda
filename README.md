# Building and Deploying for AWS Lambda (Ubuntu)

Due to the file size of the function, it is not possible to deploy using the zip upload or AWS S3 options so a docker image must be built and uploaded to AWS ECR (Elastic Container Registry).

For consistency and reproducibility, the build process will be done on an AWS EC2 instance.

## Launching an AWS EC2 instance

Navigate to the "Console Home" page by clicking the aws button which is always in the top left of the screen

![image](https://github.com/user-attachments/assets/a7afc45a-53ca-4f4b-a296-42289bc4f93c)

Navigate to the All Services menu by selecting "View All Services"

![image](https://github.com/user-attachments/assets/912ac926-76a7-413a-b000-c9f5b6658484)

In the all services menu, under Computer select EC2

![image](https://github.com/user-attachments/assets/bd6405b1-6156-4d64-9c2e-3d8237a7ade7)

In the EC2 dashboard select "Launch Instance"

![image](https://github.com/user-attachments/assets/c188532d-8738-46e0-833d-f5fa417bc498)

Give your instance a name

![image](https://github.com/user-attachments/assets/ee008446-0915-4d51-a4ce-f131165ccc7c)

In the "Application and OS Images (Amazon Machine Image)" section select Ubuntu and Ubuntu Server 24.04 LTS

![image](https://github.com/user-attachments/assets/8899baec-c618-48e3-a06a-f7b4e1f666ea)

In the "Configure Storage" section increase your root volume's size to 30 GiB

![image](https://github.com/user-attachments/assets/955b82ea-0668-445b-baaf-e5a50863ced4)

On the right, in the "Summary" section, select "Launch instance"

![image](https://github.com/user-attachments/assets/4422c433-d062-454d-baa1-0789b8fa2644)

In the menu that automatically opens after, select "Create new key pair", enter a name in the "Key pair name" field, and select "Launch Instance"

![image](https://github.com/user-attachments/assets/e7e899ce-8891-43b2-b9dd-0565e142b139)


Navigate to your instance's connect page

![image](https://github.com/user-attachments/assets/6532ca3c-41ae-448b-b86a-e858331aeffd)

![image](https://github.com/user-attachments/assets/f7836734-c65c-4507-8606-dd3c68e484f5)

![image](https://github.com/user-attachments/assets/4d284bb8-a3ba-44c0-a585-69e214df32a3)


Follow the instructions listed on this page to connect to your instance

Your key is most likely in your Downloads folder

![image](https://github.com/user-attachments/assets/62820800-0d2b-427c-97b9-248b8fc921ef)


## Installing Required Programs

### Install Unzip:

```
sudo apt install unzip
```

### Install AWS CLI by running the following commands:

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```
```
unzip awscliv2.zip
```
```
sudo ./aws/install
```
```
rm -r aws
```
```
rm awscliv2.zip
```

See https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html for official instructions

### Install Docker by running the following commands:

```
sudo apt-get update
```
```
sudo apt-get install ca-certificates curl
```
```
sudo install -m 0755 -d /etc/apt/keyrings
```
```
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
```
```
sudo chmod a+r /etc/apt/keyrings/docker.asc
```
```
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

See https://docs.docker.com/engine/install/ubuntu/ for official instructions
