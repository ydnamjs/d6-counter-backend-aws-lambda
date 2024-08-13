# Building and Deploying for AWS Lambda (Ubuntu)

Due to the file size of the function, it is not possible to deploy using the zip upload or AWS S3 options so a docker image must be built and uploaded to AWS ECR (Elastic Container Registry).

For consistency and reproducibility, the build process will be done on an AWS EC2 instance.

## Launching an AWS EC2 instance

Navigate to the "Console Home" page by clicking the aws button which is always in the top left of the screen

![image](https://github.com/user-attachments/assets/a7afc45a-53ca-4f4b-a296-42289bc4f93c)

Navigate to the All Services menu by selecting "View All Services"

![image](https://github.com/user-attachments/assets/912ac926-76a7-413a-b000-c9f5b6658484)

In the all services menu, under "Compute" select "EC2"

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

## Setting up AWS Credentials

Navigate to the "Console Home" page by clicking the aws button which is always in the top left of the screen

![image](https://github.com/user-attachments/assets/a7afc45a-53ca-4f4b-a296-42289bc4f93c)

Navigate to the All Services menu by selecting "View All Services"

![image](https://github.com/user-attachments/assets/912ac926-76a7-413a-b000-c9f5b6658484)

In the all services menu, under "Security, Identity, & Compliance" select "IAM"

![image](https://github.com/user-attachments/assets/f66116b3-11ea-4aa2-a35b-408aeccf4acf)

In the IAM Menu, navigate to the "Users" menu

![image](https://github.com/user-attachments/assets/f269402d-5bfa-4266-8147-b985e1d53146)

In the Users Menu, select "Create user"

![image](https://github.com/user-attachments/assets/2078e189-0a29-460a-ab0a-45f4bf1cb01f)

Give the user a name and select "next"

![image](https://github.com/user-attachments/assets/ef8586e7-35fb-4942-a408-45ced5672495)

In the "Set permissions" menu, select "Attach policies directly" then select "Create policy"

![image](https://github.com/user-attachments/assets/ce1099ff-3aef-4260-abfe-a9fdeab1342c)

In the "Create policy" menu's "Policy editor" section, select "JSON"

![image](https://github.com/user-attachments/assets/533ee835-c591-45aa-9493-9c6740db90ed)

Paste the below policy in the text editor

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ecr:CreateRepository",
                "ecr:CompleteLayerUpload",
                "ecr:TagResource",
                "ecr:GetAuthorizationToken",
                "ecr:UploadLayerPart",
                "ecr:InitiateLayerUpload",
                "ecr:BatchCheckLayerAvailability",
                "ecr:PutImage"
            ],
            "Resource": "*"
        }
    ]
}
```

See https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-push-iam.html for additional information

Select "Next" at the bottom of the "Policy editor" section

![image](https://github.com/user-attachments/assets/26839535-8d31-40d6-aec5-b37baa94d398)

Give the policy a name and optionally a description

![image](https://github.com/user-attachments/assets/e8b191ba-ecac-4f77-8b4b-ba9760c6404f)

At the bottom of the "Review and Create" menu, select "Create policy"

![image](https://github.com/user-attachments/assets/d1f23f46-024c-4394-921c-28aed4a2a2a0)

Return to the "Create User" tab and refresh the policy list

![image](https://github.com/user-attachments/assets/49b76322-deaf-46ea-81bb-6fa423c6e964)

Enable the policy just created in the "Create policy" tab by checking the box next to its name

![image](https://github.com/user-attachments/assets/513625a8-6048-4c23-83df-d78bd927372b)

At the bottom of the "Create User" menu, select "Next"

![image](https://github.com/user-attachments/assets/49c48a2e-49fa-456e-9b6e-f4a3dbd9e2e2)

At the bottom of the "Review and create" menu, select "Create user"

![image](https://github.com/user-attachments/assets/af72325e-1e0a-40af-b740-82b1253bc5f5)

Select the user in the "users" menu

![image](https://github.com/user-attachments/assets/2eb2eb69-2a67-4748-ad22-2d0e158b2b44)

In the "Summary" section, select "Create access key"

![image](https://github.com/user-attachments/assets/6a1b74c5-d258-40fb-b7bd-fd2832cddf12)

Select "Command Line Interface (CLI)" from the "Use Case" Section

![image](https://github.com/user-attachments/assets/b9af1ef8-e747-4069-ae11-c6ef02177a32)

Check the "Confirmation" box and select "Next"

![image](https://github.com/user-attachments/assets/27fff7e2-aa4e-420c-8237-e81d2cfb43bf)

Optionally, enter a description and then select "Create access key"

![image](https://github.com/user-attachments/assets/a2c4d5c4-3329-4e45-a089-6541260756f7)

Inside the EC2 Instance run the following command:
```
sudo aws configure
```

Copy the "Access key" and paste it into the "AWS Access Key ID" field for the aws configure

![image](https://github.com/user-attachments/assets/75fac164-3335-4907-a0f9-6f30895c8cbf)

Copy the "Secret access key" and paste it into the "AWS Secret Access Key ID" field for the aws configure

![image](https://github.com/user-attachments/assets/1c2989fe-9199-4e01-99b0-555c419fee18)

Optionally enter a region like "us-east-2" into the "Default region name" field for the aws configure

Enter "json" as the "Default output format" field for the aws configure

## Building and Pushing the Docker Image

See: https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions for official instructions

Return to the AWS IAM Console and copy your "Account ID" from the AWS Account section

![image](https://github.com/user-attachments/assets/0f96d988-fd7d-4199-ba3b-d615f08b714f)

Return to your EC2 instance and run the following command replacing both "us-east-2"s with your region of choice and the "111111111111" with your "Account ID"
```
sudo aws ecr get-login-password --region us-east-2 | sudo docker login --username AWS --password-stdin 111111111111.dkr.ecr.us-east-2.amazonaws.com
```

Create an ECR Repository by running the following command replacing the "us-east-2" with your region of choice
```
sudo aws ecr create-repository --repository-name d6-counter-backend-lambda-demo --region us-east-2 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
```

Clone this repository
```
git clone https://github.com/ydnamjs/d6-counter-backend-aws-lambda.git
```

Navigate into the repository
```
cd d6-counter-backend-aws-lambda
```

Build the Docker image
```
sudo docker build --platform linux/amd64 -t d6-counter-backend-lambda-demo:latest .
```

Tag the docker image replacing "111111111111" with your "Account ID" and "us-east-2" with your region of choice
```
sudo docker tag d6-counter-backend-lambda-demo:latest 111111111111.dkr.ecr.us-east-2.amazonaws.com/d6-counter-backend-lambda-demo:latest
```

Push the image up to the ECR Repository replacing "111111111111" with your "Account ID" and "us-east-2" with your region of choice
```
sudo docker push 111111111111.dkr.ecr.us-east-2.amazonaws.com/d6-counter-backend-lambda-demo:latest
```
