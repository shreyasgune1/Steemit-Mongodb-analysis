# Utopian.io usage statistics Sept.-Oct. 2017

This uses the MongoDB interface to the Steem blockchain provided by [steemdata.com](https://steemdata.com/).
The `steemdata` python module provides all infrastructure that is needed.
The environment for `steemdata` is provded with a `docker` image.

## Usage
```
./run.sh
```
This
* builds a docker image `utopian-post-analysis`
* creates a subdirectory `steemdata` on the host
* starts the docker image with the local `steemdata` folder mapped to `/steemdata/` in the container
  * `get_utopian-io_posts.py` queries the database and writes all posts and comments into a shelve file
  * `analyze_utopian-io_posts.py` reads the shelve file, runs the data analysis and creates the graphs in the `steemdata` directory
