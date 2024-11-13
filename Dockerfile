FROM debian:bookworm-slim

WORKDIR /ocfdocs

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3 \
    python3-pip \
    supervisor \
    python3-venv && \
    apt-get clean

# Set up virtualenv
COPY requirement.txt .
RUN python3 -m virtualenv venv && source venv/bin/activate
RUN pip3 install -r requirement.txt

# Copy source code
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY . .
RUN mkdir docs

# Add permissions
RUN chmod +x ./sync.py
RUN chmod +x ./main.sh

# Expose port
EXPOSE 80

# Start syncing
CMD ["/usr/bin/supervisord"]