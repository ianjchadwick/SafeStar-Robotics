#include "safeStar.hpp"
#include <iostream>
#include <queue>
#include <algorithm>
#include <cmath>

using Grid = std::vector<std::vector<int>>; // 0: obstacle, >0: node id

// Helper: Manhattan distance
int manhattan(int x1, int y1, int x2, int y2) {
    return std::abs(x1-x2) + std::abs(y1-y2);
}

// Build grid, add nodes, label open cells with node ids
void grid_construct(Grid& grid, std::vector<Node>& nodes, int size,
                    const std::vector<std::tuple<int, int, int, int>>& obstacles) {
    grid.assign(size, std::vector<int>(size, 1));
    // Place obstacles (tuple: x, y, xlen, ylen)
    for (auto& obs : obstacles) {
        int x0, y0, xlen, ylen;
        std::tie(x0, y0, xlen, ylen) = obs;
        for (int x = x0; x < x0 + xlen; ++x)
            for (int y = y0; y < y0 + ylen; ++y)
                grid[x][y] = 0;
    }
    // Assign node ids and build node list
    int nodeNum = 1;
    for (int x=0; x<size; ++x) for (int y=0; y<size; ++y) {
        if (grid[x][y]==1) {
            grid[x][y] = nodeNum;
            nodes.push_back(Node{nodeNum, x, y});
            nodeNum++;
        }
    }
}

// Assign neighbor node ids to each node (N, E, S, W)
void node_get_neighbors(const Grid& grid, std::vector<Node>& nodes) {
    int size = grid.size();
    for (auto& node : nodes) {
        int x = node.x, y = node.y;
        // N
        if (x > 0 && grid[x-1][y] != 0)
            node.neighbors.push_back(grid[x-1][y]);
        // E
        if (y < size-1 && grid[x][y+1] != 0)
            node.neighbors.push_back(grid[x][y+1]);
        // S
        if (x < size-1 && grid[x+1][y] != 0)
            node.neighbors.push_back(grid[x+1][y]);
        // W
        if (y > 0 && grid[x][y-1] != 0)
            node.neighbors.push_back(grid[x][y-1]);
    }
}

// Assign d_exit for each node
void node_set_d_exit(std::vector<Node>& nodes, const std::vector<std::pair<int,int>>& exits) {
    for (auto& node : nodes) {
        node.d_exit = std::numeric_limits<int>::max();
        for (auto& ex : exits) {
            int d = manhattan(node.x, node.y, ex.first, ex.second);
            if (d < node.d_exit) node.d_exit = d;
        }
    }
}

// BFS wavefront from hazard sources to assign safety_score
void hazard_wavefront(std::vector<Node>& nodes, const std::vector<std::pair<int,int>>& hazard_sources) {
    std::queue<int> Q;
    std::vector<int> closed(nodes.size(), 0);

    // Find node_ids of hazard sources
    for (auto& hsrc : hazard_sources) {
        for (auto& node : nodes) {
            if (node.x == hsrc.first && node.y == hsrc.second) {
                node.safety_score = 0;
                Q.push(node.id);
                break;
            }
        }
    }

    while (!Q.empty()) {
        int n_id = Q.front(); Q.pop();
        Node& current = nodes[n_id-1];
        int next_dist = current.safety_score + 1;
        for (int nb_id : current.neighbors) {
            Node& nb = nodes[nb_id-1];
            if (nb.safety_score > next_dist) {
                nb.safety_score = next_dist;
                Q.push(nb.id);
            }
        }
    }
}

double next_cost(const Node& curr, const Node& next) {
    if (curr.safety_score < next.safety_score && curr.d_exit > next.d_exit)
        return 0.0;
    if (curr.safety_score <= next.safety_score && curr.d_exit <= next.d_exit)
        return 1.0;
    if (curr.safety_score > next.safety_score && curr.d_exit >= next.d_exit)
        return 1.5;
    if (curr.safety_score > next.safety_score && curr.d_exit < next.d_exit)
        return 2.0;
    return 2.0;
}


