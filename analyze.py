from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Andmete laadimine Excel-failist, eeldades, et pole päiseid
df = pd.read_excel('cleared_text_6.xlsx', header=None)

# Kasutame esimest veergu (veerg 0), kuna ei ole päiseid
texts = df[0].values  # Saame tekstid otse esimesest veerust

# Tekstide teisendamine TF-IDF vektoriteks
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)

# Kosinussarnasuse arvutamine
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# DataFrame'i loomine kosinussarnasuse jaoks
sim_df = pd.DataFrame(cosine_sim)

# DataFrame'i salvestamine Exceli faili
sim_df.to_excel('cosine_similarity_results_test_6.xlsx', index=False)

print("Kosinussarnasuse tulemused on salvestatud faili 'cosine_similarity_results.xlsx'.")





