############################################################
# Dockerfile to build DNas container images
# Based on Debian
############################################################

FROM debian

MAINTAINER public0821@gmail.com

# use a fast apt source in China 
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update

# install needed packages
RUN apt-get install -y git python3

# install dnas
RUN git clone https://github.com/public0821/dnas.git /root/dnas

ENV PATH="/root/dnas/src:${PATH}"

# install samba
RUN dnas samba install

# remove default share points
RUN dnas samba clear

CMD ["dnas samba start --forever"]