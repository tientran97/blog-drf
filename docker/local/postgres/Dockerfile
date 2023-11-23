FROM postgres:15-bullseye

# Install dos2unix
RUN apt-get update && apt-get install -y dos2unix

COPY ./docker/local/postgres/maintenance /usr/local/bin/maintenance

# Convert line endings to Unix style
RUN find /usr/local/bin/maintenance -type f -exec dos2unix {} \;

# Make scripts executable and move them
RUN chmod +x /usr/local/bin/maintenance/*

RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
   && rmdir /usr/local/bin/maintenance