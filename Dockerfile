# Use the official image as a parent image.
FROM python:3

# Set the working directory.
WORKDIR /

# Copy the file from your host to your current location.
COPY getweather.py /

# Run pip to install requirements.
RUN pip install --no-cache-dir pyowm setuptools

# Run the command and redirect output to logger.
CMD ["/usr/local/bin/python","/getweather.py","|","logger"]
