#!/bin/bash -eu

bucket=$1
snakemake --rerun-incomplete -p -j 750 --kubernetes --container-image us.gcr.io/strides-sra-hackathon-data/test_pipeline:v0.4 --default-remote-provider GS --default-remote-prefix $bucket --latency-wait 60 --keep-going --restart-times 3 --nolock check_all
