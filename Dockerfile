ARG IMAGE_TYPE="gpu"
FROM gcr.io/kubeflow-images-public/tensorflow-2.1.0-notebook-gpu:1.0.0
USER root
RUN pip3 install tensorflow_datasets

COPY mnist-kale-katib-gpu.py /
COPY multy_worker.py /

#USER jovyan

#ENTRYPOINT ["python3", "/mnist-kale-katib-gpu.py"]
