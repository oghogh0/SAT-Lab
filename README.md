<h1>SAT Lab</h1>
<h2>Description</h2>
In this lab, we'll look at the problem of Boolean satisfiability. The goal is: given a description of Boolean variables and constraints on them, find a set of assignments that satisfies all of the given constraints. In encoding the puzzle, we follow a very regular structure in our Boolean formulas: conjunctive normal form (CNF). In this form, we say that a literal is a variable or the not of a variable. Then a clause is a multiway 'or' of literals, and a CNF formula is a multiway 'and' of clauses. <br /> 

When represent problems in CNF as follows: <br /> 
- a variable: a Python string <br /> 
- a literal: a pair (a tuple), containing a variable and a Boolean value (False if 'not' appears in this literal, True otherwise) <br /> 
- a clause: a list of literals <br /> 
- a formula: a list of clauses <br />

 
<h2>Languages and Environments Used</h2>

- <b>Python</b> 
- <b>VS code</b>

<h2>Program walk-through</h2>

<p align="left">
UPDATING EXPRESSIONS:<br/>
A key operation here is updating a formula to model the effect of a variable assignment.<br/>

The first 'update' function I have implemented takes in a CNF formula and a tuple(var, updated boolean), and returns an updated formula.<br/>

For example, given the formula:<br/>

formula_one = [<br/>
        [("a", True), ("b", True), ("c", True)],<br/>
        [("a", False), ("f", True)],<br/>
        [("d", False), ("e", True), ("a", True), ("g", True)],<br/>
        [("h", False), ("c", True), ("a", False), ("f", True)],<br/>
    ]<br/>

Calling update_function(formula_one, ('a',False)) returns:<br/>

[[('b', True), ('c', True)], [('d', False), ('e', True), ('g', True)]]
<br/>

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

<br/>
In the procedure described above, if setting the value of x immediately leads to a contradiction, we can immediately discard that possibility (rather than waiting for a later step in the recursive process to notice the contradiction). Therefore, to optimise the previous approach, I have implemented 'update_with_unit_clause'. Unit clauses are lenght-one clauses. If such a clause [(x, b)] exists, then we may set x to Boolean value b, just as we do in the True and False cases. However, we know that, if this setting leads to failure, there is no need to backtrack and also try x = not b (because the unit clause alone tells us exactly what the value of x must be). Thus, the function begins with a loop that repeatedly finds unit clauses, if any, and propagates their consequences through the formula before making any recursive calls. Propagating the effects of one unit clause may reveal further unit clauses, whose later propagations may themselves reveal more unit clauses, and so on.<br/><br/>

    for clause in formula:
        if len(clause) == 1:
            unit_formula = update_function(formula, clause[0])
            return (unit_formula, clause[0])
    return formula, None
<br/>
<p align="left">
REDUCTION to SAT:<br/>
In this last part of the lab, I have implemented a reduction to SAT from Sudoku puzzles, however this idea has been expanded to work with boards of different sizes.<br/>

Sudoku Description: a solution to a standard Sudoku puzzle represents an arrangement of the digits 1-9 on a grid such that every row contains each digit exactly once, every column contains each digit exactly once, each of the 3×3 blocks that make up the grid contains each digit exactly once. The puzzles are represented as 2-d arrays (lists-of-lists) of numbers, where a 0 = empty. Here is an example puzzle:<br/>
[   <br/>
[5, 3, 0, 0, 7, 0, 0, 0, 0],<br/>
[6, 0, 0, 1, 9, 5, 0, 0, 0],<br/>
[0, 9, 8, 0, 0, 0, 0, 6, 0],<br/>
[8, 0, 0, 0, 6, 0, 0, 0, 3],<br/>
[4, 0, 0, 8, 0, 3, 0, 0, 1],<br/>
[7, 0, 0, 0, 2, 0, 0, 0, 6],<br/>
[0, 6, 0, 0, 0, 0, 2, 8, 0],<br/>
[0, 0, 0, 4, 1, 9, 0, 0, 5],<br/>
[0, 0, 0, 0, 8, 0, 0, 7, 9]]<br/>
<br/>
We'll expand on this idea a little bit by allowing for boards of size n×n, where n is a perfect square (so 4×4, 9×9, 16×16, 144×144, etc, are all valid board sizes). With this change in mind, we still have similar constraints on the board:<br/>
- Each cell must contain one of the numbers between 1 and n, inclusive.<br/>
- Each row must contain all of the numbers from 1 to n exactly once.<br/>
- Each column must contain all of the numbers from 1 to n exactly once.<br/>
- Each subgrid must contain all of the numbers from 1 to n exactly once.<br/>

One key difference from the standard 9×9 board is the number of the subgrids, as well as their size and placement. Each subgrid is n×n, and there will be a total of n subgrids. The top-left-most subgrid always has its upper-left-most corner at row 0, column 0
subgrids never overlap. <br/>

There are 3 steps involved:<br/>
1. Generate a SAT formula based on a given Sudoku board.<br/>
2. Use our SAT solver to find a solution to the formula.<br/>
3. Reinterpret the output from the solver in terms of the original puzzle.<br/>

<br/>
<p align="left">
IMPLEMENTATION:<br/>

