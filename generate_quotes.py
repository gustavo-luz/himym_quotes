from multiprocessing.sharedctypes import Value
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
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

    #print(df['raw_data'][0])

    df['first'] = df['raw_data']

    df[df.columns] = df.apply(lambda x: x.str.strip())

    stop_words = ['<li>']

    df['first'] = df['raw_data']
    #split the phrase and name of char
    df['first']= df['raw_data'].str.strip('<li>').str.strip('“')
    
    #create empty columns that will be populated
    df[['quote','char','unique_char']] = ''
    

    stop_words = ["</","<em>","</em>","em>",'"','”',', ref','a>']

    char_dict = {
        "Barney":"Barney Stinson",
        "Lily":"Lily Aldrin",
        "Robin":"Robin Scherbatsky",
        "Ted":"Ted Mosby",
        "Marshall":"Marshall Eriksen"
    }


    innapropriate_quotes = [
        'Every Halloween, I bring a spare costume, in case I strike out with the hottest girl at the party. That way, I have a second chance to make a first impression.',
        'The only reason to wait a month for sex is if she’s 17 years, 11 months old.',
        'I just want to say from the bottom of my heart… I’m going to kill you.',
        'That’s love, bitch.',
        'Oh, come on! I haven’t seen that much hooking go unpunished since my last trip to Vegas.',
        'Every hookup at a weekend wedding is decided at Friday Night Drinks. Get stuck with the wrong girl tonight, the only action you’ll be getting all weekend is a self five, and I don’t mean the cool kind. Self-five! That’s the cool kind.',
        'The biggest case of my life and I’d already lost the jury. I mean, I’ve heard of Twelve Angry Men, but this was more like ‘Twelve Horny Women.',
        'You guys bangin’? Keep goin’, I’m not even here. But just for the record? Having a baby? Big mistake. ',
        'I can’t wait to tell the gang. This is one of those moments you dream about! Guys… Lily and I… are having unprotected sex. I just got the chills.',
        'There’s three rules of cheating: One — it’s not cheating if you’re not the one who’s married. Two — it’s not cheating if her name has two adjacent vowels. Three — and it’s not cheating if she’s from a different area code.',
        'Yeah, I wasn’t really listening either. Ted can really go on about a bitch. '
     ]

    rows_2_remove = []


    for i in range(len(df)):
        for j in range(len(stop_words)):
            df['first'].iloc[i] = df['first'].iloc[i].replace(stop_words[j],'')


        df['quote'].iloc[i] = re.sub('<[^>]+>', '', df['first'].iloc[i])
        df['quote'].iloc[i] = df['quote'].iloc[i].replace('a>','')


        if len(df['first'].iloc[i].split("—")) >= 2:
            len_multiple_= len(df['first'].iloc[i].split("—"))
            #print(len_multiple_,df['first'].iloc[i].split("—"))
            df['quote'].iloc[i] = ("—".join(df['quote'].iloc[i].split("—")[0:(len_multiple_ - 1)]))
            #print(i,len_multiple_,df['quote'].loc[i])
        
        
        df['char'].iloc[i] = df['first'].iloc[i].split("—")[-1].replace('a>','').strip(" ")
        df['char'].iloc[i] = re.sub('<.*?>', '', df['char'].iloc[i].split("—")[0])

        #116 117 128: nome aparecendo no inicio da string
        #print(len(char_dict))
        for key in range(len(char_dict)):

            if list(char_dict.keys())[key] in df['char'].iloc[i]:

                df['unique_char'].iloc[i] = list(char_dict.values())[key]

        #tirar as do barney machistas

        #if any(innapropriate_quotes) in df['quote'].iloc[i]:
        if any(x in df['quote'].iloc[i] for x in innapropriate_quotes):
            #df['quote'].iloc[i] = np.NaN
            #print(df['quote'].iloc[i])
            rows_2_remove.append(i)

    
    #remover as que estão sem personagem e a penny mosby 102,131
    #invert the list and remove index of df backwards
    rows_2_remove = rows_2_remove[::-1]
    #print(rows_2_remove)
    df = df.drop(df.index[rows_2_remove])
    df = df.dropna()
    df['tweet'] = df['quote'] + df['unique_char']   
    #remove strings not regognized as na and tweets bigger than max lenght
    mask = (df['unique_char'].str.len() > 2) & (df['tweet'].str.len() < 275)
    df = df.loc[mask]
    df = df[['quote','unique_char','tweet']] 

    #df['quote'] = df['quote'][1:-1] 
    df.quote.str.rstrip()
    print(df)

    df.to_csv('himym_quotes.csv', index=False)


if __name__ == '__main__':
    main()
