from twisted.internet import reactor, defer
import subprocess
from flask import Flask
from .run_crawler import crawl_process
app = Flask(__name__)

@app.route('/')
def hello_world():
   result = crawl_process()

   return result

if __name__ == '__main__':
   app.run()