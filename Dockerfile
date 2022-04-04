FROM continuumio/miniconda3
WORKDIR .   
COPY ./ ./

RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
CMD ["conda", "run", "-n", "ukraine-help", "/bin/bash", "-c"]
CMD ["conda", "activate", "ukraine-help"]
CMD ["conda", "develop", "."]

EXPOSE 8080 
# The code to run when container is started:
WORKDIR ua_help/bot_student
CMD ["python", "main.py"]
