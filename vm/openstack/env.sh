#!/bin/bash

rm .env

# Source the .sh file
source opensrc.sh

# Export the environment variables to a .env file
echo "OS_AUTH_URL=$OS_AUTH_URL" >> .env
echo "OS_PROJECT_ID=$OS_PROJECT_ID" >> .env
echo "OS_PROJECT_NAME=$OS_PROJECT_NAME" >> .env
echo "OS_USER_DOMAIN_NAME=$OS_USER_DOMAIN_NAME" >> .env
echo "OS_PROJECT_DOMAIN_ID=$OS_PROJECT_DOMAIN_ID" >> .env
echo "OS_USERNAME=$OS_USERNAME" >> .env
echo "OS_PASSWORD=$OS_PASSWORD" >> .env
echo "OS_REGION_NAME=$OS_REGION_NAME" >> .env
echo "OS_INTERFACE=$OS_INTERFACE" >> .env
echo "OS_IDENTITY_API_VERSION=$OS_IDENTITY_API_VERSION" >> .env
