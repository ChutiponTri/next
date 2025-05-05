# Use an Alpine image with Python installed
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the local files to the container
COPY requirements.txt requirements.txt

# Install Streamlit and other required Python packages (if there's a requirements.txt)
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy the local files to the container
COPY . .

# Expose the port Streamlit will run on
EXPOSE 8306

# Command to run the Streamlit app
# CMD ["streamlit", "run", "main.py", "--server.port=8306", "--server.address=0.0.0.0"]
