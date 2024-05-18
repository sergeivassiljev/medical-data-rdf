import pandas as pd
import numpy as np

def calculate_similarity_statistics(file_path):
    # Andmete laadimine Excel-failist
    data = pd.read_excel(file_path)

    # Andmete tasandamine üheks massiiviks
    values = data.values.flatten()

    # Statistikute arvutamine
    average_similarity = np.mean(values)
    std_dev_similarity = np.std(values)
    min_similarity = np.min(values)
    median_similarity = np.median(values)
    max_similarity = np.max(values)

    # Tulemuste väljastamine
    print(f"Keskmine sarnasuse väärtus: {average_similarity:.3f}")
    print(f"Standardhälve: {std_dev_similarity:.3f}")
    print(f"Minimaalne sarnasuse väärtus: {min_similarity:.3f}")
    print(f"Mediaan sarnasuse väärtus: {median_similarity:.3f}")
    print(f"Maksimaalne sarnasuse väärtus: {max_similarity:.3f}")

# Määra Excel-faili asukoht
file_path = 'cosine_similarity_results2.xlsx'

# Funktsiooni kutsumine etteantud failiteega
calculate_similarity_statistics(file_path)
