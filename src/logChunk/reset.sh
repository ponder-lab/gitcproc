#!/bin/bash
set -ex
psql -h localhost -U khatchad -d streams -c "drop table if exists change_summary"
psql -h localhost -U khatchad -d streams -c "drop table if exists method_change_detail"
rm -rf ../../evaluation/repos/StreamProjects
