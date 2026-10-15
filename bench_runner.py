import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exécute plusieurs scripts N reines et enregistre les mesures en CSV."
    )
    parser.add_argument(
        "--scripts",
        nargs="+",
        required=True,
        help="Scripts à comparer (par exemple nqueens_boolean.py nqueens_lines.py).",
    )
    parser.add_argument(
        "--n",
        nargs="+",
        type=int,
        required=True,
        help="Tailles d'échiquier à tester (par exemple 4 5 8).",
    )
    parser.add_argument(
        "--output",
        default="benchmark.csv",
        help="Fichier CSV de sortie (par défaut : benchmark.csv).",
    )
    args = parser.parse_args()

    scripts = [Path(script).resolve() for script in args.scripts]
    for script in scripts:
        if not script.is_file():
            parser.error(f"script introuvable : {script}")

    if any(n < 1 for n in args.n):
        parser.error("Toutes les valeurs de --n doivent être des entiers positifs.")

    results = []
    for script in scripts:
        for n in args.n:
            completed = subprocess.run(
                [sys.executable, str(script), "--n", str(n)],
                capture_output=True,
                text=True,
                check=False,
            )
            if completed.returncode != 0:
                raise RuntimeError(
                    f"Échec de {script.name} pour n={n} "
                    f"(code {completed.returncode}).\n{completed.stderr}"
                )
            output_lines = [
                line for line in completed.stdout.splitlines() if line.strip()
            ]
            if not output_lines:
                raise RuntimeError(
                    f"{script.name} n'a produit aucun résultat pour n={n}."
                )
            try:
                result = json.loads(output_lines[-1])
            except json.JSONDecodeError as error:
                raise RuntimeError(
                    f"Sortie JSON invalide de {script.name} pour n={n}.\n"
                    f"Sortie reçue :\n{completed.stdout}"
                ) from error
            results.append(
                {
                    "model": result["model"],
                    "script": script.name,
                    "n": result["n"],
                    "solutions": result["solutions"],
                    "execution_time_seconds": result["elapsed_seconds"],
                    "peak_memory_mb": result["peak_memory_mb"],
                }
            )

    output_path = Path(args.output)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        fieldnames = [
            "model",
            "script",
            "n",
            "solutions",
            "execution_time_seconds",
            "peak_memory_mb",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Résultats enregistrés dans {output_path.resolve()}")


if __name__ == "__main__":
    main()
