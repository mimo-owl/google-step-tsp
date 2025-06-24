# solver_2opt.py
import sys
import math
import os

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

def two_opt(tour, cities):
    num_cities = len(cities)
    best_route = tour[:]
    can_improve = True

    # 改善の余地がある限り、次の処理を実行
    while can_improve:
        can_improve = False
        for i in range(1, num_cities - 1):
            for j in range(i + 1, num_cities):
                # 現時点でのベストルートについて、ノードiとjの間のルートを反転させる
                new_route = two_opt_swap(best_route, i, j)
                # swap前後で総距離を比較し、より短くなっていたらそれをベストルートとして更新
                if total_distance(new_route, cities) < total_distance(best_route, cities):
                    best_route = new_route[:]
                    can_improve = True
        tour = best_route[:]
    return best_route


if __name__ == '__main__':
    assert len(sys.argv) > 1
    input_file_path  = sys.argv[1]
    input_filename = os.path.basename(input_file_path)
    challenge_number = input_filename.split("_")[1].split(".")[0]

    # greedy で解く
    tour = solver_greedy.solve(read_input(sys.argv[1]))
    print_tour(tour)
    # greedy で求めた経路に2-optを適用
    optimized_tour = two_opt(tour, read_input(sys.argv[1]))
    print_tour(optimized_tour)

    output_file_path = f'output_{challenge_number}.csv'
    with open(output_file_path, 'w') as f:
        f.write(format_tour(optimized_tour) + '\n')

    print(f"Result has been saved to: {output_file_path}")
