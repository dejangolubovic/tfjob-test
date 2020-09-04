# tfjob-test

1) git clone https://github.com/dejangolubovic/tfjob-test.git
2) git checkout staging
3) Copy krb file to the folder where Dockerfile is
4) Create a file custom-code.py with your code, in the same directory
5) Locally: docker build -f Dockerfile.custom -t dejangolubovic/tfjob-test:custom .
6) https://ml.cern.ch/katib/#/katib/hp copy and paste content of custom-code.yaml
