FROM python:3.7

ARG WORKDIR
ENV WORKDIR $WORKDIR
ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}"

COPY . ${WORKDIR}

WORKDIR ${WORKDIR}
RUN pip install -r requirements.txt


WORKDIR /opt
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8082"]
EXPOSE 8082