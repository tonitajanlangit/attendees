import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

sns.set_style('whitegrid')

# Load data
file_path = 'full-attendee-dataset.csv'
df = pd.read_csv(file_path)

# Title
st.title("Attendees Data Analysis")

# Show dataframe
if st.checkbox("Show raw data"):
    st.write(df.head())

# Missing values handling
missing_values = df.isnull().sum()
st.write("### Missing Values", missing_values)

# Data Cleaning
fill_values = {
    'Is it ok to share your contact for networking? This is a networking event after all :)': 'Yes',
    'What will you help you best with your AI project or startup ideas? (Helps us plan better programming for you!)': 'No response',
    'Are you interested in contributing to the GenAI collective community?': 'No response',
    'Which of the following best describes your background? ': 'Unknown',
    'custom_source': 'Direct',
    'Pls specify area of interest (if selected other)': 'No response'
}
df.fillna(fill_values, inplace=True)

# Approval Status
st.subheader("Approval Status")
approval_counts = df.groupby('approval_status').size()
fig, ax = plt.subplots()
approval_counts.plot(kind='barh', color=sns.color_palette('Dark2'), ax=ax)
ax.set_title('Attendees Approval Status')
ax.set_xlabel('Number of Attendees')
ax.set_ylabel('Approval Status')
st.pyplot(fig)

# Background of Attendees
st.subheader("Background of Attendees")
all_keywords = [kw.strip().lower() for row in df['Which of the following best describes your background? '] for kw in str(row).split(',')]
keyword_counts = Counter(all_keywords)
keywords, counts = zip(*sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True))
fig, ax = plt.subplots()
ax.pie(counts, labels=keywords, autopct='%1.1f%%', startangle=90)
ax.set_title('Background of Attendees')
st.pyplot(fig)

# Contact Sharing Preferences
st.subheader("Contact Sharing Preferences")
df['Is it ok to share your contact for networking? This is a networking event after all :)'].replace(['Yes', 'yes'], 'Yes', inplace=True)
fig, ax = plt.subplots()
sns.countplot(x='Is it ok to share your contact for networking? This is a networking event after all :)', data=df, ax=ax)
ax.set_title('Contact Sharing Preferences')
ax.set_xlabel('Willing to Share Contact')
ax.set_ylabel('Number of Attendees')
st.pyplot(fig)

# Top AI Interests
st.subheader("Top AI Interests")
all_keywords = [kw.strip().lower() for row in df['Which part of AI interests you most?'] for kw in str(row).split(',')]
keyword_counts = Counter(all_keywords)
top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]
keywords, counts = zip(*top_keywords)
fig, ax = plt.subplots()
sns.barplot(x=list(keywords), y=list(counts), ax=ax)
ax.set_xticklabels(keywords, rotation=45, ha='right')
ax.set_xlabel('Category')
ax.set_ylabel('Frequency')
ax.set_title('Top AI Interests')
st.pyplot(fig)

# Word Cloud for Best Support for AI Projects
st.subheader("Best Support for AI Projects")
text = ' '.join(df[df['What will you help you best with your AI project or startup ideas? (Helps us plan better programming for you!)'] != 'No response']['What will you help you best with your AI project or startup ideas? (Helps us plan better programming for you!)'].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=STOPWORDS).generate(text)
fig, ax = plt.subplots()
ax.imshow(wordcloud)
ax.axis("off")
st.pyplot(fig)

# Custom Source Distribution
st.subheader("Custom Source Distribution (excluding 'Direct')")
fig, ax = plt.subplots()
sns.countplot(data=df[df['custom_source'] != 'Direct'], x='custom_source', ax=ax)
ax.set_title('Custom Source Distribution')
ax.set_xlabel('Custom Source')
ax.set_ylabel('Count')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig)
