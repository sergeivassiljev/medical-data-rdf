from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Загрузка данных
df = pd.read_excel('request_responses4.xlsx')

# Заменяем np.nan на пустые строки
df['generated_rdf'] = df['generated_rdf'].fillna('')

# Теперь получаем тексты после замены
texts = df['generated_rdf'].values

# Преобразование текстов в TF-IDF векторы
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)

# Расчет косинусного сходства
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Создаем DataFrame для косинусного сходства
sim_df = pd.DataFrame(cosine_sim)

# Сохраняем DataFrame в Excel файл
sim_df.to_excel('cosine_similarity_results4.xlsx', index=False)

print("Результаты косинусного сходства сохранены в файл 'cosine_similarity_results3.xlsx'.")