// Hazard-aware A* pathfinding
std::vector<int> safeStar_path(std::vector<Node>& nodes, const Grid& grid,
                                     std::pair<int,int> start, const std::vector<std::pair<int,int>>& exits) {
    using P = std::pair<double, int>;
    std::priority_queue<P, std::vector<P>, std::greater<P>> open;
    std::vector<double> g(nodes.size(), INFINITY);
    std::vector<int> closed(nodes.size(), 0);
    int start_id = -1, exit_id = -1;

    for (auto& node : nodes) {
        if (node.x == start.first && node.y == start.second) {
            start_id = node.id;
            g[start_id-1] = 0;
            open.emplace(0, start_id);
            break;
        }
    }
    if (start_id == -1) return {};

    while (!open.empty()) {
        auto [curr_cost, curr_id] = open.top(); open.pop();
        if (closed[curr_id-1]) continue;
        closed[curr_id-1] = 1;
        Node& curr = nodes[curr_id-1];

        // Stop at any exit node
        if (curr.d_exit == 0) {
            exit_id = curr_id;
            break;
        }

        for (int nb_id : curr.neighbors) {
            Node& nb = nodes[nb_id-1];
            double new_cost = curr.cost + next_cost(curr, nb);
            if (!closed[nb_id-1] || new_cost < nb.cost) {
                nb.cost = new_cost;
                nb.backpointer = curr_id;
                // Strongly bias toward higher safety_score, but always reach the exit
                double priority = nb.d_exit - nb.safety_score;
                open.emplace(priority, nb_id);
            }
        }
    }

    // Reconstruct path
    std::vector<int> path;
    if (exit_id == -1) return path;
    int path_id = exit_id;
    while (path_id != start_id) {
        path.push_back(path_id);
        path_id = nodes[path_id-1].backpointer;
    }
    path.push_back(start_id);
    std::reverse(path.begin(), path.end());
    return path;
}

// Classic A* for baseline
std::vector<int> classic_a_star(std::vector<Node>& nodes, const Grid& grid,
                                std::pair<int,int> start, const std::vector<std::pair<int,int>>& exits) {
    using P = std::pair<double, int>;
    std::priority_queue<P, std::vector<P>, std::greater<P>> open;
    std::vector<double> g(nodes.size(), INFINITY);
    std::vector<int> closed(nodes.size(), 0);
    int start_id = -1, exit_id = -1;

    for (auto& node : nodes) {
        if (node.x == start.first && node.y == start.second) {
            start_id = node.id;
            g[start_id-1] = 0;
            open.emplace(0, start_id);
            break;
        }
    }
    if (start_id == -1) return {};

    while (!open.empty()) {
        auto [curr_cost, curr_id] = open.top(); open.pop();
        if (closed[curr_id-1]) continue;
        closed[curr_id-1] = 1;
        Node& curr = nodes[curr_id-1];

        if (curr.d_exit == 0) {
            exit_id = curr_id;
            break;
        }

        for (int nb_id : curr.neighbors) {
            Node& nb = nodes[nb_id-1];
            double new_cost = curr.cost + 1.0;
            if (!closed[nb_id-1] || new_cost < nb.cost) {
                nb.cost = new_cost;
                nb.backpointer = curr_id;
                double priority = new_cost + nb.d_exit;
                open.emplace(priority, nb_id);
            }
        }
    }

    std::vector<int> path;
    if (exit_id == -1) return path;
    int path_id = exit_id;
    while (path_id != start_id) {
        path.push_back(path_id);
        path_id = nodes[path_id-1].backpointer;
    }
    path.push_back(start_id);
    std::reverse(path.begin(), path.end());
    return path;
}

// Print grid with path overlays
void print_grid(const Grid& grid, const std::vector<Node>& nodes,
                const std::vector<int>& safeStar_path, const std::vector<int>& classic_path,
                std::pair<int,int> start, const std::vector<std::pair<int,int>>& exits,
                const std::vector<std::pair<int,int>>& hazard_sources) {
    int size = grid.size();
    // Copy grid to overlay paths
    std::vector<std::vector<char>> vis(size, std::vector<char>(size, '.'));

    // Obstacles
    for (int x=0; x<size; ++x) for (int y=0; y<size; ++y)
        if (grid[x][y]==0) vis[x][y] = '#';
                    
    // Safe* path: 2
    for (int id : safeStar_path) {
        auto& n = nodes[id-1];
        vis[n.x][n.y] = 'S';
    }
    // Classic path: 3 (will overwrite S if overlapping)
    for (int id : classic_path) {
    auto& n = nodes[id-1];
    if (vis[n.x][n.y] == 'S')
        vis[n.x][n.y] = '@'; // Overlap
    else
        vis[n.x][n.y] = 'A';
    }

    // Hazard sources
    for (auto& hs : hazard_sources)
        vis[hs.first][hs.second] = 'H';
    // Start
    vis[start.first][start.second] = 'X';
    // Exits
    for (auto& ex : exits)
        vis[ex.first][ex.second] = 'E';

    // Print
    for (int x=0; x<size; ++x) {
        for (int y=0; y<size; ++y)
            std::cout << vis[x][y] << " ";
        std::cout << "\n";
    }
}
