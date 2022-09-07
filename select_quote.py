import pandas as pd



def main():
    df = pd.read_csv('himym_quotes.csv')

    df_day = df.sample(n=1)
  
    day_quote = df_day['quote'].iloc[0]
    day_char = df_day['unique_char'].iloc[0]
    print(f'----------\nThe how i met your mother quote of the day is: \n\n{day_quote} \n Said by: {day_char}\n----------')

    past_quotes = []
    past_char = []
    rows_2_remove = []

    past_quotes.append(day_quote)
    past_char.append(day_char)

    #remove from original df the 
    for i in range(len(df)):
        if any(x in df['quote'].iloc[i] for x in past_quotes):
            rows_2_remove.append(i)
            removed_quote = df['quote'].loc[i]
            print(f'\n\nremoved quote:\n {removed_quote} from {day_char}')

    df = df.drop(df.index[rows_2_remove])

    df.to_csv('himym_quotes.csv', index=False)




if __name__ == '__main__':
    main()