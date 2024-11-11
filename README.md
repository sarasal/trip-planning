# trip-planning


![Demo](images/user-study-preview.gif)

## Description

This repository contains the interface developed to support a research project published in the following paper. The project involved an empirical study exploring how human decision-makers interact with AI systems when dealing with complex and uncertain tasks. The corresponding code for the interface and the full list of tasks are available here. 

Sara Salimzadeh, Gaole He, and Ujwal Gadiraju. 2024. Dealing with Uncertainty: Understanding the Impact of Prognostic Versus Diagnostic Tasks on Trust and Reliance in Human-AI Decision Making. In Proceedings of the CHI Conference on Human Factors in Computing Systems (CHI '24). Association for Computing Machinery, New York, NY, USA, Article 25, 1–17. https://doi.org/10.1145/3613904.3641905


## Installation

The codebase includes a Vue.js front-end application along with a bac-kend Flask API. The corresponding folders are 'front-end' and 'back-end', both contained within the 'trip-planner-interface' directory. To run the application locally, both the front-end and back-end components need to be started.

1. Back-end

Change directory to the back-end and run the Python script

```bash
$ cd back-end
$ Python api.py
```
**Requirements** 
- Python version at least 3.8
- Python packages Flask, CORS, sqlite3

2. Front-end

Change directory to the front-end and install the required packages

```bash
$ cd front-end
$ npm install
$ npm run dev
```

The Docker file is provided to simplify the front-end setup. You can build and run the Docker container to get the application up and running.

```bash
$ docker build -t webapp .
$ docker run -it -d -p 8080:80 webapp
```

**Requirements** 
- NodeJS
- Vue 3


## Contributing Guidelines

Read the (CONTRIBUTING.md) to know how can you take part in this project. 


## License

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


## Copyright

Technische Universiteit Delft hereby disclaims all copyright interest in the dataset contains the annotation of the complexity and diverse features of decision tasks in the human-AI decision-making literature written by Sara Salimzadeh.

Lucas van Vliet, Dean of the Faculty of Electrical Engineering, Mathematics, and Computer Science.

&copy; (2024) Sara Salimzadeh, Delft, The Netherlands. 

## Citation

If you use trip-planning to produce results for your scientific publication, please refer to our [CHI paper](https://doi.org/10.1145/3613904.3641905). 

```bash
@inproceedings{salimzadeh2024_uncertainty,
  author = {Salimzadeh, Sara and He, Gaole and Gadiraju, Ujwal},
  title = {Dealing with Uncertainty: Understanding the Impact of Prognostic Versus Diagnostic Tasks on Trust and Reliance in Human-AI Decision Making},
  year = {2024},
  isbn = {9798400703300},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  url = {https://doi.org/10.1145/3613904.3641905},
  doi = {10.1145/3613904.3641905},
  articleno = {25},
  numpages = {17},
  location = {Honolulu, HI, USA},
  series = {CHI '24}
}
```

