#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int map[3][3];

int ft_atoi(char *arg)
{
    int out = 0;
    int minus = 1;
    if (*arg == '-')
    {
        arg++;
        minus = -minus;
    }
    while (*arg)
    {
        out = out * 10 + *arg - '0';
        arg++;
    }
    return out * minus;
}

int get_current_pos(int player)
{
    int t;
    for (int i = 0; i < 3; i++)
    {
        t = map[i][0] + map[i][1] + map[i][2];
        if (t == 3)
            return player;
        if (t == -3)
            return -player;
        t = map[0][i] + map[1][i] + map[2][i];
        if (t == 3)
            return player;
        if (t == -3)
            return -player;
    }
    t = map[0][0] + map[1][1] + map[2][2];
    if (t == 3)
        return player;
    if (t == -3)
        return -player;
    t = map[2][0] + map[1][1] + map[0][2];
    if (t == 3)
        return player;
    if (t == -3)
        return -player;
    return 0;
}

void sorting(int *results, int *indexes, int len)
{
    for (int i = 0; i < len - 1; i++)
    {
        for (int j = 0; j < len - 1 - i; j++)
        {
            if (results[j] > results[j + 1])
            {
                int temp;

                temp = results[j];
                results[j] = results[j + 1];
                results[j + 1] = temp;
                temp = indexes[j];
                indexes[j] = indexes[j + 1];
                indexes[j + 1] = temp;
            }
        }
    }
}

int get_index_forward(int *res, int len)
{
    int i = 0;
    while (i < len)
    {
        if (res[0] != res[i])
            break ;
        i++;
    }
    return rand() % i;
}

int get_index_backward(int *res, int len)
{
    int i = len - 1;
    while (i >= 0)
    {
        if (res[len - 1] != res[i])
            break ;
        i--;
    }
    int mod = len - (i + 1);
    return (i + 1) + rand() % mod;
}

int min_max(int player, int current_move, int res)
{
    int t = get_current_pos(player);
    if (t != 0)
        return t;
    if (current_move >= 9)
        return 0;
    int amount = 0;
    int results[9];
    int indexes[9];
    for (int y = 0; y < 3; y++)
    {
        for (int x = 0; x < 3; x++)
        {
            if (map[y][x] == 0)
            {
                map[y][x] = current_move % 2 == 0 ? 1: -1;
                results[amount] = min_max(player, current_move + 1, 1);
                indexes[amount] = y * 3 + x;
                map[y][x] = 0;
                amount += 1;
            }
        }
    }
    int max_or_min;
    if (current_move % 2 == 1)
        max_or_min = 1;
    else
        max_or_min = 0;
    if (player == -1)
        max_or_min = !max_or_min;
    // if (res == 0)
    // {
    //     for (int i = 0; i < 9; i++)
    //     {
    //         printf("%i %i    ", indexes[i], results[i]);
    //     }
    // }
    sorting(results, indexes, amount);

    if (max_or_min == 1){
        int ind = get_index_forward(results, amount);
        if (res == 0)
        {
            return indexes[ind];
        }
        else{
            return results[ind];
        }
    }
    else{
        int ind = get_index_backward(results, amount);
        if (res == 0)
        {
            return indexes[ind];
        }
        else{
            return results[ind];
        } 
    }
}


int main(int ac, char **av)
{
    srand(time(NULL));
    for (int i = 0; i < 9; i++)
    {
        map[i / 3][i % 3] = ft_atoi(av[i + 1]);
    }

    int amount_of_moves = ft_atoi(av[10]);
    int player = ft_atoi(av[11]);
    int res = min_max(player, amount_of_moves, 0);
    printf("%i", res);
}