
import cpmpy as cp
import time as temps
import matplotlib.pyplot as plt

v_n = [4, 5]
temps_execution_bool = []
temps_execution_lignes = []

SOLVEUR = "ortools"

for n in v_n:
    # Resolution du problème des n reines avec avec des variables booléennes..
    echequier = cp.boolvar(shape=(n, n), name="cases")
    constraintes = []

    # ici c'est les contraintes liées aux ligne et aux colonnes. Deux reines ne peuvent pas restent sur la mm ligne ni colonne
    for i in range(n):
        constraintes.append(cp.sum(echequier[i, :]) ==1)
        constraintes.append(cp.sum(echequier[:, i]) ==1)

    for d_m in range(2*n - 1):
        cases = [(li, d_m-li) for li in range(n) if 0 <= d_m-li < n ]
        if len(cases) > 1 :
            constraintes.append(cp.sum([echequier[li, col] for li, col in cases]) <=1)

    for dia_desc in range(1-n, n):
        cases = [(li, dia_desc + li) for li in range(n) if 0 <= dia_desc + li < n ]
        if len(cases) > 1 :
            constraintes.append(cp.sum([echequier[li, col] for li, col in cases]) <= 1)  

    m = cp.Model(constraintes) 

    start_time = temps.perf_counter()
    solution_trouvee = m.solveAll(solver=SOLVEUR)
    temps_execution_bool.append(temps.perf_counter() - start_time)


    # resolution du probleme avec des variables lignes
    q = cp.intvar(0, n-1, shape=n, name = "q")

   
    m = cp.Model(
        cp.AllDifferent(q),
        cp.AllDifferent([q[i] + i for i in range(n)]),
        cp.AllDifferent([q[i] - i for i in range(n)])
    )
    
    start_time_ligne = temps.perf_counter()
    sol_find = m.solveAll(solver = SOLVEUR)
    temps_execution_lignes.append(temps.perf_counter() - start_time_ligne)


# Tracer les deux courbes
plt.plot(v_n, temps_execution_bool, marker="o", label="Variables booléennes ")
plt.plot(v_n, temps_execution_lignes, marker="o", label="Variables lignes")

plt.xlabel("Taille de l'échiquier n")
plt.ylabel("Temps de résolution (secondes)")
plt.title("Comparaison des modèles pour le problème des n reines")
plt.xticks(v_n)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()