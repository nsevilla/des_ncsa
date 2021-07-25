DES Data Management (DESDM) public data release website
========================================================

This repository is the source code for the DESDM public data release website at https://des.ncsa.illinois.edu/.

Workflow for contributing content updates
----------------------------------------------

0. [Install `docker`](https://docs.docker.com/engine/install/) and `git`.
1. Fork the repo https://github.com/des-labs/des_ncsa to https://github.com/$GITHUB_USER/des_ncsa where `$GITHUB_USER` is your GitHub account username.
2. Clone your fork locally and checkout the `dev` branch.
    ```shell
    CLONE_DIR="$HOME/src/$GITHUB_USER/des_ncsa"
    git clone https://github.com/$GITHUB_USER/des_ncsa $CLONE_DIR
    cd $CLONE_DIR
    git checkout dev
    ```
3. Build and run the Docker image.
    ```shell
    docker build -t desdm-public:dev .
    docker run --rm --name desdm-public \
      -e APP_ROOT="" -e JIRA_DEFAULT_ASSIGNEE="" \
      -p 8080:8080 desdm-public:dev
    ```
4. Open your browser to http://127.0.0.1:8080 to view the website.
5. Edit the relevant HTML files. Stop the webserver by pressing CTRL+C in the terminal running the `docker run` command. Repeat the `docker build` and `docker run` commands. For convenience you can use `&&` to execute them together.
    ```shell
    docker build -t desdm-public:dev . && \
    docker run --rm --name desdm-public \
      -e APP_ROOT="" -e JIRA_DEFAULT_ASSIGNEE="" \
      -p 8080:8080 desdm-public:dev
    ```
6. Reload the page and see the results. Repeat step 5 until satisfied.
7. Commit your changes to the git repo and push the updates to your GitHub fork.
    ```shell
    git add
    git commit -m 'Updated release page blah'
    git push
    ```
8. Create a pull request to merge and publish your changes.
