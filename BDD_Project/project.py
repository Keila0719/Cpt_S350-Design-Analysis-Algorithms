# Keila Holcombe
# Cpt_S 350 
# Spring 2026

from pyeda.inter import *
from pyeda.boolalg.bdd import BDDONE, BDDZERO

# Convert a num to a binary form and store it to var, 
# Reference: I got some help from my friend Sydney
# Return: the binary for of the num. Ex: 3 -> 00011
def convert_int_to_bdd(num, var):
    # Create a 5 bit form of representing the num
    bit = format(num, '05b')
    bit = reversed(bit)
    result = BDDONE
    index = 0
    
    # For each bit, check if it's 1 or 0 and add the designated type of variable to the result
    for current_bit in bit:
        if current_bit == '1':
            result = result & var[index]
        else:
            result = result & ~var[index]
        index += 1

    # Return the converted bdd
    return result

# It will create the even BDD
# Return: Computed EVEN
def create_EVEN(var):
    temp_EVEN = BDDZERO
    # From each one node to all other node, check if it's an even, prime, or an edge
    for i in range(32):
        # Check if the current i is an even node, if yes add the current node to even
        if i in even_value:
            temp_EVEN = temp_EVEN | convert_int_to_bdd(i, var)
    return temp_EVEN

# It will create the Prime BDD
# Return: Computed PRIME
def create_PRIME(var):
    temp_PRIME = BDDZERO
    # From each one node to all other node, check if it's an even, prime, or an edge
    for i in range(32):
        # Check if the current i is an prime node, if yes add the current node to prime
        if i in prime_value:
            temp_PRIME = temp_PRIME | convert_int_to_bdd(i, var)
    return temp_PRIME


# It will create the RR based on the the node that satisfies the if statement condition
# Return: Computed RR
def create_RR(varx, vary):
    temp_RR = BDDZERO
    for i in range(32):
        for j in range(32):
            #Replace with what is given
            if ((((i + 3) % 32) == (j % 32)) or (((i + 8) % 32) == (j % 32))):
                temp_RR = temp_RR | (convert_int_to_bdd(i, varx) & convert_int_to_bdd(j, vary))
    return temp_RR
# It will create the RR2 which is R o R from BDD RR
# Return: COmputed RR2
def create_RR2():
    temp_RR_xy = RR
    temp_RR_yz = create_RR(y, z) 
    temp_RR2 = (temp_RR_xy & temp_RR_yz).smoothing(y)
    return temp_RR2
# It will create the RR2star which is set of all node pairs such that one can reach the other in a positive even number of steps
# Return: Computed RR2*
def create_RR2_star():
    current_RR2star = RR2
    previous_RR2star = BDDZERO
    while current_RR2star != previous_RR2star:
        previous_RR2star = current_RR2star
        mapping = {x[i]: y[i] for i in range(5)}
        mapping.update({y[i]: z[i] for i in range(5)})
        new = current_RR2star & current_RR2star.compose(mapping)
        new_addon = new.smoothing({z[i] for i in range(5)})
        current_RR2star = current_RR2star | new_addon
    return current_RR2star

# Checks if the edge of num1 to num2 exist in the RR
# Return: true = edge exist, false = edge does not exist
def evaluate_RR(num1, num2):
    result =  (RR & convert_int_to_bdd(num1, x) & convert_int_to_bdd(num2, y))
    return result.satisfy_one() is not None

# Checks if the node num exist in EVEN
# Return: true = node exist, false = node does not exist
def evaluate_EVEN(num):
    result = (EVEN & convert_int_to_bdd(num, x))
    return result.satisfy_one() is not None

# Checks if the node num exist in PRIME
# Return: true = node exist, false = node does not exist
def evaluate_PRIME(num):
    result = (PRIME & convert_int_to_bdd(num, x))
    return result.satisfy_one() is not None

# Checks if the path of num1 and num2 exists in RR2
# Return: true = edge exist, false = edge does not exist
def evaluate_RR2(num1, num2):
    result = RR2 & convert_int_to_bdd(num1, x) & convert_int_to_bdd(num2, z)
    return result.satisfy_one() is not None

