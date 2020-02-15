# Search-Engine
Simple search engine that uses Boolean and Vector search models. for uOttawa CSI 4107 class
Implemented using python and using Flask as framework
Can handle wildcards such as "manag*" (only for boolean)
Does spell check

STILL IN BETA AND NEEDS A LOT OF BUG FIXES

How to use:
-  make sure re, nltk, beautifulsoup, numpy and flask are installed on your device
- run search_engine.py (in /app) and flask server will run automatically.
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


  
