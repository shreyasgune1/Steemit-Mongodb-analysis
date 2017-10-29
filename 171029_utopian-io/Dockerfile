FROM python:3

RUN pip install -U steemdata
RUN sed -i 's/(==0.9.3.1)/(==0.9.3)/g' /usr/local/lib/python3.6/site-packages/steem*/METADATA
RUN pip install -U matplotlib
ADD get_utopian-io_posts.py /
ADD analyze_utopian-io_posts.py /
RUN mkdir -p /steemdata/
ENTRYPOINT python get_utopian-io_posts.py && python analyze_utopian-io_posts.py
