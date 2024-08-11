FROM public.ecr.aws/lambda/python:3.11

COPY general.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r general.txt

COPY torch.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r torch.txt

COPY main.py ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]
