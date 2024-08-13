FROM public.ecr.aws/lambda/python:3.11

COPY general.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r general.txt

COPY torch.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r torch.txt

COPY detector.pt ${LAMBDA_TASK_ROOT}
COPY classifier.pt ${LAMBDA_TASK_ROOT}

COPY main.py ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]
