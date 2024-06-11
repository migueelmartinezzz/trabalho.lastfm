import streamlit as st
import requests
import matplotlib.pyplot as plt
from collections import Counter

def get_similar_artists(artist_name, api_key):
    url = f'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist={artist_name}&api_key={api_key}&format=json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        similar_artists = Counter()
        for artist in data['similarartists']['artist']:
            novo_nome = artist['name']
            url = f'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={novo_nome}&api_key={api_key}&format=json'
            response = requests.get(url)
            data2 = response.json()
            if 'artist' in data2:
                similar_artists[novo_nome] = data2['artist']['stats']['listeners']
        return similar_artists
    else:
        st.error("Erro ao consultar a API: {}".format(response.status_code))
        return None

def plot_popularity(similar_artists):
    if similar_artists:
        names = list(similar_artists.keys())
        popularity = list(similar_artists.values())
        plt.figure(figsize=(50, 25))
        plt.barh(names, popularity, color='skyblue')
        plt.xlabel('Popularidade')
        plt.ylabel('Artista')
        plt.title('Popularidade dos Artistas Semelhantes')
        plt.gca().invert_yaxis()
        st.pyplot(plt)
    else:
        st.warning("Não foi possível plotar o gráfico, dados ausentes.")

def main():
    st.title("HPIYFA")
    st.header('How :red[Popular] Is Your Favorite Artist?')
    st.subheader('O site que te mostra os :blue[artistas mais populares] relacionados ao seu fave', divider='rainbow')
    api_key = '7df4a32d7aec2f6a2fbe9cd02c3a5a6e'
    artist_name = st.text_input("Digite o nome do seu artista favorito:")
    #st.markdown("<style></style>", unsafe_allow_html=true)
    
    if artist_name:
        similar_artists = get_similar_artists(artist_name, api_key)
        if similar_artists:
            st.write(f"Artistas semelhantes a '{artist_name}':")
            for artist, popularity in similar_artists.most_common(10):
                st.write(f"{artist}: {popularity} ouvintes")
            plot_popularity(similar_artists)
        else:
            st.warning("Não foi possível obter artistas semelhantes ao seu favorito.")

if __name__ == "__main__":
    main()
