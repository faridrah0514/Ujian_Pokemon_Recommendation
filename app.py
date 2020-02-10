from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def find_pokemon_recommendation(name):
    pokemon_name = name
    pokemon_name = pokemon_name.capitalize()
    pokemon_index = df[df['Name'] == pokemon_name].index[0]
    recom = list(enumerate(score[pokemon_index]))
    pokemon_index_list = sorted(recom, key=lambda x:x[1], reverse=True)[0:10]
    idx = [i[0] for i in pokemon_index_list]
    df_recomm=df.iloc[idx][['Name', 'Type 1', 'Generation', 'Legendary']]
    print(df_recomm)
    lst=[]
    url='https://pokeapi.co/api/v2/pokemon'
    for i in range(df_recomm.shape[0]):
        dct={}
        dct['Name'] = df_recomm.iloc[i]['Name']
        print(url+'/'+dct['Name'].lower())
        try:
            api=requests.get(url+'/'+dct['Name'].lower())
            data_pokemon = api.json()
        except:
            continue
        gambar = data_pokemon['sprites']['front_default']
        dct['Gambar'] = gambar
        dct['Type 1'] = df_recomm.iloc[i]['Type 1']
        dct['Generation'] = df_recomm.iloc[i]['Generation']
        dct['Legendary'] = df_recomm.iloc[i]['Legendary']
        # print(df_recomm.iloc[i]['Name'])
        lst.append(dct)
    # return pd.DataFrame(lst)
    return lst[:7]

@app.route('/', methods=['POST', 'GET'])
def func1():
    return render_template("home.html")

@app.route("/hasil", methods=['POST'])
def func2():
    # global makan
    # try:
    if request.method == 'POST':
        data = request.form
        data=data
        name_pok=data['pokemon'].lower()
        print(name_pok)
        # url='https://pokeapi.co/api/v2/pokemon'
        # api=requests.get(url+'/'+name_pok)
        recommendation = find_pokemon_recommendation(name_pok)
        print(recommendation)
        # data_pokemon = api.json()
        # gambar = data_pokemon['sprites']['front_default']
        pokemon_favorit=recommendation[0]
        final_data = {
            'Name': pokemon_favorit['Name'],
            'Gambar': pokemon_favorit['Gambar'],
            'Type 1': pokemon_favorit['Type 1'],
            'Generation': pokemon_favorit['Generation'],
            'Legendary': pokemon_favorit['Legendary']
        }
        return render_template(
            "result.html", 
            data=final_data, 
            df=recommendation[1:]
            )
    # except:
    #     return render_template('not_found.html')

if __name__ == "__main__":
    
    df = pd.read_csv('dataset/Pokemon.csv')
    # df.shape
    arr=[]
    for i in range(df.shape[0]):
        val = str(df.loc[i]['Type 1'])+' '+str(df.loc[i]['Generation'])+' '+str(df.loc[i]['Legendary'])
        arr.append(val)

    df['feature'] = np.array(arr)
    c_vect = CountVectorizer(tokenizer= lambda x : x.split(' '))
    matrix = c_vect.fit_transform(df['feature'])
    score = cosine_similarity(matrix)
    # makan="makan nasi"

    app.run(debug=True)