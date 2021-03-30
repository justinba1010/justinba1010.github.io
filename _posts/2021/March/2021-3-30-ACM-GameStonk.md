---
layout: post
title: ACM@USC Codeathon - GameStonk - C++
date: March 30, 2021
time: 0:00 UTC-4
---

The greatest thing I learned this year, was imagine every dynamic programming question as some subproblem of knapsack. Once you think of it as knapsack, it feels magnitudes easier to solve if you know the $$O(nW)$$ dynamic solution and $$W$$ is sufficiently a small enough factor. K-dimensional dynamic programming has become a lot easier, but I still struggle from time to time.

I learned through my years going to ICPC that my weakness in algorithm competitions is dynamic programming. Graph algorithms almost feel trivial, divide and conquer can be difficult but do not come up often. I decided to spend the last year or so really trying to get a deep understanding and ability in dynamic programming. Today I feel very comfortable. I found a neat problem, [Min Jumps](https://www.geeksforgeeks.org/minimum-number-of-jumps-to-reach-end-of-a-given-array/), and tweaked it to be a little more difficult, and requiring an understanding of the algorithm otherwise trying to tweak the geeks for geeks solution will be futile.

This last month has also been a great opportunity to really pick up on my C++ and algorithms skills. I went ahead and brushed up quite a bit over the last few days, and have decided to try and finish all of AlgoExpert in just C++, [AlgoExpert Solutions](https://github.com/justinba1010/AlgoExpert-Practice).

It begins with an array of positive integers designating how many jumps you can go forward to reach the end from each position. The target is to solve the path of jumps that give the fewest jumps. This is almost knapsack, and thinking it this way makes life a lot easier. Below is the the problem statement and solution.


# 2021 GameStonk

It has been shown with a high correlation that turning memes into integers, and ordering them chronologically gives you data that you can predict the value of GameStop stock with 70% confidence. Every meme gives a value indicating how many memes forward you can jump. You must move chronologically. Once you have the shortest path through all of the memes, you can use this information to put memes into google reverse image search. If there is more green than red, you invest now. If there is more red than green, you hold. If there is an equal amount of green and red, you have hit the lotto, you should sell your home and buy call options.

## Description

Given all the values of memes in chronological order. Then the corresponding meme names, find the path of memes `A->B->C->D` such that you take the shortest path to Gamestop riches.

## Input
 
You will receive an integer `n` that will correspond to the number of memes you will receive on the first line. You will then receive the meme's value `v_i` space delimitted on the same line. Then you will receive the meme names. Meme names will be in the regex `[A-z]*` and have length less than or equal to 15 ascii characters.

```
n
v_1 v_2 v_3 ... v_n
m_1 m_2 m_3 ... m_n
```

## Constraints

$$1 \leq n \leq 10000$$

$$1 \leq v_i \leq 100$$

$$m_i \in [A-z]*$$

## Output

```
p_1 p_2 ... p_k
```

Where you can legally jump from $$p_1$$->$$p_2$$->...$$p_k$$, where $$p_k = m_n$$.


### Disclaimer

This is not a financial strategy, advice, or anything more than a problem statement for the USC Codeathon.

## Solution


```c++
/* Copyright 2021
** Justin Baum
** MIT License
*/

#include <vector>
#include <iostream>
#include <string>
#include <climits>
using namespace std;

vector<string> min_number_of_jumps(vector<int> &array, vector<string> &names) {
    int size = array.size();
    vector<string> solution;
    int steps = array[0];
    int max_reach = array[0];
    int max_index = 0;
    solution.push_back(names[0]);
    for (int i = 1; i < array.size() - 1; i++) {
        int new_reach = i + array[i];
        --steps;
        if (new_reach > max_reach) {
            max_index = i;
            max_reach = new_reach;
        }
        if (steps == 0) {
            solution.push_back(names[max_index]);
            steps = max_reach - i;
        }
    }
    return solution;
}

int main(void) {
    int n;
    cin >> n;
    vector<int> array;
    vector<string> names;
    for(int _ = 0; _ < n; ++_) {
        int x;
        cin >> x;
        array.push_back(x);
    }
    for(int _ = 0; _ < n; ++_) {
        string x;
        cin >> x;
        names.push_back(x);
    }
    auto x = min_number_of_jumps(array, names);
    //cout << x.first << endl;
    for(string name : x) {
        cout << name << " ";
    }
    cout << names[n - 1];
    cout << endl;
    return 0;
}
```
