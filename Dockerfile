FROM python:3-slim AS builder

ADD . /app

WORKDIR /app

# We are installing the dependencies here directly into our app source dir
RUN pip install --target=/app pyyaml requests

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10:nonroot

COPY --from=builder /app /app

WORKDIR /app

ENV PYTHONPATH /app

CMD ["/app/main.py"]
