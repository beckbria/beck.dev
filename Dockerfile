FROM golang:1.22-alpine

# Install build dependencies and libraries needed for Hugo Extended
RUN apk add --no-cache \
    curl \
    git \
    build-base \
    libc6-compat \
    gcompat \
    bash

# Define Hugo version (extended)
ARG HUGO_VERSION=0.163.3

# Install Hugo Extended
RUN curl -L -o hugo.tar.gz https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz && \
    tar -xzf hugo.tar.gz -C /usr/local/bin hugo && \
    rm hugo.tar.gz

# Verify Hugo installation
RUN hugo version

WORKDIR /src

# Expose port 1313 for Hugo's development server
EXPOSE 1313

# Default command to run Hugo server
CMD ["hugo", "server", "--bind", "0.0.0.0", "--navigateToChanged"]
