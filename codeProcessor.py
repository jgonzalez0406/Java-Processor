import re
import javalang
import argparse
import os
import requests
from flask import Flask, jsonify, request
from codeManager import CodeManager

app = Flask(__name__)


def insert_custom_comment(existing_comment, custom_comment):
    if existing_comment:
        lines = existing_comment.split("\n")
        lines.insert(1, " * " + custom_comment)
        return "\n".join(lines)
    else:
        return "/**\n * " + custom_comment + "\n */"

class CodeProcessor:
    def __init__(self, directory):
        self.directory = directory
        self.parser = CodeManager()

    def process_methods(self):
        output = ""

        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".java"):  # Process only Java files
                    java_filepath = os.path.join(root, file)

                    # Read the contents of the Java file
                    with open(java_filepath, 'r') as f:
                        java_code = f.read()

                    method_names = self.parser.get_method_decl(java_code)

                    for method_name in method_names:
                        print("Method name:", method_name)
                        method_text = self.parser.get_method_code(method_name, java_code)
                        method_comments = self.parser.get_method_comments(method_name, java_code)
                        method_description = generate_method_description(method_text) #processes through flask server

                        if method_comments != "":
                            updated_method_comment = insert_custom_comment(method_comments, method_description)
                            output += updated_method_comment + "\n" + method_text + "\n"
                            print(updated_method_comment)
                            print(method_text)

                        print()

        return output

#responsible for chatGPT comment
def generate_method_description(method_text):
    url = 'http://localhost:5000/generate-description' #creates url
    payload = {'method_text': method_text} #dictionary
    response = requests.post(url, json=payload) #sends request over

    if response.ok:
        data = response.json()
        method_description = data['method_description']
        return method_description
    else:
        # Handle the case when the request to the Flask script fails
        return ""



chat = ContextChat()



# Parse the command-line arguments
arg_parse = argparse.ArgumentParser(description='Create a new Java file.')
arg_parse.add_argument('filename', help='Name of the Java file')
arg_parse.add_argument('directory', help='Path to the directory containing Java files')

args = arg_parse.parse_args()

# Create an instance of CodeProcessor
processor = CodeProcessor(args.directory)

# Call the process_methods method
output = processor.process_methods()

java_filename = args.filename + ".java"
with open(os.path.join(args.directory, java_filename), 'w') as file:
    file.write(output)

print("Java file '{}' created.".format(java_filename))
