import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


def main() -> None:
    parser = argparse.ArgumentParser(description="Trace les temps et la mémoire à partir d'un fichier de benchmark CSV.")
    parser.add_argument( "--input", default="benchmark.csv", help="Fichier CSV produit par bench_runner.py.",)
    parser.add_argument(
        "--output",
        default="comparison.png",
        help="Image de sortie (par défaut : comparison.png).",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Afficher également le graphique dans une fenêtre.",
    )
    args = parser.parse_args()

    measurements: dict[str, list[dict[str, float]]] = defaultdict(list)
    with Path(args.input).open(newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            measurements[row["model"]].append(
                {
                    "n": float(row["n"]),
                    "time": float(row["execution_time_seconds"]),
                    "memory": float(row["peak_memory_mb"]),
                }
            )

    if not measurements:
        parser.error(f"aucune mesure trouvée dans {args.input}")

    figure, (time_axis, memory_axis) = plt.subplots(1, 2, figsize=(12, 5))
    for model_name, rows in sorted(measurements.items()):
        rows.sort(key=lambda row: row["n"])
        sizes = [row["n"] for row in rows]
        time_axis.plot(
            sizes,
            [row["time"] for row in rows],
            marker="o",
            label=model_name,
        )
        memory_axis.plot(
            sizes,
            [row["memory"] for row in rows],
            marker="o",
            label=model_name,
        )

    time_axis.set(
        xlabel="Taille de l'échiquier n",
        ylabel="Temps de résolution (secondes)",
        title="Temps de résolution",
    )
    memory_axis.set(
        xlabel="Taille de l'échiquier n",
        ylabel="Mémoire maximale du processus (MiB)",
        title="Consommation mémoire",
    )
    for axis in (time_axis, memory_axis):
        axis.grid(True)
        axis.legend()

    figure.suptitle("Comparaison des modèles pour le problème des N reines")
    figure.tight_layout()
    output_path = Path(args.output)
    figure.savefig(output_path)
    print(f"Graphique enregistré dans {output_path.resolve()}")
    if args.show:
        plt.show()


if __name__ == "__main__":
    main()
