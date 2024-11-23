FROM python:3.12-alpine
COPY ./dist/ /dist/
RUN pip install --find-links=/dist english==0.1.0 && rm -rf /dist
CMD ["python"]
