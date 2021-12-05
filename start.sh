#!/bin/bash

docker-compose up --build
docker-compose up --build -d && docker attach majorizer
