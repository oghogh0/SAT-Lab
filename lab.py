"""
6.1010 Spring '23 Lab 8: SAT Solver
"""

#!/usr/bin/env python3

import sys
import typing
import doctest

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS


def update_function(formula, variable):
    """
    Args:
        formula: CNF formula
        updated_variables: tuple of var & updated
                        bool
    Returns:
        updated formula
    """
    new_formula = []
    for statement in formula:
        if variable in statement:  # if chosen value same as set value
            continue  # don't append
        if (variable[0], not variable[1]) in statement:
            new_statement = []
            for clause in statement:
                if clause != (variable[0], not variable[1]):
                    new_statement.append(clause)  # acc for dupes
            new_formula.append(new_statement)  # statement without var
        else:  # if var not in statement
            new_formula.append(statement)
    return new_formula


def update_with_unit_clause(formula):
    """
    Given a formula, updates formula applies unit clauses
    """
    for clause in formula:
        if len(clause) == 1:
            unit_formula = update_function(formula, clause[0])
            return (unit_formula, clause[0])
    return formula, None


def satisfying_assignment(formula):
    """ 
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.
    """
    if formula == []:
        return {}
    if [] in formula:  # doesn't work
        return None
    solution = {}
    # print(len(formula))

    initial_tup = formula[0][0]
    for clause in formula:
        if len(clause) == 1:
            initial_tup = clause[0]

    assignment = satisfying_assignment(update_function(formula, initial_tup))
    if assignment is not None:
        solution.update(assignment)  # with unit clause
        solution[initial_tup[0]] = initial_tup[1]  # var as key, bool as val in dict
        return solution

    opp_solution = {}
    new_tup = (initial_tup[0], not initial_tup[1])

    opp_assignment = satisfying_assignment(update_function(formula, new_tup))
    if opp_assignment is not None:
        opp_solution.update(opp_assignment)
        opp_solution[new_tup[0]] = new_tup[1]
        return opp_solution
    return None


