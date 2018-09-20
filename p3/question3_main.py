import question3_1
import question3_2
import question3_3

def main():
    
    # use Genetic algorithm to find the good position and the possibility of the Constellation, this need about 6 hours in a i7 computer. 
    # and print the ind
    print("start")
    ind = question3_1.main(5)
    print(ind)

    # or you can just run my solution, and the drawing function need lots of times too. 
    question3_3.main( )


if __name__ == "__main__":
    main()