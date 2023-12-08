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

def solve(word1,word2,bannedlist):
  distances={}
  predecessors={}
  st.write(f"word1={word1}, word2={word2}, bannedlist={bannedlist}")
  for word in words:
    distances[word]=-1
  distances[word1]=0
  for w in bannedlist:
    distances[w]=-2
  queue=[word1]
  while(len(queue)>0):
    word=queue.pop(0)
    if word==word2:
      break
    if word in neighbors:
      for neighbor in neighbors[word].split(","):
        if distances[neighbor]==-1:
          distances[neighbor]=distances[word]+1
          predecessors[neighbor]=word
          queue.append(neighbor)
  if word2 in distances:
    st.write(f"Distance between {word1} and {word2} is {distances[word2]}")
    path=[]
    word=word2
    while(word!=word1):
      path.append(word)
      word=predecessors[word] 
    path.append(word1)
    path.reverse()
    st.write(f"Path is {path}")


st.title("# Weaver")
st.write("## A simple word game")
word1 = st.text_input("Enter the start word (4-letters)")
word2 = st.text_input("Enter the end word (4-letters)")
word3 = st.text_input("Enter the comma-separated banned words (4-letters)")
if word1 and word2:
  li=word3.split(",") if word3 else []
  if word1 in words and word2 in words:
    st.write(f"You entered: {word1} & {word2}")
    solve(word1,word2,li)
  else:
    if word1 not in words:
      st.write(f"Start word {word1} is not in the dictionary")
    if word2 not in words:
      st.write(f"End word {word2} is not in the dictionary")



