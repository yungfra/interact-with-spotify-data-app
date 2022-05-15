from functools import total_ordering
from numpy import isin
import pandas as pd
import streamlit as st
import plotly.express as px

# My Spotify Analytics Project

## Setting the page title and the icon, for a nice aestethic.
st.set_page_config(page_title="Spotify Analytics Project", page_icon=":headphones:")

## Hiding the menu button.
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# Condense the layout
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

## Reading the data.
df = st.cache(pd.read_csv)("Data/song_df.csv")

# Sidebar
st.sidebar.header(":exclamation: Please Filter Here.")

artist = st.sidebar.multiselect(
    "Filter by artists:",
    options=df["artist_name"].unique(),
    default=df["artist_name"].unique()
)

st.sidebar.write('You can use this section to filter data by selecting only the artists whose analytics you want to view.')

df_selection = df.query(
   "artist_name == @artist" 
)


## Main page

## Making the title.
st.title(':headphones: Spotify Recent Tracks Analytics Project!')

## Display data.
if st.checkbox('Display data'):
    st.subheader('Data')
    st.dataframe(df_selection)

## Dataframe for the streams section
artist_names = []
for index in df_selection['artist_name'].value_counts().index:
    artist_names.append(index)

streams_list = []
for value in df_selection['artist_name'].value_counts().values:
    streams_list.append(value)

df_dict={
    "artist_name": artist_names,
    "streams": streams_list
}


streams_df = pd.DataFrame(data=df_dict, columns=['artist_name', 'streams'])

## Streams section
st.header('Streams')
st.write('In this section you can see how many times I have streamed songs by a particular artist. Streaming is valid only if the artist is the main artist of the song (not featuring!)')

streamed_artists = (
    streams_df
)

fig_streamed_artists = px.bar(
    streamed_artists,
    x = "streams",
    y=streamed_artists['artist_name'],
    orientation="h",
    title="<b>Number of streams per artist</b>",
    color_discrete_sequence=["#0083B8"] * len(streamed_artists),
    template="plotly_white"
)

st.plotly_chart(fig_streamed_artists)


## Popularity and Available Markets Section
st.header('Popularity-Available Markets')
st.write('In this section you can check the popularity level of the single songs compared to the number of markets in which they are available.')

if(st.checkbox("What's popularity?")):
    st.warning("According to Spotify: “Popularity is calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how recent those plays are.\"")

## Dataframe for the popularity and available markets section
song_name_list = []
for song in df_selection['song_name']:
    song_name_list.append(song)

popularity_list = []
for value in df_selection['popularity']:
    popularity_list.append(value)

available_markets_list = []
for value in df_selection['available_markets']:
    available_markets_list.append(value)

df_dict_2={
    "song_name": song_name_list,
    "popularity": popularity_list,
    "available_markets": available_markets_list
}

popularity_df = pd.DataFrame(data=df_dict_2, columns=['song_name', 'popularity', 'available_markets'])

fig = px.bar(popularity_df, x="song_name", y=["popularity", "available_markets"], barmode='group', height=600)
st.plotly_chart(fig)

st.success('Most popular song of the (filtered) database: {}' .format(df_selection[df_selection['popularity'] == df_selection['popularity'].max()]['song_name'].values[0]))
st.error('Least popular song of the (filtered) database: {}' .format(df_selection[df_selection['popularity'] == df_selection['popularity'].min()]['song_name'].values[0]))

## Additional data section
st.header('Additional data')
total_songs_before = df.shape[0]
total_songs_after = df_selection.shape[0]

status = st.radio("Select: ", ('Total songs (in the dataframe)', 'Total songs (after filtering)'))
 
if (status == 'Total songs (in the dataframe)'):
    st.subheader("Total songs (in the dataframe): {}" .format(total_songs_before))
else:
    st.subheader("Total songs (after filtering): {}" .format(total_songs_after))
    

st.warning('To display the raw data please go to the top of the page and check the "display data" checkbox.')

## Conclusions section
st.header('Conclusions')
st.write('As you can see from the analytics, I could be a perfect Posty groupie: he\'s pretty popular as well! :grimacing:')
st.success('In order to see how I extracted and transformed data from the Spotify API, please visit my github page :heart:')