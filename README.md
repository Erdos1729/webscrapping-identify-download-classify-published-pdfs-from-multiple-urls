## Webscrapping to identify and download latest pdf documents. Classify these documents into pre-defined categories.

-   This repository will assist you in scrapping data from multiple websites. It will download the latest pdf files published on a website in a specific folder as per the users requirement. This can be used for automating various operations involved in market research.
-   Once the pdfs are downloaded they are classified into oil/no_oil/foreign_language categories based on a string based rule
-   You can customize these rules for classification as per your need

## Instructions

-   pip install -r requirements
-   Run radar_automation.py

## Reference

I devised the solution from the following pages of the documentation:

-   [![Urllib](https://docs.python.org/3/library/urllib.html#:~:text=urllib%20is%20a%20package%20that%20collects%20several%20modules%20for%20working%20with%20URLs%3A&text=request%20for%20opening%20and%20reading,the%20exceptions%20raised%20by%20urllib.)] package that collects several modules for working with URLs
-   [![beautyfulsoup4](https://pypi.org/project/beautifulsoup4/)] to scrape information from web pages
-   [![PDFminer](https://pypi.org/project/pdfminer/)] is a text extraction tool for PDF documents
-   [![NLTK](https://pypi.org/project/nltk/)] for natural language processing
-   Keyword based search in extracted text for rule based classification