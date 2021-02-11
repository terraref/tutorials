FROM rocker/binder:4.0.3

RUN apt-get update \
    && apt-get install -y \
    libudunits2-dev \
    libgdal-dev

RUN echo "alias l='ls -al'" >> /root/.bashrc

RUN Rscript -e 'install.packages("blogdown")'
RUN Rscript -e 'install.packages("ggplot2")'
RUN Rscript -e 'install.packages("ggthemes")'
RUN Rscript -e 'install.packages("reticulate")'

COPY . /terraref/tutorials

WORKDIR /terraref/tutorials

EXPOSE 3000

CMD Rscript -e 'bookdown::render_book("index.Rmd")' \
    && cd docs \
    && echo 'Starting a web server on http://localhost:3000/ to preview the documentation...' \
    && python -m SimpleHTTPServer 3000
    
# CMD wget -O trait_data.zip https://datadryad.org/stash/downloads/file_stream/624637
