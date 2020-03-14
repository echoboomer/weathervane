FROM python:3.7-slim-stretch

# Copy only the relevant Python files into the container.
COPY ./lib /wv/lib
COPY requirements.txt /wv
COPY wv.py /wv

# Set the work directory to the app folder.
WORKDIR /wv

# Install Python dependencies.
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "wv.py"]
