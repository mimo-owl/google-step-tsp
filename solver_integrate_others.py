# solver_2opt.py
import sys
import math
import os
import time
import random

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

def calculate_distance(city1, city2):
    """
    2都市間のユークリッド距離を計算する
    """
    return math.hypot(city1[0] - city2[0], city1[1] - city2[1])

def calculate_total_distance(route, cities):
    """
    経路全体の総距離を計算する
    """
    total_dist = 0
    num_cities = len(route)
    for i in range(num_cities):
        from_city = cities[route[i]]
        to_city = cities[route[(i + 1) % num_cities]]
        total_dist += calculate_distance(from_city, to_city)
    return total_dist

# 最近傍法によって, 最初の都市から最も近い都市を選ぶ, ということを繰り返すことで, そこそこいい初期解を出す
def nearest_neighbor_heuristic(cities):
    """
    最近傍法で初期解を生成する
    """
    num_cities = len(cities)
    unvisited = set(range(num_cities))
    route = []

    current_city = 0
    unvisited.remove(current_city)
    route.append(current_city)

    while unvisited:
        nearest_city = min(unvisited, key=lambda city: calculate_distance(cities[current_city], cities[city]))
        unvisited.remove(nearest_city)
        route.append(nearest_city)
        current_city = nearest_city

    return route
def local_search_2opt(route, cities):
    """
    2-opt法による局所探索。1秒ごとに進捗を表示する。
    """
    current_route = route[:]
    num_cities = len(current_route)
    improved = True
    last_update_time = time.time()

    while improved:
        improved = False
        for i in range(num_cities - 1):
            for j in range(i + 2, num_cities):
                # 1秒ごとの進捗表示ロジック
                current_time = time.time()
                if current_time - last_update_time > 1.0:
                    progress_msg = f"    -> 2-opt search in progress... (Checking node i={i}/{num_cities})"
                    sys.stdout.write(f"\r{progress_msg:<80}")
                    sys.stdout.flush()
                    last_update_time = current_time
                # 進捗表示ロジックここまで

                j_next = (j + 1) % num_cities
                original_dist = calculate_distance(cities[current_route[i]], cities[current_route[i+1]]) \
                              + calculate_distance(cities[current_route[j]], cities[current_route[j_next]])
                new_dist = calculate_distance(cities[current_route[i]], cities[current_route[j]]) \
                         + calculate_distance(cities[current_route[i+1]], cities[current_route[j_next]])

                if new_dist < original_dist:
                    current_route[i+1:j+1] = reversed(current_route[i+1:j+1])
                    improved = True
                    break
            if improved:
                break

    sys.stdout.write("\r    -> 2-opt search finished.                                          \n")
    sys.stdout.flush()
    return current_route

def double_bridge_kick(route):
    """
    Double Bridge操作による摂動(kick)。
    """
    kicked_route = route[:]
    num_cities = len(kicked_route)
    indices = sorted(random.sample(range(num_cities), 4))
    p1, p2, p3, p4 = indices
    seg1 = kicked_route[:p1]
    seg2 = kicked_route[p1:p2]
    seg3 = kicked_route[p2:p3]
    seg4 = kicked_route[p3:p4]
    seg5 = kicked_route[p4:]
    new_route = seg1 + seg4 + seg3 + seg2 + seg5
    return new_route


def iterated_local_search(initial_tour, cities, max_iterations=100, time_limit=60):
    """
    反復局所探索法(ILS)を実行する
    """
    num_cities = len(cities)
    start_time = time.time()

    # 1. 初期化 (最近傍法を使用)
    print("[Phase 1] Creating initial route with Nearest Neighbor Heuristic...")
    x_0 = initial_tour

    # 2-optで初期解をさらに改善
    print("[Phase 2] Performing initial local search (This may take a long time)...")
    x_best = local_search_2opt(x_0, cities) # ここで1秒ごとの進捗が表示される
    best_dist = calculate_total_distance(x_best, cities)
    print(f"Initial Best Distance: {best_dist:.2f}\n")

    # 2. 反復　ずっとコードを回し続けていて, 終わりが来なくて気が狂いそうだったので現状どこまで計算が進んでいるのかを教えてもらう
    print("[Phase 3] Starting Iterated Local Search main loop...")
    for i in range(max_iterations):
        print(f"--- ILS Iteration {i+1}/{max_iterations} ---")
        if time.time() - start_time > time_limit:
            print(f"Time limit of {time_limit} seconds reached.")
            break

        print("  - Perturbing solution (Double Bridge Kick)...")
        x_kicked = double_bridge_kick(x_best)

        print("  - Running local search on the new route...")
        x_new = local_search_2opt(x_kicked, cities) # ここでも1秒ごとの進捗が表示される
        new_dist = calculate_total_distance(x_new, cities)

        if new_dist < best_dist:
            x_best = x_new
            best_dist = new_dist
            print(f"  -> 🎉 New best solution found! Distance: {best_dist:.2f}\n") # おめでとう🥳
        else:
            print(f"  -> No improvement. Current best: {best_dist:.2f}\n") # 改善されないのなら現状の最高スコアを吐き出す

    print(f"ILS finished. Final Best Distance: {best_dist:.2f}")
    return x_best


if __name__ == '__main__':
    assert len(sys.argv) > 1
    input_file_path  = sys.argv[1]
    input_filename = os.path.basename(input_file_path)
    challenge_number = input_filename.split("_")[1].split(".")[0]

    # greedy で解く
    tour = solver_greedy.solve(read_input(sys.argv[1]))
    print_tour(f"greedy: {tour}")
    # greedy で求めた経路に2-optを適用
    tour_2opt = two_opt(tour, read_input(sys.argv[1]))
    print_tour(f"2opt: {tour_2opt}")

    # ILS で解く（2opt+ダブルキック）
    cities = read_input(sys.argv[1])
    tour_ils = iterated_local_search(
        [int(x) for x in tour_2opt],  # 2-optの結果を与える
        cities,
        max_iterations=1000,
        time_limit=300  # 例: 5分
    )
    print(f"tour_ils: {tour_ils}")

    output_file_path = f'output_{challenge_number}.csv'
    with open(output_file_path, 'w') as f:
        f.write(format_tour(tour_ils) + '\n')

    print(f"Result has been saved to: {output_file_path}")
