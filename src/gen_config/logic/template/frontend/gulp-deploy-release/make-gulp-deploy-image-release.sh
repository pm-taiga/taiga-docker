#!/bin/bash
cd {{PROJECT_BASE_IN_HOST}}/temp/frontend/gulp-deploy-release
docker build -t taiga-front-dist-gen-release:v3 .