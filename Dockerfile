FROM nginx:alpine

WORKDIR /ocfdocs

# Install dependencies
RUN apk update && \
    apk add --no-cache python3 \
    py3-pip \
    supervisor \
    py3-virtualenv \
    bash

# Set up virtualenv
COPY requirement.txt .
RUN python3 -m venv venv 
ENV PATH="/ocfdocs/venv/bin:$PATH"
RUN pip3 install -r requirement.txt

# Copy source code
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY . .

# Initialize directories to prevent errors
RUN mkdir docs
RUN mkdir site

# Add permissions
RUN chmod +x ./sync.py
RUN chmod +x ./main.sh

# Logging
RUN mkdir -p /var/log/sync
RUN mkdir -p /var/log/nginx

# Expose port
EXPOSE 80

# Start syncing
CMD ["/usr/bin/supervisord"]