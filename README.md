# tfjob-test

1) git clone https://github.com/dejangolubovic/tfjob-test.git
2) Copy krb file to the folder where Dockerfile is
3) Create a file custom-code.py with your code, in the same directory
4) Locally: docker build -f Dockerfile -t dejangolubovic/tfjob-test:custom .
5) https://ml.cern.ch/katib/#/katib/hp copy and paste content of custom-code.yaml
