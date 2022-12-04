# UNICORN

Local Setup:

1. set up virtual environment:  python3 -m venv venv

2. install packages:  pip3 install -r requirements.txt

3. run the app: flask run

4. query the app using provided test: python3 tests/query.py

Docker Setup:

1. pull the docker image from docker hub: docker pull bk121/platformtm-nlp:latest

2. run the docker container: docker run -p 8000:8000 -v `pwd`/datasets:/usr/src/app/datasets -it bk121/platformtm-nlp

3. query the app using provided test: python3 tests/query.py



The app makes two endpoints available: 'plain' and 'prompt'. 

The 'plain' endpoint expects a project name, a dataset name, a property name, and a column parser as arguments. It will then return a .csv file 
with a mapping of the property values from their original values into a standardised format. This mapping has been done in advance by a call to 
gpt3 with a prompt designed by a non-medical expert.

The 'prompt' endpoint expects a project name, a dataset name, a property name, a column parser, and a prompt as arguments. It will then return a .csv file 
with a mapping of the property values according to the prompt that has been provided. This takes a while to process as many calls to the gpt3 language 
model need to be made. The prompt can take any form as long is it formatted regularly.
One example might be: 

prompt = "Example: 2 years and 3 months\nOutput: 27 months\n\nExample: 1 year and 9 months\nOutput: 21 months\n\nExample: 12 weeks\nOutput: 3 months\n\n
Example: 23\nOutput: 23 months\n\nExample: 19\nOutput: 19 months\n\nExample: 3 years and 4 months\nOutput: 40 months\n\nExample: 16 weeks\nOutput: 4 months
\n\nExample: I think about 17 months\nOutput: 17 months\n\nExample: not sure\nOutput: unknown\n\nExample: "

Note that each call to gpt3 will append a value from the list of property values to this prompt to make up the entire input to the gpt3 model.
