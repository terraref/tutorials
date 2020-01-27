[![Travis-CI Build Status](https://travis-ci.org/terraref/tutorials.svg?branch=master)](https://travis-ci.org/terraref/tutorials)

# TERRA REF Documentation

## Overview

In this repository is an extensive set of materials for how to use TERRA REF data and software. 
The best place to start is the [TERRA REF tutorials website](https://terraref.github.io/tutorials/). 
We used [bookdown](https://bookdown.org/) to create the website, and relevant files include _[bookdown.yml](https://github.com/terraref/tutorials/blob/master/_bookdown.yml), [index.Rmd](https://github.com/terraref/tutorials/blob/master/index.Rmd), and all of the [vignettes](https://github.com/terraref/tutorials/tree/master/vignettes). 

Tutorials on the website come from the more extensive tutorials in the [traits](https://github.com/terraref/tutorials/tree/master/traits), [sensors](https://github.com/terraref/tutorials/tree/master/sensors), and [plantcv](https://github.com/terraref/tutorials/tree/master/plantcv) folders. 
Notes from walkthroughs of TERRA REF data use are in [videos](https://github.com/terraref/tutorials/tree/master/videos). 

These are intended to cover diverse use cases, and you will find information about accessing data from web interfaces but the primary focus is on accessing data using R, Python, SQL, and REST APIs. These are intended to provide quick-start introductions to access data along with computing environments required for further exploration. They are not intended to teach analyses, although some illustrative visualizations and statistical models are provided.

This is a work in progress for an open source community that welcomes contributions in many forms. Please feel welcome to ask questions, provide suggestions, or share analyses that may be of interest to others.

## How to contribute

We welcome suggestions and edits from all users. 
Feel free to [create a GitHub issue](https://github.com/terraref/tutorials/issues) detailing possible improvements. 

If you would like to make changes yourself, fork this repository, make changes on a branch, and submit a pull request. 
We are happy to help with this process. 

There are two ways to preview your changes as you make them. 
The first is by running the following on the command line from within the forked repository folder:

```bash
Rscript -e 'bookdown::render_book("index.Rmd")'
```

The output will be in the `docs` folder.

The second way to preview changes is using the Docker container. 
This requires installing Docker on your computer:

- [Docker for Mac](https://download.docker.com/mac/stable/Docker.dmg)
- [Docker for Windows](https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe) 

Build the image:

```bash
docker build -t terraref-tutorials:local .
```

Run the container:

```bash
docker run --rm -p 3000:3000 --name tutorial-preview terraref-tutorials:local
```

This will generate the documentation and start a local web server to preview
your changes. Open the preview URL in your browser: <http://localhost:3000/>

Run `docker kill tutorial-preview` to kill the web server container. 
