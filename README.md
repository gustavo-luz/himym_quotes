# himym_quotes

One day i had the idea to gather public quotes of how i met your mother 

![Alt Text](https://media.giphy.com/media/13hZL3j0Dcmsso/giphy.gif)

This is progress work to parse how i met you mother quotes and tweet one quote by day.

Future works can include an api to be consumed by other clients with the quote of the day and a website with all quotes

```python
'generate_quotes.py'
```

includes data consuming and formatting from html of https://www.scarymommy.com/how-i-met-your-mother-quotes creating a csv file

Also, an innapropriate_quotes list was created to exclude not cool quotes from barney

![Alt Text](https://media.giphy.com/media/knwUMC1D5Ce1a/giphy.gif)

```python
'select_quote.py'
```

selects a quote from the csv generated and creates a post json consumed by 'tweet_bot.py'

```python
'app.py'
```
Is a trial to create and host the server