Firstly, I have made a function that finds and returns a satisfying assignment for a given CNF formula, if one exists. 'satisfying_assignment_helper' does the same for unit formulae. This covers step 2 in the previous section.<br/>
For example, given the formula:<br/>

formula_one = [<br/>
        [("a", True), ("b", True), ("c", True)],<br/>
        [("a", False), ("f", True)],<br/>
        [("d", False), ("e", True), ("a", True), ("g", True)],<br/>
        [("h", False), ("c", True), ("a", False), ("f", True)],<br/>
    ]<br/>

Calling satisfy_assignment(formula_one) returns:<br/>

{'f': True, 'a': True}<br/>

    if formula == []:
        return {}
    if [] in formula:  # doesn't work
        return None
    solution = {}
    print(len(formula))

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

<br/>  
Secondly, for step 1 from the previous section I created a function that generates a SAT formula that, when solved, represents a solution to the given sudoku board.  The result is a formula of the right form to be passed to the 'satisfying_assignment' function above. The code is as follows:<br/><br/>

    n = len(sudoku_board)
    at_least_one = (
        valid_range_rule(n)
        + value_once_row_rule2(n)
        + value_once_col_rule2(n)
        + value_once_subgrid_rule2(n)
    )
    at_most_one = make_combinations(at_least_one)
    return match_representation_rule(sudoku_board) + at_most_one + at_least_one

This code consists of 6 functions:<br/>
1. match_representation_rule: returns a CNF that matches the given board representation. <br/>
    
        matched_cnf = []
    
        for row, rep in enumerate(board):
            for col, num in enumerate(rep):
                if num:  # doesn't append for 0
                    matched_cnf.append([((row, col, num), True)])
        return matched_cnf
<br/>
2. make_combinations: given a list of clauses with True statements, returns combinations of pairs of clauses for False. <br/> 
    
        clauses = []
        for clause in list_clauses:
            for i, (coord_value, _) in enumerate(clause):
                for coord_value_2, _ in clause[i + 1 :]:
                    clauses.append([(coord_value, False), (coord_value_2, False)])
        return clauses
<br/> 
3. valid_range_rule: returns a CNF formula with values is in the board dimension range.<br/>

        cnf_formula_range = []
    
        for row in range(n):
            for col in range(n):
                clause = []
                for num in range(1, n + 1):
                    clause.append(((row, col) + (num,), True))
                cnf_formula_range.append(clause)
        return cnf_formula_range
<br/>
4. value_once_row_rule2: returns a CNF formula where each row has each digit at least once given the board dimension. <br/>
 
        cnf_formula_row_least = []
    
        for row_num in range(n):
            row_coords = get_coordinates(n, "row", row_num)
    
            for value in range(1, n + 1):
                clause = []
                for coord in row_coords:
                    clause.append(((coord) + (value,), True))
                cnf_formula_row_least.append(clause)
    
        return cnf_formula_row_least
<br/> 
5. value_once_col_rule2: returns a CNF formula where each column has each digit at least once given the board dimension. <br/>

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

<br/> 
6. value_once_subgrid_rule2): returns a CNF formula where each subgrid has each digit at least once given the board dimension. <br/> 

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
<br/> 
HELPER FUNCTIONS:  <br/> 
-get_coordinates: returns a list of all coordinates in a row given a dimension n and char = row or col and the row/col number. <br/> 

          if char == "row":
              return [(num, col) for col in range(dim_n)]
          else:
              return [(row, num) for row in range(dim_n)]
<br/> 
-get_subgrid_coordinates: returns a list of all coordinates in a subgrid given a dimension sqrt n , and starting coordinate i.e. first coord in subgrid.<br/> 

          subgrid_coords = []
          for row in range(start_coord[0], start_coord[0] + root_n):
              for col in range(start_coord[1], start_coord[1] + root_n):
                  subgrid_coords.append((row, col))
          return subgrid_coords

<br/>  
Lastly, for step 3 from the previous section I created a function that constructs an n-by-n 2-d array (list-of-lists) representing the solution as given by 'satisfying_assignment'. Instead, it returns None if the given assignments correspond to an unsolvable board.The code is as follows:<br/><br/>

          sudoku_board = create_nd_array([n, n], -1)
          if assignments is None:
              return None
          else:
              for position in assignments:
                  if assignments[position]:
                      replace_coordinate_value(sudoku_board, position[:2], position[2])
              return sudoku_board
<br/> 
HELPER FUNCTIONS:<br/> 
-create_nd_array: creates an N-D array with dimensions in 'dimensions' list with each value in the array being the given value. <br/> 
     
         if len(dimensions) == 1:
             return [value] * dimensions[0]
         else:
             # finds what the array you want looks like 
             # - don't store bc of aliasing
             return [create_nd_array(dimensions[1:], value) for i in range(dimensions[0])]


-replace_coordinate_value: returns an N-D array with coordinates values replaced by a given value.<br/> 

         if not isinstance(nd_array[0], list):
             nd_array[coordinate[0]] = value
         else:
             replace_coordinate_value(nd_array[coordinate[0]], coordinate[1:], value)
         return nd_array  # return at end






