#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>

//============= First understand the code deeply to exploit binaries ===========

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

// first it fills 32 bytes and then score value and then writes puts got in *name

struct Highscore highscore = { "", 1, 0x0  };

void error(char *msg) {
    perror(msg);
    exit(1);
}

void print_header() {
    time_t timer;
    char buffer[26];
    struct tm* tm_info;
    time(&timer);

    tm_info = localtime(&timer);          // creating a random value using localtime of system
    strftime(buffer, 26, "%Y-%m-%d %H:%M:%S", tm_info);
    printf("Hello there! It's %s and the weather looks pretty nice!\n\n", buffer);

    srand(timer);                    // the local time is seed of srand which creates random values
    highscore.name = names[ rand() % n_array];
    highscore.score = (rand() % 32) + 1;   // random value is going in score
}

void show_highscore() {              // this is only showing highscore to us
    printf("Current highscore:\n%d\t by \t %s\n", highscore.score, highscore.name);
}

void set_highscore_name() {   // here buffer overflow exists
    char buffer[256];
    ssize_t size;
    printf("Give me your name: ");
    highscore.name = highscore.new_name;
    size = read(0, buffer, 1024);
    memcpy( highscore.new_name, buffer, size);  //string in the buffer of 32 
    // when this funciton end control goes to 
}

void play_game() {  // when this end control goes to mindgame()
    unsigned int score = 0;
    unsigned int random_number = 0;
    unsigned int guessed_number = 0;
    // creating three variables
    printf("Can you guess my numbers?\n> ");
    while( 1 ) {            // entering in infinite loop
        random_number = rand();            // creating a random value
        scanf("%d", &guessed_number);      // getting value from user
        if(guessed_number == random_number) {   // to call vulnerable function we have to guess random values
            printf("You were lucky this time!\n>");
        } else {
            printf("Game over!\n");
            break; // if our guess is wrong it will break loop
        }
        score++;                  // if we guess the correct value it will increment score value and ask again for value from us
    }            

// after loop it will check this 

    if( score >= highscore.score ) {     // if our score value greater than it call 
        printf("New Highscore! Amazing!\n");
        highscore.score = score;
        set_highscore_name();          // this is the function which is vulnerable we have to call this
    }
}

void mindgames()
{
    unsigned int choice = 0;
    print_header();                 //calling this why check first

    printf("\nWe should play a game of the mind!\n> ");
    while( 1 ) {                  // we are entering in infinite loop
        printf("What do you want to do?\n 1) Show Highscore\n 2) Play the game\n 3) Exit\n> ");
        scanf("%d", &choice); 
        switch(choice) {
            case 1: show_highscore();       // only shows score value and random name
                    break;
            case 2: play_game();             // this is the main function
                    break;
            default: exit(0);
        }
    }
}
// here now we will call and get puts got values

int main()
{
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    mindgames();
}