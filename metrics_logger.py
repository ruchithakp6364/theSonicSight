import json, random, os

# Simulate model metrics for demonstration
acc = round(random.uniform(0.80, 0.95), 3)
metrics = {"accuracy": acc, "f1": round(acc - 0.05, 3)}

os.makedirs("metrics", exist_ok=True)
with open("metrics/val_metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("📊 Metrics logged:", metrics)
