# tfjob-test

1) `git clone https://github.com/dejangolubovic/tfjob-test.git`
2) git checkout staging
3) cd tf-job-test
4) cp local/tmp/krb5cc_1000 krb5cc_1000
5) Copy your code to custom-code.py
6) docker build -f Dockerfile.custom -t username/katib-job .
7) docker push username/katib-job
8) Edit custom-code.yaml to add hyperparameters and algorithm options
9) https://ml.cern.ch/katib/#/katib/hp copy and paste content of custom-code.yaml
