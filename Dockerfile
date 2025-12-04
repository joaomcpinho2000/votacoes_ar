FROM python:3.6.12-alpine3.12

# Copy the requirements file
COPY . .

# Install the required dependencies
RUN pip install -r requirements.txt

RUN crontab crontab

# Command to run the Python script
CMD ["crond", "-f"]