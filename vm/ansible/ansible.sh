#!/bin/bash

ansible-playbook -i hosts setup-playbook.yml --private-key=/.ssh/cluster-key
ansible-playbook -i hosts start-train.yml --private-key=/.ssh/cluster-key