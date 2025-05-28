# Darkrawl

## Description

Darkrawl is a project designed to simplify crawling the dark web. It utilizes a Docker image that sets up an environment with Tor and Privoxy, enabling Scrapy to connect to .onion domains.

## Features

*   Easy setup using Docker.
*   Pre-configured Tor and Privoxy for accessing .onion sites.
*   Integrates with Scrapy for web crawling.

## Prerequisites

*   Docker installed on your system.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/w0uldy0u/darkrawl.git
    cd darkrawl
    ```
2.  Build the Docker image:
    ```bash
    docker build -t darkrawl .
    ```

## Usage

To start crawling, run the Docker container. This command mounts the `onion_project` directory from your current working directory into the `/app` directory in the container. This allows you to access your Scrapy project files and store crawled data.

```bash
docker run -v $(pwd)/onion_project:/app darkrawl
```
