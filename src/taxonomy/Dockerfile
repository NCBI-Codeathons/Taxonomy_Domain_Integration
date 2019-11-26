FROM debian:stretch

RUN apt-get update
RUN apt-get install -qy wget

RUN wget -q https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh && bash Anaconda3-2019.10-Linux-x86_64.sh -b -p /root/anaconda 
ENV PATH="/root/anaconda/bin:${PATH}"
RUN eval $(conda shell.bash hook) && conda init

RUN conda install -y -c bioconda -c conda-forge snakemake

RUN conda install google-cloud-storage

COPY bloom_filter bloom_check /usr/bin/

RUN wget -q https://github.com/marbl/Mash/releases/download/v2.2/mash-Linux64-v2.2.tar && tar xf mash-Linux64-v2.2.tar && mv mash-Linux64-v2.2/mash /usr/bin/
