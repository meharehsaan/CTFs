#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>

char * names[] = {
    "General Kenobi",
    "Leia Organa",
    "Luke Skywalker",
    "Darth Vader",
    "Yoda",
    "Han Solo"
};

#define n_array (sizeof (names) / sizeof (const char *))

struct Highscore {
    char new_name[32];
    unsigned int score;
    char *name; 
};

struct Highscore highscore = { "", 1, 0x0  };
/home/mehar/tmp/codemind.c
void error(char *msg) {
    perror(msg);
    exit(1);
}

void print_header() {
    time_t timer;
    char buffer[26];
    struct tm* tm_info;
    time(&timer);

    tm_info = localtime(&timer);
    strftime(buffer, 26, "%Y-%m-%d %H:%M:%S", tm_info);
    printf("Hello there! It's %s and the weather looks pretty nice!\n\n", buffer);

    srand(timer);
    printf("Timer = %d\n", timer);
    // int randval = rand();
    // printf("first rand = %d\n", (randval));
    highscore.name = names[ rand() % n_array];
    highscore.score = (rand() % 32) + 1;
    // highscore.score = 1;
    // printf("High score = %d\n", highscore.score);
    // printf("hello %d", rand() % 2);
}

void show_highscore() {
    printf("Current highscore:\n%d\t by \t %s\n", highscore.score, highscore.name);
}

void set_highscore_name() {
    char buffer[256];
    ssize_t size;
    printf("Give me your name: ");
    highscore.name = highscore.new_name;
    size = read(0, buffer, 1024);
    memcpy( highscore.new_name, buffer, size);
    show_highscore();
}

void play_game() {
    unsigned int score = 0;
    unsigned int random_number = 0;
    unsigned int guessed_number = 0;
    printf("Can you guess my numbers?\n> ");
    while( 1 ) {
        random_number = rand();
        scanf("%d", &guessed_number);
        if(guessed_number == random_number) {
            printf("You were lucky this time!\n>");
        } else {
            printf("Game over!\n");
            break;
        }
        score++;
    }

    printf("Score is %d\n", score);
    printf("Highscore Score is %d\n", highscore.score);

    if( score >= highscore.score ) {
        printf("New Highscore! Amazing!\n");
        highscore.score = score;
        set_highscore_name();
    }
}

void mindgames()
{
    unsigned int choice = 0;
    print_header();

    printf("\nWe should play a game of the mind!\n> ");
    while( 1 ) {
        printf("What do you want to do?\n 1) Show Highscore\n 2) Play the game\n 3) Exit\n> ");
        scanf("%d", &choice); 
        switch(choice) {
            case 1: show_highscore();
                    break;
            case 2: play_game();
                    break;
            default: exit(0);
        }
    }
}


int main()
{
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    // mindgames();
    print_header();
    set_highscore_name();
}