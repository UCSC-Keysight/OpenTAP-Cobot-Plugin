
# This block does not work, currently an issue with importing UR3e ########################

import sys
sys.path.append('../UR_Prototype')
import UR3e


test_ur3e = UR3e.UR3e()
print(sys)
def test_move_request():
    # setup
    command = "movej([1, 1, 0, 1, 0, 1], a=1.2, v=1.05)"

    assert UR3e.send_request_movement(test_ur3e, command) != None

###########################################################################################


# This block does work, using the file eztest.py ##########################################

# import sys
# sys.path.append('../UR_Prototype')
# import eztest

# def test_hello():
#     assert eztest.hello() == 1

###########################################################################################