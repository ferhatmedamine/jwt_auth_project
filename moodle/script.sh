#!/bin/bash

# Set variables
DOCKER_COMPOSE_FILE="./docker-compose.yml"
MOODLE_CONTAINER_NAME="moodle"
MOODLE_IMAGE="bitnami/moodle:latest"
MOODLE_NETWORK="moodle_moodle-network"
MOODLE_ENV_VARS="-e MOODLE_HOST=moodle.localhost -e  MOODLE_DATABASE_USER=campusnauser -e MOODLE_DATABASE_PASSWORD=amine -e MOODLE_DATABASE_NAME=campusnadb -e ALLOW_EMPTY_PASSWORD=yes -e MOODLE_DATABASE_TYPE=pgsql -e MOODLE_DATABASE_HOST=postgres -e MOODLE_DATABASE_PORT_NUMBER=5432"
MOODLE_VOLUMES="-v moodle_data:/bitnami/moodle -v moodledata_data:/bitnami/moodledata"
TRAEFIK_LABELS="--label traefik.enable=true --label traefik.http.routers.moodle.rule=Host(\`moodle.localhost\`) --label traefik.http.routers.moodle.entrypoints=web --label traefik.http.services.moodle.loadbalancer.server.port=8080"
LOG_FILE="/var/log/moodle_deploy.log"

# Function to log messages
echo_log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Step 1: Start Traefik and postgres
echo_log "Starting Traefik and postgres..."
docker-compose -f "$DOCKER_COMPOSE_FILE" up -d

# Wait for postgres to start
echo_log "Waiting for MariaDB to start..."
while true; do
    CONTAINER_STATUS=$(docker inspect --format='{{.State.Status}}' postgres)
    if [[ "$CONTAINER_STATUS" == "running" ]]; then
        echo_log "postgres is running."
        break
    else
        echo_log "postgres is not yet running. Current status: $CONTAINER_STATUS. Retrying in 5 seconds..."
        sleep 5
    fi
done

# Step 3: Start Moodle with Traefik labels
echo_log "Deploying Moodle container with Traefik labels..."
docker run -d \
  --name "$MOODLE_CONTAINER_NAME" \
  --network "$MOODLE_NETWORK" \
  $MOODLE_ENV_VARS \
  $MOODLE_VOLUMES \
  $TRAEFIK_LABELS \
  "$MOODLE_IMAGE"

# Step 4: restart Traefik when moodle is  running successfully
docker restart traefik 
echo_log "Moodle is accessible"

echo_log "Deployment completed successfully!"