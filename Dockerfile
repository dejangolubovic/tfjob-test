ARG IMAGE_TYPE="gpu"
FROM gcr.io/kubeflow-images-public/tensorflow-2.1.0-notebook-gpu:1.0.0

COPY mnist-kale-katib-gpu.py /
ENTRYPOINT ["python3", "/mnist-kale-katib-gpu.py"]
