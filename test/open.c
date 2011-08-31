#include <stdio.h>
#include <sys/types.h>
#include <getopt.h>
#include <fcntl.h>

int main(int argc, char* argv[]){
    int fd = open ("-", O_WRONLY | O_CREAT | O_NONBLOCK | O_NOCTTY,
             S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
    printf("%d\n", fd);
    return 0;
}
