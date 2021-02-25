# Set a base image
FROM python:3.7

# Set the working directory
WORKDIR /code

# Copy the file from the local host to the filesystem of the container at the working directory.
COPY waterScrape/requirements.txt .

# Install Scrapy specified in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project source code from the local host to the filesystem of the container at the working directory.
COPY waterScrape/ .

# Run the crawler when the container launches.
CMD [ "python3", "./runner.py" ]