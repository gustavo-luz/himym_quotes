import requests
from bs4 import BeautifulSoup
import pandas as pd
import re



def generate_csv(url):
    #generate csv from web
    r = requests.get(url)
    soup =   BeautifulSoup(r.content,"lxml")
    myList = soup.find_all('body')

    quotes = []
    for l in myList:
        ulList = l.find_all('li')
        for li in ulList:
            #print(li)
            quotes.append(li)

    #print(quotes)

    df = pd.DataFrame(quotes)
    df.to_csv('raw_himym_quotes.csv', index=False)
    return df



def main():
    
    #generate_csv("https://www.scarymommy.com/how-i-met-your-mother-quotes")

    df = pd.read_csv('raw_himym_quotes.csv')

    df = df.rename(columns={df.columns[0]: "raw_data"}, errors="raise")

    df = df.explode("raw_data")

    print(df['raw_data'][0])

    df['first'] = df['raw_data']

    df[df.columns] = df.apply(lambda x: x.str.strip())

    stop_words = ['<li>']

    df['first'] = df['raw_data']
    #split the phrase and name of char
    df['first']= df['raw_data'].str.strip('<li>').str.strip('“')

    df[['quote','char']] = ''
    print(df)

    stop_words = ["</","<em>","</em>","em>",'"','”',', ref']

    char_dict = {
        "Barney","Barney Stinson",
        "Lily","Lily Aldrin",
        "Robin","Robin Scherbatsky",
        "Ted","Ted Mosby",
        "Marshall","Marshall Eriksen"

    }

    for i in range(len(df)):
        for j in range(len(stop_words)):
            df['first'].iloc[i] = df['first'].iloc[i].replace(stop_words[j],'')
        
        if len(df['first'].iloc[i].split("—")) > 2:
            len_multiple_= len(df['first'].iloc[i].split("—"))
            #print(len_multiple_,df['first'].iloc[i].split("—"))
            df['quote'].iloc[i] = ("—".join(df['first'].iloc[i].split("—")[0:(len_multiple_ - 1)]))
            print(i,len_multiple_,df['quote'].loc[i])

        df['quote'].iloc[i] = re.sub('<.*?>', '', df['first'].iloc[i].split("—")[0].replace('a>',''))

        df['char'].iloc[i] = df['first'].iloc[i].split("—")[-1].replace('a>','').strip(" ")
        df['char'].iloc[i] = re.sub('<.*?>', '', df['char'].iloc[i].split("—")[0])
    #criar um regex pra ver qual personagem falou o que
    # 
    #remover as que estão sem personagem e a penny mosby

    #tirar as do barney machistas

    #116 117 128: nome aparecendo no inicio da string

    print(df)
    print(type(df['raw_data']))
    df.to_csv('himym_quotes.csv', index=False)


if __name__ == '__main__':
    main()
