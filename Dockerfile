FROM public.ecr.aws/lambda/python:3.11

ENV TORCH_HOME=/opt/pytorch_model

COPY general.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r general.txt

COPY torch.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r torch.txt

RUN mkdir -p $TORCH_HOME && \
    python -c "import torchvision.models as models; \ 
    models.detection.fasterrcnn_mobilenet_v3_large_320_fpn(weights=None, num_classes=2); \
    models.mobilenet_v3_small(weights=None) "

COPY detector.pt ${LAMBDA_TASK_ROOT}
COPY classifier.pt ${LAMBDA_TASK_ROOT}

COPY main.py ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]
