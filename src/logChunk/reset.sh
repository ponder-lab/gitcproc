#!/bin/bash
set -ex

HOST="database-research.cwfckxyjfuva.us-east-1.rds.amazonaws.com"
USER="khatchad"
DB="func"
REPO_DIR="FuncProjects"

psql -h "$HOST" -U "$USER" -d "$DB" -c "drop table if exists change_summary"
psql -h "$HOST" -U "$USER" -d "$DB" -c "drop table if exists method_change_detail"

rm -rf "../../evaluation/repos/$REPO_DIR"
