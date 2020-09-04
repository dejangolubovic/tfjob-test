# tfjob-test

1) git clone https://github.com/dejangolubovic/tfjob-test.git
2) git checkout staging
3) Copy krb file to the folder where Dockerfile is
4) Copy your code to custom-code.py
5) Locally: docker build -f Dockerfile.custom -t dejangolubovic/tfjob-test:custom .
6) https://ml.cern.ch/katib/#/katib/hp copy and paste content of custom-code.yaml
