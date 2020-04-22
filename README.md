# Search-Engine
Simple search engine that uses Boolean and Vector search models. for uOttawa CSI 4107 class
Implemented using python and using Flask as framework
Can handle wildcards such as "manag*" (only for boolean)
Does spell check

STILL IN BETA AND NEEDS A LOT OF BUG FIXES

How to use:
<<<<<<< HEAD
-  make sure regex, nltk, beautifulsoup, numpy, editdistance and flask are installed on your device
  
  `pip install beautifulsoup4 regex numpy editdistance flask`

move to the CSI-4107-Search-Engine-Project directory
`cd CSI-4107-Search-Engine-Project`

run `python3 app/search_engine.py` and flask server will run automatically.
=======
-  make sure re, nltk, beautifulsoup, numpy and flask are installed on your device
- run search_engine.py (in /app) and flask server will run automatically.
>>>>>>> 795930dfc7b7961fc6d60d5fcb34e9ba20106e47
- follow path to website

Types of queries:

Boolean:
- keywords include AND, OR and AND_NOT
- all the terms (including parentheses) must have a single whitespace separating them
- no useless parentheses can be inputed
  i.e: ( student and business ) -> NOT VALID
       student AND ( management OR work* ) -> VALID

Vector:
no specific ways to query, any input should work


  
