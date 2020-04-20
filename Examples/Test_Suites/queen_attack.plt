:- begin_tests(queen_attack).

    test(create_in_center, condition(true)) :- create((3,3)).

    test(valid_position) :- create((2,2)).

    test(must_have_positive_row, [fail]) :- create((-2,2)).

    test(row_smaller_than_board_size, [fail]) :- create((8,4)).

    test(must_have_positive_column, [fail]) :- create((2,-2)).

    test(column_smaller_than_board_size, [fail]) :- create((4,8)).

    test(cant_attack, [fail]) :- attack((2,4), (6,6)).

    test(attack_on_same_row) :- attack((2,4), (2,6)).

    test(attack_same_column) :- attack((4,5), (2,5)).

    test(attack_first_diagonal) :- attack((2,2), (0,4)).

    test(attack_second_diagonal) :- attack((2,2), (3,1)).

    test(attack_third_diagonal) :- attack((2,2), (1,1)).

    test(attack_fourth_diagonal) :- attack((2,2), (5,5)).

:- end_tests(queen_attack).
