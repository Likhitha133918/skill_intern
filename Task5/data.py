import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("Task5/Iris dataset.csv")   


print("First 5 Rows:")
print(df.head())


print("\nDataset Info:")
print(df.info())


print("\nSummary Statistics:")
print(df.describe())


print("\nMean Values:")
print(df.mean())


df.mean().plot(kind="bar")
plt.title("Average Feature Values")
plt.ylabel("Mean Value")
plt.xticks(rotation=45)
plt.show()


plt.scatter(df["sepal length (cm)"], df["petal length (cm)"])
plt.title("Sepal Length vs Petal Length")
plt.xlabel("Sepal Length (cm)")
plt.ylabel("Petal Length (cm)")
plt.show()


df.hist(figsize=(8,6))
plt.tight_layout()
plt.show()
