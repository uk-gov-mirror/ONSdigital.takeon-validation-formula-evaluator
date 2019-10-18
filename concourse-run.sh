fly -t takeon destroy-pipeline -p lambda-takeon-validation-formula-evaluator
fly -t takeon set-pipeline -p lambda-takeon-validation-formula-evaluator -c pipeline.yml --load-vars-from params.yml
fly -t takeon unpause-pipeline -p lambda-takeon-validation-formula-evaluator