# Checks if the path of num1 and num2 exists in RR2*
# Return: true = edge exist, false = edge does not exist
def evaluate_RR2_star(num1, num2):
    result = RR2_star & convert_int_to_bdd(num1, x) & convert_int_to_bdd(num2, z)
    return result.satisfy_one() is not None

# Checks if the statement A on the direction is being satisfied or not
# Return: true = satisfied, false = nope
def evaluate_statementA():
    # First lets do the "There is" section which is EVEN ^ RR2*
    there_is = EVEN.compose({x[i]: y[i] for i in range(5)}) & RR2_star.compose({z[i]: y[i] for i in range(5)})
    there_is_check = there_is.smoothing(y)

    # Next lets do the "For each" section which is PRIME -> there_is_check
    for_each = ~PRIME | there_is_check 
    counterExamples = (~for_each).smoothing(x)

    # All set that passes the statement
    result = ~counterExamples

    # Return the condition of the statementA
    return result


# Tests for the 3.1 tests that was shared in the assignment direction
def test_for_3_1():
    # Test for the RR(#, #)
    print("\nTesting RR functionality:")
    print("RR(27, 3) is true: ", evaluate_RR(27, 3))
    print("RR(16, 20) is false: ", evaluate_RR(16, 20))

    # Test for the EVEN(#)
    print("\nTesting EVEN functionality:")
    print("EVEN(14) is true: ", evaluate_EVEN(14))
    print("EVEN(13) is false: ", evaluate_EVEN(13))

    # Test for the PRIME(#)
    print("\nTesting PRIME functionality:")
    print("PRIME(7) is true: ", evaluate_PRIME(7))
    print("PRIME(2) is false: ", evaluate_PRIME(2))

# Tests for the 3.2 test that was shared in the assignment direction
def test_for_3_2():
    # Test for the RR2(#, #)
    print("\nTesting RR2 functionality")
    print("RR2(27, 6) is true:", evaluate_RR2(27, 6))
    print("RR2(27, 9) is false:", evaluate_RR2(27, 9))

# Tests for the 3.3 RR2* thing
def test_for_3_3():
    # Test for the RR2*(#, #)
    print("\nTesting RR2* functionality:")
    print("RR2*(27, 6) is true: ", evaluate_RR2_star(27, 6))
    print("RR2*(27, 9) is false: ", evaluate_RR2_star(27, 9))
    print("RR2*(1, 2) is true or false depending on RR structure: ", evaluate_RR2_star(1, 2))

# Main statement
if __name__ == '__main__':
    even_value = {0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30}
    prime_value = {3, 5, 7, 11, 13, 17, 19, 23, 29, 31}

    # Create a node x, y and z that stores the 5 bool variables
    x = bddvars('x', 5)
    y = bddvars('y', 5)
    z = bddvars('z', 5)

    #Step 3.1
    RR = create_RR(x, y)
    EVEN = create_EVEN(x)
    PRIME = create_PRIME(x)
    test_for_3_1()

    # Step 3.2
    RR2 = create_RR2()
    test_for_3_2()

    # Step 3.3
    RR2_star = create_RR2_star()
    test_for_3_3()

    # Step 3.4
    statementA = bool(evaluate_statementA())
    print("\nStatementA: ", statementA, "\n") 
    

# Step 1: Build RR from scratch
def create_RR():
    temp_RR = BDDZERO
    for i in range(4):
        for j in range(4):
            # Example edge condition 
            # (Replace with what is given)
            if (i + 1) % 4 == j or (i + 2) % 4 == j:
                temp_RR = temp_RR | (
                    convert_int_to_bdd(i, x) &
                    convert_int_to_bdd(j, y)
                )
    return temp_RR

# Step 2: RR2 (2-step reachability)
def create_RR2():
    RR_xy = RR
    RR_yz = RR.compose({
        x[i]: y[i] for i in range(2)
    })
    RR2 = (RR_xy & RR_yz).smoothing(y)
    return RR2

# Step 3: R* (transitive closure)
def create_R_star():
    R_star = RR
    previous = BDDZERO
    while R_star != previous:
        previous = R_star
        RR_xy = R_star
        RR_yz = RR.compose({
            x[i]: y[i] for i in range(2)
        })
        new_paths = (RR_xy & RR_yz).smoothing(y)
        R_star = R_star | new_paths
    return R_star