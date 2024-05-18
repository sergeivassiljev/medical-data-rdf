import pandas as pd
import seaborn as sns
import matplotlib.pyplot as pyplot

def plot_cosine_similarity_heatmap(file_path):
    data = pd.read_excel(file_path)
    
    pyplot.figure(figsize=(10, 8))
    heatmap = sns.heatmap(data, cmap='coolwarm', annot=False)
    pyplot.title('Heatmap of Cosine Similarity')
    pyplot.xlabel('Document Index')
    pyplot.ylabel('Document Index')
    pyplot.show()

file_path = 'cosine_similarity_results2.xlsx'
plot_cosine_similarity_heatmap(file_path)

