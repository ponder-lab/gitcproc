#!/bin/bash
set -ex
psql -h localhost -U postgres -d logging -c "drop table if exists change_summary"
psql -h localhost -U postgres -d logging -c "drop table if exists method_change_detail"
sudo rm -rf ../../evaluation/repos/LogProjects
