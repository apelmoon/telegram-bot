#!/bin/bash

apt-get update && apt-get install -y \
    libgstgl-1.0-0 \
    libgstcodecparsers-1.0-0 \
    libavif15 \
    libenchant2-2 \
    libsecret-1-0 \
    libmanette-0.2-0 \
    libgles2-mesa \
    libglib2.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libappindicator3-1 \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libatspi2.0-0 \
    ca-certificates \
    wget \
    curl \
    --no-install-recommends

playwright install