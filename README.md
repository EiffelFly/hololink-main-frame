# Hololink

![tele2](https://user-images.githubusercontent.com/57251712/132660686-9f64b34c-0674-4ef8-ac67-bc89056f4341.png)

## Overview

Hololink is built for everyone whom want to gain more insight from reading. It will tokenize the whole article you read and use NLP to generate insights.

## How it works

1. Use hololink-browser-extension to upload the article
2. The text of article will be tokenized and process with our NLP model
3. Tokenized words will be connected and displayed with force directed graph
4. The graph will have insight about how many words are connected, what is your primary word in your study

## Benefit

- In long term, you can store all the words you had read in Hololink, when you encounter a new article, Hololink will compare the words you have and the word the article have to help you decide whether to read the article or not.
- We define technical term as basestone and normal term as stellar, before you read certain article, we can tell you how many basestone term you don't know right now.

## Tech stack

- web-framework: Django
- REST api: Django Rest Framework
- web-services: GCP compute engine

![telescope1_1](https://user-images.githubusercontent.com/57251712/132660185-cd126248-2936-4f56-aa97-b80c2807bba6.gif)
![telescope1_4](https://user-images.githubusercontent.com/57251712/132660195-356f5419-114b-4adf-9e88-8f26fc5b8765.gif)

