# solver_2opt.py
import sys
import math
import os
import itertools

from common import print_tour, read_input, format_tour
import solver_greedy, solver_2opt

def total_distance(tour, cities):
    total_dist = 0
    num_cities = len(tour)
    for i in range(num_cities):
        j = (i + 1) % num_cities
        total_dist += distance(cities[tour[i]], cities[tour[j]])
    return total_dist

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def devide_area(cities):
    """
    4分割して各エリアに属する都市インデックスを返す
    戻り値: [area1, area2, area3, area4]
        各エリアは都市インデックスのリスト
    """
    xs = [c[0] for c in cities]
    ys = [c[1] for c in cities]

    median_x = sorted(xs)[len(xs)//2]
    median_y = sorted(ys)[len(ys)//2]

    area1 = []  # 左下
    area2 = []  # 右下
    area3 = []  # 左上
    area4 = []  # 右上

    for idx, (x,y) in enumerate(cities):
        if x <= median_x and y <= median_y:
            area1.append(idx)
        elif x > median_x and y <= median_y:
            area2.append(idx)
        elif x <= median_x and y > median_y:
            area3.append(idx)
        else:
            area4.append(idx)

    return [area1, area2, area3, area4]

# 各エリアの代表ノード（都市のインデックス）を決める
def select_representative_city(areas, cities, start_node=0):
    representatives = []

    for area in areas:
        if start_node in area:
            representatives.append(start_node)
            continue
        # representatives[-1] から最も近い位置にあるcity を代表ノードとして選ぶ
        if len(representatives) == 0:
            rep_node = area[0]
        else:
            prev_rep = representatives[-1]
            # 直前の代表ノードとの距離を調べる
            min_dist = float('inf')
            rep_node = None
            for idx in area:
                dx = cities[idx][0] - cities[prev_rep][0]
                dy = cities[idx][1] - cities[prev_rep][1]
                dist = (dx**2 + dy**2)**0.5
                if dist < min_dist:
                    min_dist = dist
                    rep_node = idx
        representatives.append(rep_node)

    return representatives


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

    cities =read_input(sys.argv[1])

    # エリアを４分割
    areas = devide_area(cities)

    # # 各エリアの代表ノードを決定
    # representatives = select_representative_city(areas, cities)

    # # 代表ノード間の経路を greedy で決定
    # rep_cities = [cities[idx] for idx in representatives]
    # rep_tour_local = solver_greedy.solve(rep_cities)
    # rep_tour_global = [representatives[i] for i in rep_tour_local]

    # エリアごとに、greedy + 2opt で経路最適化
    subtours = []
    for area in areas:
        area_cities = [cities[idx] for idx in area]
        tour_greedy = solver_greedy.solve(area_cities)
        tour_2opt = solver_2opt.two_opt(tour_greedy, area_cities)
        global_tour = [area[i] for i in tour_2opt]
        subtours.append(global_tour)

    # subtourを連結
    final_tour = None
    best_distance = float('inf')

    # 全ての順列パターンを試す（4! = 24通り）
    for order in itertools.permutations(range(4)):
        candidate = []
        for idx in order:
            candidate += subtours[idx]
        dist = total_distance(candidate, cities)
        if dist < best_distance:
            best_distance = dist
            final_tour = candidate[:]


    print_tour(final_tour)
    print(f"best distance among 24 patterns: {best_distance:.2f}")
    output_file_path = f'output_{challenge_number}.csv'
    with open(output_file_path, 'w') as f:
        f.write(format_tour(final_tour) + '\n')
    print(f"Result has been saved to: {output_file_path}")


