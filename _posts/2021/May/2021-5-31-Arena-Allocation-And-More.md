---
layout: post
title: Arena Allocation, Strings, and other Pandemic Low Level Ideas
date: May 31, 2021
time: 0:00 UTC-4
---

Some time during the pandemic, I wrote some small snippets of C code for low level processes that I thought were interesting.


To skip to the Pacman experiment: [Pacman](#Pacman).

## Strings

Strings are interesting in C, because they almost necessarily need dynamic memory. That and we take them for granted. I wrote a tiny little struct that manages strings, as well as a `readinput` function that returns a raw pointer.

```c
/*
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define CHUNK 8

struct stringy {
  char *string;
  size_t size;
};

void freestringy(struct stringy s) {
  if (s.string != NULL) {
    free(s.string);
  }
}

struct stringy read_string() {
  char *input = NULL;
  char tempbuf[CHUNK];
  size_t inputlen = 0;
  size_t templen = 0;
  do {
    fgets(tempbuf, CHUNK, stdin);
    templen = strlen(tempbuf);
    input = realloc(input, inputlen + templen + 1);
    strcpy(input + inputlen, tempbuf);
    inputlen += templen;
  } while (templen == CHUNK - 1 && tempbuf[CHUNK-2] != '\n');
  struct stringy s;
  s.string = input;
  s.size = inputlen;
  return s;
}

char *readinput(size_t *size) {
  char *input = NULL;
  char tempbuf[CHUNK];
  size_t inputlen = 0;
  size_t templen = 0;
  do {
    fgets(tempbuf, CHUNK, stdin);
    templen = strlen(tempbuf);
    input = realloc(input, inputlen + templen + 1);
    strcpy(input + inputlen, tempbuf);
    inputlen += templen;
  } while (templen == CHUNK - 1 && tempbuf[CHUNK-2] != '\n');
  *size = inputlen;
  return input;
}

int main(void) {
  char *result;
  size_t *size;
  struct stringy s;
  size = malloc(sizeof(size_t));
  result = readinput(size);
  printf("Result: %s", result);
  printf("Length: %d\n", *size);
  free(result);
  result = readinput(size);
  printf("Result: %s", result);
  printf("Length: %d\n", *size);
  free(result);
  free(size);
  s = read_string();
  printf("Result: %s", s.string);
  printf("Length: %d\n", s.size);
  freestringy(s);
  return 0;
}
```

## Function Pointers

I take currying and first class function for granted greatly. I wanted to see how unwieldy they are in C. Without going too deep, there are tons of StackOverflow posts that explain this more deeply.

```c
#include <stdlib.h>
#include <stdio.h>

void hello_world(void) {
  printf("Hello World \n");
}

void p(void (f)(void)) {
  f();
}

void g(void (*f)(void)) {
  (*f)();
}

int main(void) {
  p(hello_world);
  g(&hello_world);
  return 0;
}
```

## Arena Allocation

I liked the idea of memory management. It's one thing to be able to use `malloc` and another to try rewriting it. I chose to try a very greedy solution and see if it had any speed up benefits from pinging the kernel.

```c
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#define ARENA 4 << 20

char *arena;
u_int64_t current;
void hexDump (const char * desc, const void * addr, const int len) {
    int i;
    unsigned char buff[17];
    const unsigned char * pc = (const unsigned char *)addr;

    // Output description if given.

    if (desc != NULL)
        printf ("%s:\n", desc);

    // Length checks.

    if (len == 0) {
        printf("  ZERO LENGTH\n");
        return;
    }
    else if (len < 0) {
        printf("  NEGATIVE LENGTH: %d\n", len);
        return;
    }

    // Process every byte in the data.

    for (i = 0; i < len; i++) {
        // Multiple of 16 means new line (with line offset).

        if ((i % 16) == 0) {
            // Don't print ASCII buffer for the "zeroth" line.

            if (i != 0)
                printf ("  %s\n", buff);

            // Output the offset.

            printf ("  %04x ", i);
        }

        // Now the hex code for the specific character.
        printf (" %02x", pc[i]);

        // And buffer a printable ASCII character for later.

        if ((pc[i] < 0x20) || (pc[i] > 0x7e)) // isprint() may be better.
            buff[i % 16] = '.';
        else
            buff[i % 16] = pc[i];
        buff[(i % 16) + 1] = '\0';
    }

    // Pad out last line if not exactly 16 characters.

    while ((i % 16) != 0) {
        printf ("   ");
        i++;
    }

    // And print the final ASCII buffer.

    printf ("  %s\n", buff);
}

void *arena_malloc(u_int64_t size) {
  current += size;
  if (current > ARENA) {
    printf("Heap overflow");
    exit(0);
  }
  return arena + current - size;
}

void *arena_calloc(u_int64_t size, u_int64_t num) {
  return arena_malloc(size * num);
}

int compare(const void *a, const void *b) {
  int x = *(const int*)a;
  int y = *(const int*)b;
  return (x > y) - (x < y);
}

struct vector {
  int64_t size;
  int64_t *vector;
};

#define TV 120

int main(void) {
  srand(time(0));
  arena = malloc(ARENA);
  current = 0;
  int64_t total_vectors;
  scanf("%ld", &total_vectors);
  printf("%ld", total_vectors);
  struct vector* vectors = (struct vector*)arena_calloc(sizeof(struct vector), total_vectors);
  for (int64_t i = 0; i < total_vectors; ++i) {
    int size = total_vectors; // rand() % TV + (TV >> 1);
    vectors[i].size = size;
    vectors[i].vector = (int64_t*)arena_calloc(sizeof(int64_t), size);
    for (int64_t j = 0; j < size; ++j) {
      vectors[i].vector[j] = (int64_t)rand();
      vectors[i].vector[j] <<= 32;
      vectors[i].vector[j] |= (int64_t)rand();
    }
  }

  for (int64_t i = 0; i < total_vectors; ++i) {
    //printf("Enter character to go to next\n");
    //printf("Vector: %ld\t Size: %ld\n", i, vectors[i].size);
    for (int64_t j = 0; j < vectors[i].size; ++j) {
     //printf("%ld, ", vectors[i].vector[j]);
    }
    //printf("\n");
  }
  //hexDump("", arena, current);
  free(arena);
  printf("%ld\n", current);
}
```

<div id="Pacman"></div>
## Pacman Experiment

Lastly I wrote a small little pacman game without the ghosts due to time constraints, using low level libraries and Unix API calls. It ended up being very difficult to keep track of everything, and this was when I realized that modern programmers are saved by very powerful languages. I would assume that I would be unable to write a pacman game in any assembler.

It is incredible what people were able to accomplish before modern compilers, languages, and toolchains. Below is just some of the pacman code that I found interesting.

### Depth First Search

This was meant for `Blinky`? The ghost that does not change direction until hitting an obstacle, but chases pacman. DFS is the basis of all the ghosts, I believe one tails pacman by navigating to 4 squares behind where Pacman is, one tries to ambush by navigating to 4 squares ahead, and one last one runs away(I was going to implement this by just picking the opposite furthest corner. Unfortunately I never finished, but just DFS was embarrasingly long.

```c
#ifndef __pacman_ai__
#define __pacman_ai__

#include <stdlib.h>
#include <map.c>
#define STACK_SIZE 256

typedef enum {R, L, U, D} direction;

direction stack[STACK_SIZE];
int stack_index = 0;
bool visited[ROWS][COLS];

void reset(void) {
  stack_index = 0;
  for (int i = 0; i < ROWS; ++i) {
    for (int j = 0; j < COLS; ++j) {
      visited[i][j] == false;
    }
  }
}

direction blinky(Positional *blinky, Positional *pacman) {
  reset();
  return dfs(blinky->graphx, blinky->graphy, pacman->graphx, pacman->graphy, ghost_allowed, g_a);
}

direction dfs(int x, int y, int x_t, int y_t, tile *t, int s) {
  if (x_t == x && y_t == y) {
    return stack[0];
  }
  // Right
  if (!visited[y][x+1] && legal(x + 1, y, t, s)) {
    visited[y][x+1] = true;
    stack[stack_index++] = R;
    return dfs(x+1, y, x_t, y_t);
  }
  stack_index--;
  // Left
  if (!visited[y][x-1] && legal(x - 1, y, t, s)) {
    visited[y][x-1] = true;
    stack[stack_index++] = L;
    return dfs(x-1, y, x_t, y_t);
  }
  stack_index--;
  // Down
  if (!visited[y + 1][x] && legal(x, y + 1, t, s)) {
    visited[y+1][x] = true;
    stack[stack_index++] = D;
    return dfs(x, y+1, x_t, y_t);
  }
  stack_index--;
  // Up
  if (!visited[y][x] && legal(x, y - 1, t, s)) {
    visited[y - 1][x] = true;
    stack[stack_index++] = R;
  }
  stack_index--;
}
#endif
```

Lastly just the positioning of the "sprites", which were not rendered as images, as I decided drawing a few circles and squares to make up each ghost and pacman would be far easier:

```c
/*
This gives Pacman's location
void player(void) {
  struct timespec xt;
  timespec_get(&xt, TIME_UTC);
  float diff = difftime(xt.tv_sec, currtime.tv_sec);
  diff += 1e-9*(xt.tv_nsec - currtime.tv_nsec);

  float newx, newy;
  timespec_get(&currtime, TIME_UTC);
  pacman.x += diff * pacman.vx;
  pacman.y += diff * pacman.vy;
  float x = round(pacman.x/W_W)*W_W;
  float y = round(pacman.y/W_V)*W_V;

  int x_ = (int) x;
  int y_ = (int) y;

  if (x_ >= 0 && x_ < WIDTH && y_ >= 0 && y_ < HEIGHT) {
    int i = x / W_W;
    int j = y / W_V;
    switch (maze[i][j]) {
      case W:
        pacman.x = lastvalidx;
        pacman.y = lastvalidy;
        pacman.vx = 0.;
        pacman.vy = 0.;
        break;
      case o:
        lastvalidx = pacman.x;
        lastvalidy = pacman.y;
        maze[i][j] = 'e';
        break;
      case O:
        lastvalidx = pacman.x;
        lastvalidy = pacman.y;
        maze[i][j] = 'E';
        break;
      case P:
        pacman.x = pacman.x > 140 ? 10: 260;
        break;
      default:
        lastvalidx = pacman.x;
        lastvalidy = pacman.y;

    }
  } else {
    pacman.x = lastvalidx;
    pacman.y = lastvalidy;
    pacman.vx = 0.;
    pacman.vy = 0.;
  }
  x = round(pacman.x/W_W)*W_W;
  y = round(pacman.y/W_V)*W_V;
  x_ = (int) x;
  y_ = (int) y;
  draw_circ(x + W_W/2., y + W_V/2., 4., 1., 1., 0., 1.);
}
```

I will eventually put up a github link with all of the excerpts above.
