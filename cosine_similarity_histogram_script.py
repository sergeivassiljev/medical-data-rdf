import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot

def plot_cosine_similarity_histogram(file_path):
    data = pd.read_excel(file_path)

    upper_triangle_values = data.where(np.triu(np.ones(data.shape), k=1).astype(bool)).stack()

    pyplot.figure(figsize=(8, 6))
    pyplot.hist(upper_triangle_values, bins=50, color='blue', alpha=0.7)
    pyplot.title('Distribution of Cosine Similarity Scores')
    pyplot.xlabel('Cosine Similarity')
    pyplot.ylabel('Frequency')
    pyplot.grid(True)
    pyplot.show()

file_path = 'cosine_similarity_results_test_6.xlsx'
plot_cosine_similarity_histogram(file_path)
