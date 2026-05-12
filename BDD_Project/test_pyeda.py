# Mark Shinozaki
# Cpts-350 
# Title: Symbolic Graph Project

from pyeda.inter import *

# Compatibility adjustment for newer Python versions
import collections
collections.Sequence = collections.abc.Sequence

# Graph G construction:
# G is a graph with 32 nodes. An edge exists from node i to node j if:
# - (i + 3) % 32 == j % 32 or (i + 8) % 32 == j % 32
# Using the modulo operator to establish edge conditions.

# Define BDD variables for x, y, and z
x, y, z = bddvars('x', 5), bddvars('y', 5), bddvars('z', 5)

# Generate binary expression for a number using a specified variable
def num_to_expr(num, var):
    binary_format = "{:05b}".format(num)
    expression = ""
    for bit_index, bit in enumerate(binary_format):
        if bit_index > 0:
            expression += "&"
        if bit == '0':
            expression += "~"
        expression += f"{var}[{bit_index}]"
    return expression

# Create an expression for a list of numbers using a specified variable
def list_to_bdd_expr(numbers, var):
    combined_expr = ""
    for number in numbers:
        if combined_expr:
            combined_expr += "|"
        combined_expr += f"({num_to_expr(number, var)})"
    return expr(combined_expr)

# Generates the graph G's representation as an expression
def graph_g_expression():
    graph_expr = ""
    for i in range(32):
        for j in range(32):
            if (i + 3) % 32 == j % 32 or (i + 8) % 32 == j % 32:
                if graph_expr:
                    graph_expr += "|"
                graph_expr += f"(({num_to_expr(i, 'x')})&({num_to_expr(j, 'y')}))"
    return expr(graph_expr)

# Computes the transitive closure for 2 steps
def two_step_transitive_closure(step1, step2):
    step1 = step1.compose({y[i]: z[i] for i in range(5)})
    step2 = step2.compose({x[i]: z[i] for i in range(5)})
    return step1 & step2

# Computes the reflexive-transitive closure
def reflexive_transitive_closure(initial_rr):
    rt_closure = initial_rr
    while True:
        previous_closure = rt_closure
        rt_closure = previous_closure | two_step_transitive_closure(rt_closure, initial_rr)
        if rt_closure.equivalent(previous_closure):
            break
    return rt_closure

# Convert a number to a dictionary mapping for BDD restriction
def num_to_dict(num, var):
    binary_format = "{:05b}".format(num)
    return {var[i]: int(bit) for i, bit in enumerate(binary_format)}

# Testing functions for the BDDs
def test_RR(num1, num2):
    val1 = num_to_dict(num1, x)
    val2 = num_to_dict(num2, y)
    val1.update(val2)
    return bool(RR_BDD.restrict(val1))

def test_even(num):
    val = num_to_dict(num, y)
    return bool(E_BDD.restrict(val))

def test_prime(num):
    val = num_to_dict(num, x)
    return bool(P_BDD.restrict(val))

def test_RR2(num1, num2):
    val1 = num_to_dict(num1, x)
    val2 = num_to_dict(num2, y)
    val1.update(val2)
    return bool(RR2_BDD.restrict(val1))

def test_RR2Star(num1, num2):
    val1 = num_to_dict(num1, x)
    val2 = num_to_dict(num2, y)
    val1.update(val2)
    return bool(RR2Star_BDD.restrict(val1))

def perform_tests():
    print("Testing RR Functionality:")
    print(f"RR(27, 3) should be True: {test_RR(27, 3)}")
    print(f"RR(16, 20) should be False: {test_RR(16, 20)}\n")

    print("Testing EVEN Functionality:")
    print(f"EVEN(14) should be True: {test_even(14)}")
    print(f"EVEN(13) should be False: {test_even(13)}\n")

    print("Testing PRIME Functionality:")
    print(f"PRIME(7) should be True: {test_prime(7)}")
    print(f"PRIME(2) should be True: {test_prime(2)}\n")

    print("Testing RR2 Functionality:")
    print(f"RR2(27, 6) should be True or False based on definition: {test_RR2(27, 6)}")
    print(f"RR2(27, 9) should be True or False based on definition: {test_RR2(27, 9)}\n")

    print("Testing RR2Star Functionality:")
    print(f"RR2Star(23, 2) should be True or False based on closure properties: {test_RR2Star(23, 2)}")
    print(f"RR2Star(29, 11) should be True or False based on closure properties: {test_RR2Star(29, 11)}")

def verify_statementA(RR2Star_BDD, P_BDD, E_BDD):
    # For StatementA, I want to verify that for every prime number node u,
    # there exists an even number node v such that u can reach v in a positive even number of steps.
    
    # Step 1: Project RR2Star onto the prime and even nodes
    prime_to_even_projection = P_BDD.smoothing(x) & E_BDD.smoothing(y) & RR2Star_BDD

    # Step 2: Check if for all prime nodes, there exists a path to an even node
    # We achieve this by checking if the projection is non-empty 
    verification_result = prime_to_even_projection.is_one()

    return verification_result

# Execute tests
if __name__ == '__main__':
    x, y, z = bddvars('x', 5), bddvars('y', 5), bddvars('z', 5)

    # Create BDDs for graph G, prime numbers, and even numbers
    RR_BDD = expr2bdd(graph_g_expression())
    P_BDD = expr2bdd(list_to_bdd_expr([3, 5, 7, 11, 13, 17, 19, 23, 29, 31], 'x'))
    E_BDD = expr2bdd(list_to_bdd_expr(list(range(0, 32, 2)), 'y'))

    # Compute BDD for 2-step reachability and reflexive-transitive closure
    RR2_BDD = two_step_transitive_closure(RR_BDD, RR_BDD)
    RR2_BDD = RR2_BDD.smoothing(z)
    RR2Star_BDD = reflexive_transitive_closure(RR_BDD)

    # Run tests
    perform_tests()
    
    # Verify StatementA
    statementA_result = verify_statementA(RR2Star_BDD, P_BDD, E_BDD)
    print(f"\nVerification of StatementA (Every prime can reach an even in an even number of steps): {statementA_result}")
