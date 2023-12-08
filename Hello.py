import streamlit as st
import pandas as pd
import os

# @st.cache_data
def load_words():
  dirname=os.getcwd()
  fname=dirname+"/data/wordlist"
  words = [line.rstrip('\n') for line in open(fname, 'r')]
  return words

def dist(word1,word2):
  if(len(word1)!=len(word2)):
    return -1
  diff=0
  for i in range(len(word1)):
    if(word1[i]!=word2[i]):
      diff+=1
  return diff

# @st.cache_data
def process_words():
  neighbors={}
  words=load_words()
  for word1 in words:
    for word2 in words:
      if(dist(word1,word2)==1):
        if word1 not in neighbors:
          neighbors[word1]=word2
        else:
          neighbors[word1]=neighbors[word1]+","+word2
  return neighbors
  



if "words" not in st.session_state:
  st.session_state.words=load_words()
words=st.session_state.words

if "neighbors" not in st.session_state: 
  st.session_state.neighbors=process_words()
neighbors=st.session_state.neighbors

print(f"Neighbors length = {len(neighbors)}")
with st.expander("Show neighbors"):
  st.table(list(neighbors.items()))

st.title("# Weaver")
st.write("## A simple word game")
if word := st.text_input("Enter a 4-letter word"):
  st.write("You entered: ", word)
  if(word not in words):
    st.write("Not a word in our dictionary. Try again.")
  elif word in neighbors:
    st.write("Neighbors: ", neighbors[word])
    st.write("Number of neighbors: ", len(neighbors[word]))
    st.write("Number of words: ", len(words))
  else:
    st.write("No neighbors found. Try again.")