def satisfying_assignment_helper(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False 
    or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """

    unit_formula = formula
    unit_dict = {}

    formula = unit_formula
    solution = unit_dict
    result = satisfying_assignment(unit_formula)

    if result is not None:
        solution.update(result)
    else:
        return None
    return solution

    

def match_representation_rule(board):
    """
    Given a board representation,
    return a cnf that matches that representation
    """
    matched_cnf = []

    for row, rep in enumerate(board):
        for col, num in enumerate(rep):
            if num:  # doesn't append for 0
                matched_cnf.append([((row, col, num), True)])
    return matched_cnf


def valid_range_rule(n):
    """
    Given a board,
    return a cnf formula that value is in dimension range
    """
    cnf_formula_range = []

    for row in range(n):
        for col in range(n):
            clause = []
            for num in range(1, n + 1):
                clause.append(((row, col) + (num,), True))
            cnf_formula_range.append(clause)
    return cnf_formula_range



def get_coordinates(dim_n, char, num):
    """
    Given a dimension n and char = row or col and the row/col number,
    return a list of all coordinates in that row
    """
    if char == "row":
        return [(num, col) for col in range(dim_n)]
    else:
        return [(row, num) for row in range(dim_n)]





def value_once_row_rule2(n):
    """
    Given a board dimension n,
    returns a cnf formula where each row has each
    digit at least once
    """
    cnf_formula_row_least = []

    for row_num in range(n):
        row_coords = get_coordinates(n, "row", row_num)

        for value in range(1, n + 1):
            clause = []
            for coord in row_coords:
                clause.append(((coord) + (value,), True))
            cnf_formula_row_least.append(clause)

    return cnf_formula_row_least




def value_once_col_rule2(n):
    """
    Given a board dimension n,
    returns a cnf formula where each col has each
    digit at least once
    """
    cnf_formula_col_least = []

    for col_num in range(n):
        col_coords = get_coordinates(n, "col", col_num)

        for value in range(1, n + 1):
            clause = []
            for coord in col_coords:
                clause.append(((coord) + (value,), True))
            cnf_formula_col_least.append(clause)
        # for value in range(1,n+1):
    return cnf_formula_col_least


def get_subgrid_coordinates(root_n, start_coord):
    """
    Given a dimension sqrt n , and starting coordinate
    i.e. first coord in subgrid,
    returns a list of all coordinates in subgrid
    """
    subgrid_coords = []
    for row in range(start_coord[0], start_coord[0] + root_n):
        for col in range(start_coord[1], start_coord[1] + root_n):
            subgrid_coords.append((row, col))
    return subgrid_coords


def value_once_subgrid_rule2(n):
    """
    Given a board dimension n,
    returns a cnf formula where each subgrid has each
    digit at least once
    """
    sqrt_n = int(n ** (1 / 2))
    cnf_formula_subg_least = []
    for i in range(sqrt_n):
        for j in range(sqrt_n):
            subg_coords = get_subgrid_coordinates(sqrt_n, [i * sqrt_n, j * sqrt_n])
            for value in range(1, n + 1):
                clause = []
                for coord in subg_coords:
                    clause.append(((coord) + (value,), True))
                cnf_formula_subg_least.append(clause)
    return cnf_formula_subg_least





def make_combinations(list_clauses):
    """
    Given a list of clauses with of True statements, 
    returns combinations of pairs of clauses for False
    """
    clauses = []
    for clause in list_clauses:
        for i, (coord_value, _) in enumerate(clause):
            for coord_value_2, _ in clause[i + 1 :]:
                clauses.append([(coord_value, False), (coord_value_2, False)])
    return clauses


def sudoku_board_to_sat_formula(sudoku_board):
    """
    Generates a SAT formula that, when solved, represents a solution to the
    given sudoku board.  The result should be a formula of the right form to be
    passed to the satisfying_assignment function above.
    """
    n = len(sudoku_board)
    at_least_one = (
        valid_range_rule(n)
        + value_once_row_rule2(n)
        + value_once_col_rule2(n)
        + value_once_subgrid_rule2(n)
    )
    at_most_one = make_combinations(at_least_one)
    return match_representation_rule(sudoku_board) + at_most_one + at_least_one


def create_nd_array(dimensions, value):
    """
    Args:
        dimesnions: list of dimensions
        value: num
    Returns:
        n-d array with dimensions in 'dimensions' list 
        with each value in the array being the given value
    """
    if len(dimensions) == 1:
        return [value] * dimensions[0]
    else:
        # create_nd_array(dimensions[1:], value) 
        # finds what the array you want looks like 
        # - don't store bc of aliasing
        return [create_nd_array(dimensions[1:], value) for i in range(dimensions[0])]


def replace_coordinate_value(nd_array, coordinate, value):
    """
    Args:
        nd_array : n-dimension array
        coordinate : tuple/list of coordinates
        value: replacement value

    Returns:
        n-dimension array with coordinates value
        replaced by given value
    """
    if not isinstance(nd_array[0], list):
        nd_array[coordinate[0]] = value
    else:
        replace_coordinate_value(nd_array[coordinate[0]], coordinate[1:], value)
    return nd_array  # return at end


def assignments_to_sudoku_board(assignments, n):
    """
    Given a variable assignment as given by satisfying_assignment (dict), as well as a
    size n, construct an n-by-n 2-d array (list-of-lists) representing the
    solution given by the provided assignment of variables.

    If the given assignments correspond to an unsolvable board, return None
    instead.
    """
    sudoku_board = create_nd_array([n, n], -1)
    if assignments is None:
        return None
    else:
        for position in assignments:
            if assignments[position]:
                replace_coordinate_value(sudoku_board, position[:2], position[2])
        return sudoku_board


if __name__ == "__main__":
    # _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # doctest.testmod(optionflags=_doctest_flags)
    formula_one = [
        [("a", True), ("b", True), ("c", True)],
        [("a", False), ("f", True)],
        [("d", False), ("e", True), ("a", True), ("g", True)],
        [("h", False), ("c", True), ("a", False), ("f", True)],
    ]
    # opp_formula_one = [
    #                 [('a', False), ('b', True), ('c', True)],
    #                 [('a', True), ('f', True)],
    #                 [('d', False), ('e', True), ('a', False), ('g', True)],
    #                 [('h', False), ('c', True), ('a', True), ('f', True)],
    #             ]
    # # print(negate_formula(formula_one, ('a',False)))
    # print(update_function(formula_one, ('a',False)))
    print(satisfying_assignment(formula_one))
    # # print(formula_one)
    # # print(satisfying_assignment(opp_formula_one))
    # formula_two = [
    #                 [('a', True), ('b', True), ('c', True)],
    #                 [('a', False), ('f', True)],
    #                 ]
    # # print(update_function(formula_two, [('a',True)]))
    # # print(satisfying_assignment(formula_two))
    # formula_three=[
    #                 [('a',True)],
    #                 [('b',False)]
    # ]
    # # print(update_function(formula_three, [('a',True),('b',False)]))
    # formula_four = [
    #                 [('a', True), ('b', True), ('c', True)],
    #                 [('a', False), ('f', True)]]
    # # print(satisfying_assignment(formula_one))

    # unit_one = [
    #                 [('a', True), ('b', True), ('c', True)],
    #                 [('a',False)],
    #                 [('d', False), ('e', True), ('a', True), ('g', True)],
    #                 [('h', False), ('c', True), ('a', False), ('f', True)],
    #             ]
    # # print(apply_unit_clause(unit_one))
    # cnf = [[('a', True), ('a', False)],
    #        [('b', True), ('a', True)],
    #        [('b', True)],
    #        [('b', False), ('b', False), ('a', False)],
    #        [('c', True), ('d', True)],
    #        [('c', True), ('d', True)]]
    cnff = [
        [("b", True)],
        [("b", False), ("a", False)],
        [("c", True), ("d", True)],
        [("c", True), ("d", True)],
    ]
    # # print(update_function(cnf,('a',True)))
    # # print(update_function(cnff,('b',True)))
    # # print(satisfying_assignment(cnf))

    # cnf_two = [
    #         [("a", True), ("b", True)],
    #         [("a", False), ("b", False), ("c", True)],
    #         [("b", True), ("c", True)],
    #         [("b", True), ("c", False)],
    #     ]
    # print(satisfying_assignment(cnff))

    four_by_four = [
        [1, 0, 0, 0],
        [0, 0, 0, 4],
        [3, 0, 0, 0],
        [0, 0, 0, 2],
    ]
    four_by_four_sol = [
        [1, 4, 2, 3],
        [2, 3, 1, 4],
        [3, 2, 4, 1],
        [4, 1, 3, 2],
    ]
    # print(value_once_row_rule_2(four_by_four))
    # print(sudoku_board_to_sat_formula(four_by_four))
    sat_f = sudoku_board_to_sat_formula(four_by_four)
    # for r,c,val in satisfying_assignment(sat_f):
    #     four_by_four[r][c] = val
    # print(four_by_four)
    # print(assignments_to_sudoku_board(satisfying_assignment(sat_f),4))
    # print(match_representation_rule(four_by_four))
    # print(get_coordinates(four_by_four,"row", 0))
    # print(coord_combinations([(0, 0), (1, 0), (2, 0), (3, 0)]))
    # print(value_once_col_rule(four_by_four))

    # print(len(make_combinations(value_once_col_rule2(4))))
    # print(valid_range_rule(4))
    # print(value_combinations(3))
    # print(one_digit_rule(four_by_four))
    # print(get_subgrid_coordinates(2, (2,2)))
    # print(len(value_once_subgrid_rule2(four_by_four)))
    # print(create_nd_array([2,2], 0))


# def negate_formula(formula, var):
#     """
#     Returns mutated formula if setting boolean value to False # SHOULD MUTATE??
#     """
#     for indx,statement in enumerate(formula):
#         if not var[1]: # if False
#             if var in statement:
#                 current_indx = statement.index(var)
#                 statement.insert(current_indx,(var[0], True)) # replaces False with T
#                 statement.remove(var)
#             elif (var[0],True) in statement:
#                 current_indx = statement.index((var[0],True))
#                 statement.insert(current_indx,(var[0], False)) # replaces True with F
#                 statement.remove((var[0],True))
#         formula[indx] = statement # replaces old statement w new one
#     return formula
