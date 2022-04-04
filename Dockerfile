FROM continuumio/miniconda
WORKDIR .   
COPY ./ ./

RUN conda update conda
RUN conda env create -f environment.yml -n ua_help
RUN conda run -n ua_help
EXPOSE 8080 
ENTRYPOINT ["conda", "run", "-n", "ua_help", "python3", "ua_help/bot_students/main.py"]
