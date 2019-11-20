#!/usr/bin/env bash

# Serverless deployment
cd evaluator-deploy-repository
echo Packaging serverless bundle...
serverless package --package pkg
echo Deploying to AWS...
serverless deploy --verbose;
