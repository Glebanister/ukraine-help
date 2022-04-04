FROM continuumio/miniconda
WORKDIR .   
COPY ./ ./
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

EXPOSE 8080 
# The code to run when container is started:
# ENTRYPOINT ["conda", "run", "-n", "myenv", "python3", "ua_help/bot_students/main.py"]
