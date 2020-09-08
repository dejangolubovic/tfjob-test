# Running Katib jobs directly from yaml templates (with EOS)

Workaround until kfp permissions are fixed.

The idea is to be able to run Katib jobs directly from yaml files.

It requires some additional work, but can be useful for now.

## Prerequisites

### If using a local machine
1) Install Docker. To run this example, a machine with installed Docker is needed. Docker can't be installed on ml.cern.ch, nor on lxplus. An option to install can be a local PC or a laptop. To install docker: https://docs.docker.com/get-docker/
2) Make a Docker account: https://docs.docker.com/docker-id/

### If using Docker VM
1) Login to lxplus
2) `nano ~/.ssh/dockervmkey.pem`
- Copy content of the private key (which I will you send via Mattermost)
3) `nano ~/.ssh/config`, add the following lines:
```
Host docker-temp
    User root
    IdentityFile ~/.ssh/dockervmkey.pem
```
5) `ssh docker-temp`

## Katib job setup

### On a local machine or Docker VM, where Docker daemon is installed
0) Login to Docker: `docker login` + enter Docker ID and password
1) `git clone https://github.com/dejangolubovic/tfjob-test.git`
2) `cd tfjob-test`
3) `git checkout staging`
4) Copy kerberos credentials file from local to the current directory: `cp @YOUR_LOCAL_PATH/krb5cc_1000 .`
5) Copy your code to `custom-code.py`
6) `docker build -f Dockerfile.custom -t @username/katib-job . --network=host`
7) `docker push @username/katib-job`

### Anywhere
8) Edit `custom-code.yaml`
  - Add hyperparameters and algorithm options
  - Set your docker image `image: registry.hub.docker.com/@username/katib-job`

### On ml.cern.ch
9) Go to https://ml.cern.ch/katib/#/katib/hp, and copy paste content of your `custom-code.yaml`
10) Click `Deploy` and hope for the best :)

### IMPORTANT: Once finished with Docker VM machine
Do `docker logout` as your credentials are not encrypted there.
