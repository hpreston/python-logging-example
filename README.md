# Python Logging Example
Often times when coding up a project I find myself injecting "print statements" all over the place to indicate status or messages important during development and debugging.  Later, I might comment these statements out when "releasing" a script.  While this works, it is a bit cumbersome and there is a better option available to the Python developer.  Python logging.  

This repository provides a very simple example of the same script with and without the logger.  

* [`example-print.py`](example-print.py) is a NETCONF based exmaple that looks up some information from a DevNet Sandbox and uses basic print statements to output to the console status messages.  
* [`example-logger.py`](example-logger.py) is the same script, but uses Python logging to send informational and debug messages to a log file called `mylog.log`.  Error messages will still be printed to the screen. 
* [`logger.conf`](logger.conf) is the Python logging configuration file 

For reference on the Python Logging features, see the [Logging HOWTO](https://docs.python.org/3/howto/logging.html#) from Python.org.  

Also, checkout the blog [Avoiding Silent Automation](https://blogs.cisco.com/developer/avoidingsilentautomation01) by Joe Clarke, Cisco Distinguished Engineer and fellow automation engineer I work with in Learning at Cisco.  His blog is what introduced me to logging in a way that made me want to really dive in and start using it.  