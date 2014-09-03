from game_run_to_anthill import _main
import time

if __name__ == "__main__":
    barriers = (5, 10, 15, 20)
    updown = (10, 15, 20, 25)
    leftright = (10, 15, 20, 30, 50)

    _main(0, 0, 0, True)

    for number_of_barriers in barriers:
        for up_down_step_value in updown:
            for left_right_step_value in leftright:
                _time = 0
                _error = 0

                for x in range(100):
                    start = time.time()
                    try:
                        _main(number_of_barriers, up_down_step_value, left_right_step_value)
                    except:
                        _error += 1
                    else:
                        _time += (time.time() - start)

                print("#####################################################")
                print(number_of_barriers, up_down_step_value, left_right_step_value)
                print("Error - ", _error)
                print("Time - ", _time)
                print("Time per once - ", _time / max(1, 100 - _error))

    print("THE END")