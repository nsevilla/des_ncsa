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
3. Build the Docker image.
    ```shell
    docker build -t desdm-public:dev .
    ```
4. Configure the webserver to run in "dev" mode.
    ```shell
    docker run --rm --name desdm-public \
      -e APP_ROOT="/" -e JIRA_DEFAULT_ASSIGNEE="" \
      -p 8080:8080 \
      -v $(pwd):/home/des \
      -u $(id -u) \
      desdm-public:dev \
      python3 vulcan.py --dev
    ```
5. Run the webserver to serve the webpage.
    ```shell
    docker run --rm --name desdm-public \
      -e APP_ROOT="/" -e JIRA_DEFAULT_ASSIGNEE="" \
      -p 8080:8080 \
      -v $(pwd):/home/des \
      -u $(id -u) \
      desdm-public:dev \
      python3 main.py
    ```
6. Open your browser to http://127.0.0.1:8080 to view the website.
7. Ensure that the ServiceWorker is not registered. Open your web browser's web development tools. In Firefox, use CTRL+SHIFT+I and go to the Application tab. Disable/remove any ServiceWorker you see listed.
8. Edit and save the relevant HTML files. Reload the page and see the results. Repeat this step until satisfied.
9. Commit only the substantive changes to the git repo and push the updates to your GitHub fork. Do not commit the changes related to the "dev mode" configuration.
    ```shell
    git add
    git commit -m 'Updated release page blah'
    git push
    ```
10. Create a pull request to merge and publish your changes.
