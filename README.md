# Java Processor
This goes through each Java file in a specified directory and extracts the method names, code, and pre-existing comments using Python. 
The code of each method is sent over to a flask server which generates a short description using a GPT-3.5 model that will be inserted into a comment block.
The processed file with its new comments is then added to the specified directory.

#### About me
[Juliana Gonzalez](https://jgonzalez0406.github.io/)

## Requirements
* Python 3
* Install the required dependencies by running:
  ```
   pip install -r requirements.txt
  ```
  * This contains Flask, tiktoken, torch, javalang, argparse
* Use one of the models on [APCL](https://huggingface.co/apcl) for the checkpoint file:
    * [jam](https://huggingface.co/apcl/jam)
    * [jam_sojm](https://huggingface.co/apcl/jam_sojm)
    * [jam_so](https://huggingface.co/apcl/jam_so)
  
## Usage
* After installing the appropriate dependencies and files, first run `myApp.py` since the code runs locally and will need to be running before anything else
* To run `codeProcessor.py`, execute
  ```
  python3 codeProcessor.py <filename> <directory>
  ```
  * `<filename>`: Name for the new file
  * `<directory>`: Name for the specified directory containing Java files to be processed
* The code will process each Java file in `<directory>`, generate method descriptions in the Flask server, and then update the Java files with the descriptions under `<filename>`
* Check the console for progress and to view the new file
