# solver_2opt.py
import sys
import math
import os
import matplotlib.pyplot as plt

from common import print_tour, read_input, format_tour
import solver_greedy

def total_distance(tour, cities):
    total_dist = 0
    num_cities = len(tour)
    for i in range(num_cities):
        j = (i + 1) % num_cities
        total_dist += distance(cities[tour[i]], cities[tour[j]])
    return total_dist

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def two_opt_swap(route, i, k):
    new_route  = route[:i] + route[i:k+1][::-1] + route[k+1:] # iより前と、kより後は変更なし。i~kの部分だけ、順番を反転させる
    return new_route

# def two_opt(tour, cities):
#     num_cities = len(cities)
#     best_route = tour[:]
#     can_improve = True

#     # 改善の余地がある限り、次の処理を実行
#     while can_improve:
#         can_improve = False
#         for i in range(1, num_cities - 1):
#             for j in range(i + 1, num_cities):
#                 dist_ij = distance(cities[best_route[i]], cities[best_route[j]])
#                 print(f"Distance between city {best_route[i]} and city {best_route[j]}: {dist_ij:.4f}")
#                 # 現時点でのベストルートについて、ノードiとjの間のルートを反転させる
#                 new_route = two_opt_swap(best_route, i, j)
#                 # swap前後で総距離を比較し、より短くなっていたらそれをベストルートとして更新
#                 if total_distance(new_route, cities) < total_distance(best_route, cities):
#                     best_route = new_route[:]
#                     can_improve = True
#         tour = best_route[:]
#     return best_route

def two_opt(tour, cities, threshold=100):
    num_cities = len(cities)
    best_route = tour[:]
    can_improve = True

    # improvements_euclid = []  # 直線距離横軸
    improvements_path = []    # ルート距離横軸

    while can_improve:
        can_improve = False
        for i in range(1, num_cities - 1):
            for j in range(i + 1, num_cities):

                # 現時点でのベストルートについて、ノードiとjの間のルートを反転させる
                a = best_route[i - 1]
                b = best_route[i]
                c = best_route[j]
                d = best_route[(j + 1) % num_cities]

                before = distance(cities[a], cities[b]) + distance(cities[c], cities[d])
                after  = distance(cities[a], cities[c]) + distance(cities[b], cities[d])

                # 反転した結果が改善されていればベストルートとして更新
                if after < before:
                    improvement_ratio = after / before * 100
                    if threshold != 100:
                        if improvement_ratio > threshold:
                            continue
                    print(f"Improvement found: {before:.4f} -> {after:.4f} (cities {a}, {b}, {c}, {d}), shorted by: {improvement_ratio:.2f}%")
                    new_route = two_opt_swap(best_route, i, j)
                    best_route = new_route[:]
                    can_improve = True

                    # improvement_ratio = after / before * 100
                    path_width = before  # i, j 間の元のルートの長さ

                    if len(improvements_path) < 1000:
                        improvements_path.append( (path_width, improvement_ratio) )

        tour = best_route[:]

    return best_route, improvements_path


if __name__ == '__main__':
    assert len(sys.argv) > 1
    input_file_path  = sys.argv[1]
    input_filename = os.path.basename(input_file_path)
    challenge_number = input_filename.split("_")[1].split(".")[0]

    # greedy で解く
    greedy_tour = solver_greedy.solve(read_input(sys.argv[1]))
    print_tour(greedy_tour)

    # greedy で求めた経路に2-optを適用

    threshold = 10
    count = 0
    for count in range(10):
        two_opt_tour, improvements_path = two_opt(greedy_tour, read_input(sys.argv[1]), threshold)
        print(f"Iteration {count + 1}: Tour length = {total_distance(two_opt_tour, read_input(sys.argv[1])):.2f}")
        threshold += 10


    # optimized_tour, improvements_path = two_opt(tour, read_input(sys.argv[1]))
    # print_tour(optimized_tour)

    output_file_path = f'output_{challenge_number}.csv'
    # output_file_path = f'output_8.csv'
    with open(output_file_path, 'w') as f:
        f.write(format_tour(two_opt_tour) + '\n')

    print(f"Result has been saved to: {output_file_path}")

    if improvements_path:
        x2 = [w for (w, r) in improvements_path]
        y2 = [r for (w, r) in improvements_path]
        print(f"y2: {y2}")
        plt.figure()
        plt.scatter(x2, y2, alpha=0.7)
        plt.xlabel("Route distance between i and j (before swap)")
        plt.ylabel("Improved distance (% of original route distance)")
        plt.title("First 500 improvements - Route distance as x-axis")
        plt.grid()
        plt.show()
