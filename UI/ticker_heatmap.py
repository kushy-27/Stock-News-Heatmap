import json
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

with open("Data/processed/ticker_sentiment_heatmap.json") as f:
    data = json.load(f)

sectors = list(data.keys())
sentiments = sorted(np.array([data[s]["avg_sentiment"] for s in sectors]).reshape(-1, 1))

fig, ax = plt.subplots(figsize=(6, len(sectors) * 0.4))

im = ax.imshow(
    sentiments,
    cmap="RdYlGn",
    vmin=-1,
    vmax=1,
    aspect="auto"
)

ax.set_xticks([0])
ax.set_xticklabels(["Sentiment"])
ax.set_yticks(range(len(sectors)))
ax.set_yticklabels(sectors)

cbar = plt.colorbar(im, ax=ax)
cbar.set_label("Average Sentiment")

for i, s in enumerate(sentiments[:, 0]):
    ax.text(
        0, i,
        f"{s:.2f}",
        ha="center", va="center",
        color="black"
    )

plt.title("Ticker Sentiment Heatmap")
plt.tight_layout()
plt.savefig("UI/ticker_heatmap.png", dpi=150)

