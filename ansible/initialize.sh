#!/bin/bash

python3 start_instances.py

ansible -i hosts ssh-playbook.yml --private-key=cluster-key
ansible -i hosts setup-playbook.yml --private-key=cluster-key

