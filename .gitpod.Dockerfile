FROM gitpod/workspace-full:latest

USER gitpod

RUN sudo apt-get update \
    && sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg2

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
RUN sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
RUN sudo apt-get update \
    && sudo apt-get install -y docker-ce docker-ce-cli containerd.io