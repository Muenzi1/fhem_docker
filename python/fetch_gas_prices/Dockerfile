FROM python:3.9-slim AS compile-image

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install wheel && \
    pip install -r requirements.txt

COPY src/ /app



FROM python:3.9-slim

# copy only the dependencies installation from the 1st stage image
COPY --from=compile-image /opt/venv /opt/venv
COPY --from=compile-image /app /app

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

CMD [ "python", "main.py" ]