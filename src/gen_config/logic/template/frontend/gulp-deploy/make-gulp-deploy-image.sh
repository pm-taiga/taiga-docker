#!/bin/bash
cd {{PROJECT_BASE_IN_HOST}}/temp/frontend/gulp-deploy
docker build -t stephenxjc/taiga-front-dist-gen:v3 .