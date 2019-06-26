#!/bin/bash
cd {{PROJECT_BASE_IN_HOST}}/temp/frontend/gulp-deploy-release
docker build -t stephenxjc/taiga-front-dist-gen-release:v3 .