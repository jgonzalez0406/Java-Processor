# Java Processor
This goes through each Java file in a specified directory and extracts the method names, code, and pre-existing comments. 
The code of each method is sent over to a flask server which generates a short description using a GPT-3.5 model that will be inserted into a comment block.
The processed file with its new comments is then added to the specified directory.

## Requirements
* Python 3
* Install the required dependencies by running:
  ```
   pip install -r requirements.txt
  ```
  * This contains Flask, tiktoken, torch, javalang, argparse
