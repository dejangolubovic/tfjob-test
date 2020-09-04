# Running Katib jobs directly from yaml templates
## With eos

Workaround until kfp permissions are fixed.
The idea is to be able to run Katib jobs directly from yaml files.
It requires some additional work, but can be useful for now.

1) `git clone https://github.com/dejangolubovic/tfjob-test.git`
2) `git checkout staging`
3) `cd tf-job-test`
4) Copy kerberos credentials file from local to the current directory: `cp local/tmp/krb5cc_1000 .`
5) Copy your code to `custom-code.py`
6) `docker build -f Dockerfile.custom -t username/katib-job .`
7) `docker push username/katib-job`
8) Edit `custom-code.yaml` to add hyperparameters and algorithm options
9) Go to https://ml.cern.ch/katib/#/katib/hp, and copy paste content of your `custom-code.yaml`
10) Click `Deploy` and hope for the best :)
