#!/bin/bash

# Wait (if cluster is building)
while [ -z "$(docker ps -q -f name=dev-app-1)" ]; do
    echo "Waiting for container dev-app-1 to start..."
    sleep 1
done

sudo docker exec dev-app-1 ray job submit --working-dir . -- python3 train.py
sudo docker exec dev-app-1 ray job submit --working-dir . -- python3 tune.py
sudo chmod +x push-to-prod
./push-to-prod