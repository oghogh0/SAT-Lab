<h1>Sat Lab</h1>
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
