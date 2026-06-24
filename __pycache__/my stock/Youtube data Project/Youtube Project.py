import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read dataset
df = pd.read_csv("youtube data.csv")

# Convert columns into numeric
cols = ["views", "likes", "dislikes", "comment"]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove missing values
df = df.dropna()

# Store columns
view = df["views"]
likes = df["likes"]
dislikes = df["dislikes"]
comment = df["comment"]

# ---------- Views Statistics ----------
print("\n<--- Views --->")
print("Mean =", view.mean())
print("Median =", view.median())

variance_views = ((view - view.mean())**2).mean()
std_views = np.sqrt(variance_views)

print("Variance =", variance_views)
print("Standard Deviation =", std_views)

# ---------- Likes Statistics ----------
print("\n<--- Likes --->")
print("Mean =", likes.mean())
print("Median =", likes.median())

variance_likes = ((likes - likes.mean())**2).mean()
std_likes = np.sqrt(variance_likes)

print("Variance =", variance_likes)
print("Standard Deviation =", std_likes)

# ---------- Dislikes Statistics ----------
print("\n<--- Dislikes --->")
print("Mean =", dislikes.mean())
print("Median =", dislikes.median())

variance_dislikes = ((dislikes - dislikes.mean())**2).mean()
std_dislikes = np.sqrt(variance_dislikes)

print("Variance =", variance_dislikes)
print("Standard Deviation =", std_dislikes)

# ---------- Comment Statistics ----------
print("\n<--- Comment --->")
print("Mean =", comment.mean())
print("Median =", comment.median())

variance_comment = ((comment - comment.mean())**2).mean()
std_comment = np.sqrt(variance_comment)

print("Variance =", variance_comment)
print("Standard Deviation =", std_comment)

# ---------- Range ----------
range_data = df[cols].max() - df[cols].min()

print("\n<--- Range of each column --->")
print(range_data)

# ---------- Top 5% ----------
top5_views_limit = view.quantile(0.95)
top5_likes_limit = likes.quantile(0.95)
top5_dislikes_limit = dislikes.quantile(0.95)
top5_comment_limit = comment.quantile(0.95)

print("\n<--- Top 5% Views --->")
print(df[df["views"] >= top5_views_limit][["views"]])

print("\n<--- Top 5% Likes --->")
print(df[df["likes"] >= top5_likes_limit][["likes"]])

print("\n<--- Top 5% Dislikes --->")
print(df[df["dislikes"] >= top5_dislikes_limit][["dislikes"]])

print("\n<--- Top 5% Comments --->")
print(df[df["comment"] >= top5_comment_limit][["comment"]])

# ---------- Histogram ----------
for col in cols:
    plt.figure(figsize=(8,5))
    plt.hist(df[col])
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.title(f"{col} Distribution")
    plt.show()