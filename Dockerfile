FROM python:3-onbuild
RUN ["python", "setup.py", "install"]
VOLUME ["/root/tsgdata"]
#CMD ["bin/tsg_crawl.py", "author", "--startnumber", "29523"]
EXPOSE 8910
