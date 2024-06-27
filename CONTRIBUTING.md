# Contributing Guidelines


## Installation for Developers

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

  

## Types of Contributions

A contribution can be one of the following cases:


## Questions
    
[Edit the section accordingly, though the text below is generic and a common practice]
1. use the search functionality [here](https://github.com/sarasal/trip-planning/issues) to see if someone already filed the same issue;
2. if your issue search did not yield any relevant results, make a new issue;
3. apply the "Question" label; apply other labels when relevant.

## Find Bugs

If you think you may have found a bug:

1. use the search functionality [here](https://github.com/sarasal/trip-planning/issues) to see if someone already filed the same issue;
2. if your issue search did not yield any relevant results, make a new issue, making sure to provide enough information to the rest of the community to understand the cause and context of the problem. Depending on the issue, you may want to include:
    - the [SHA hashcode](https://help.github.com/articles/autolinked-references-and-urls/#commit-shas) of the commit that is causing your problem;
    - some identifying information (name and version number) for dependencies you're using;
    - information about the operating system;
    - detailed steps to reproduce the bug.
3. apply relevant labels to the newly created issue.

## Changes to Source Code: fix bugs and add features

1. (important) announce your plan to the rest of the community before you start working. This announcement should be in the form of a (new) issue;
2. (important) wait until some consensus is reached about your idea is a good idea;
3. if needed, fork the repository to your own Github profile and create your feature branch out of the latest master commit. While working on your feature branch, make sure to stay up to date with the master branch by pulling in changes;
4. make sure the existing tests still work;
5. add your tests (if applicable);
6. update or expand the documentation;
7. push your feature branch to (your fork of) this repository on GitHub;
8. create the pull request, e.g. following the instructions [here](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

> If you feel like you have a valuable contribution to make, but you don't know how to write or run tests for it or create the documentation: don't let this discourage you from making the pull request; we can help you! Just go ahead and submit the pull request, but keep in mind that you might be asked to append additional commits to your pull request.
