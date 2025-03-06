FROM jupyter/scipy-notebook

ENV NB_USER jovyan
ENV NB_UID 1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}
# copying contents from repo to binder
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

USER $NB_UID

RUN pip install music21; \
    pip install IPython; \
    pip install ipywidgets; \
    pip install sklearn; \
    pip install numpy"<2"; \
    pip install pandas; \
    pip install matplotlib; \
    pip install itertools; \    
    pip install openpyxl

USER root

RUN apt-get update; \
    apt-get install -y software-properties-common; \
    add-apt-repository ppa:mscore-ubuntu/mscore3-stable; \
    apt-get update; \
    apt-get install -y musescore3; \
    apt-get install -y nodejs; \
    rm -rf /var/lib/apt/lists/*; \
    apt-get clean
    
USER $NB_UID

ENV QT_QPA_PLATFORM=offscreen
RUN python -c "from music21 import * ; us = environment.UserSettings(); \
us['musescoreDirectPNGPath'] = '/usr/bin/musescore3'; \ 
us['pdfPath'] = '/usr/bin/musescore3'; \
us['graphicsPath'] = '/usr/bin/musescore3'; \
us['musescoreDirectPNGPath'] = '/usr/bin/musescore3'; \
us['musicxmlPath'] = '/usr/bin/musescore3';"
