#!/bin/bash

ansible-playbook -i hosts ssh-playbook.yml --private-key=/.ssh/cluster-key
ansible-playbook -i hosts setup-playbook.yml --private-key=.ssh/cluster-key
