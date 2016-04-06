# Crawler specification

The crawler simply crawls the html of all *interesting* pages.

## Directory/File structure

The raw html files are saved in a directory raw/. Inside raw there are three folders:

- author
- journal
- conference

### File names

The files go to the corresponding folders. The file names are as follows:

For an author with this URL: *http://dblp.uni-trier.de/pers/hd/w/Walker:David*

the file name is w_Walker:David.html

For a conference http://dblp.uni-trier.de/db/conf/popl/popl2016.html it is

popl_popl2016.html

For a journal http://dblp.uni-trier.de/db/journals/toplas/toplas38.html it is

toplas_toplas38.html


# Technology

Libraries

## Important links:

http://dblp.uni-trier.de/pers?pos={}
{}=1,301,601,..

http://dblp.uni-trier.de/db/journals/?pos={}
{}=1,101,201,...

http://dblp.uni-trier.de/db/conf/?pos={}
{}=1,101,201,...


## requests

url
data = requests.get(url)


data.data
data.status_code

## xpath (look for a python library)

//div[@id="browse-person-output"]/div[@class="columns hide-body"]/div/ul/li/a/@href


def save_one_file(url):
  webpage = request.get(url)
  filename = url.something # exftract filename from url.
  with open(filename) as f:
    f.write(webpage.data)

## Invalid Links

### Invalid Journals
1. IEEE Transactions on Circuits and Systems I: Fundamental Theory and Applications
2. IEEE Transactions on Circuits and Systems I: Regular Papers
3. IEEE Transactions on Circuits and Systems II: Analog and Digital Signal Processing
4. IEEE Transactions on Circuits and Systems II: Express Briefs
5. IEICE Transactions on Communications
6. IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences
7. IEICE Transactions on Information & Systems
8. Information & Systems; IEICE Transactions on ...

