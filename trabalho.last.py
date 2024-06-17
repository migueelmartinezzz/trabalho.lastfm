import streamlit as st
import requests
import matplotlib.pyplot as plt
from collections import Counter

def get_similar_artists(artist_name, api_key):
    url_similar = f'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist={artist_name}&api_key={api_key}&format=json'
    response_similar = requests.get(url_similar)
    
    if response_similar.status_code == 200:
        data = response_similar.json()
        similar_artists = Counter()
        
        for artist in data['similarartists']['artist']:
            artist_name = artist['name']  # Renomeie para artist_name para simplificar
            url_info = f'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_name}&api_key={api_key}&format=json'
            response_info = requests.get(url_info)
            
            if response_info.status_code == 200:
                data_info = response_info.json()
                
                if 'artist' in data_info:
                    listeners = data_info['artist']['stats']['listeners']
                    similar_artists[artist_name] = listeners
                else:
                    st.warning(f"Não foi possível obter informações para o artista {artist_name}.")
            else:
                st.warning(f"Erro ao consultar a API para o artista {artist_name}: {response_info.status_code}")
        
        return similar_artists
    else:
        st.error("Erro ao consultar a API: {}".format(response_similar.status_code))
        return None

def plot_popularity(similar_artists):
    if similar_artists:
        names = list(similar_artists.keys())[:10]
        popularity = list(similar_artists.values())[:10]
        plt.figure(figsize=(10, 6))  # Ajuste o tamanho conforme necessário
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
    
    st.markdown(
    """
    <style>
    .stApp {
        background: url('https://github.com/migueelmartinezzz/trabalho.lastfm/blob/main/fundo%20site%20miguel.jpg?raw=true') no-repeat center center fixed;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    
    if artist_name:
        similar_artists = get_similar_artists(artist_name, api_key)
        if similar_artists:
            st.write(f"Artistas semelhantes a '{artist_name}':")
            for artist, popularity in similar_artists.most_common(10):
                st.write(f"{artist}: {popularity} ouvintes")
            plot_popularity(similar_artists.most_common(10))
        else:
            st.warning("Não foi possível obter artistas semelhantes ao seu favorito.")

if __name__ == "__main__":
    main()
