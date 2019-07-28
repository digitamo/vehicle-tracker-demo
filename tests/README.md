
### Running automation tests and back-end integration.

- Install dependencies
```
$ cd tests
$ pip install -r requirements
```

- Install chrome driver for selenium:
    
    If you're running ubuntu you can use this:
    ```
       $ wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
       $ unzip chromedriver_linux64.zip
       $ sudo mv chromedriver /usr/bin/chromedriver
       $ sudo chown root:root /usr/bin/chromedriver
       $ sudo chmod +x /usr/bin/chromedriver
    ```
  `NOTE: `Please make sure that the driver version matches your chrome version.  
    
   You can find more instructions on installing chrome driver for selenium [here](https://selenium-python.readthedocs.io/installation.html#downloading-python-bindings-for-selenium). 

- Running tests:
```
$ nosetests
```