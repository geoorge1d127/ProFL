:- begin_tests(complex_numbers).

    test(real_part_of_a_purely_real_number, condition(true)) :- real((1,0),R), R =:= 1.

    test(real_part_of_a_purely_imaginary_number) :- real((0,1),R), R =:= 0.

    test(real_part_of_a_number_with_real_and_imaginary_part) :- real((1,2),R), R =:= 1.

    test(imaginary_part_of_a_purely_real_number) :- imaginary((1,0),R), R =:= 0.

    test(imaginary_part_of_a_purely_imaginary_number) :- imaginary((0,1),R), R =:= 1.

    test(imaginary_part_of_a_number_with_real_and_imaginary_part) :- imaginary((1,2),R), R =:= 2.

    test(add_purely_real_numbers) :- add((1,0), (2,0), (X,Y)), X =:= 3, Y =:= 0.

    test(add_purely_imaginary_numbers) :- add((0,1), (0,2), (X,Y)), X =:= 0, Y =:= 3.

    test(add_numbers_with_real_and_imaginary_part) :- add((1,2), (3,4), (X,Y)), X =:= 4, Y =:= 6.

    test(subtract_purely_real_numbers) :- sub((1,0), (2,0), (X,Y)), X =:= -1, Y =:= 0.

    test(subtract_purely_imaginary_numbers) :- sub((0,1), (0,2), (X,Y)), X =:= 0, Y =:= -1.

    test(subtract_numbers_with_real_and_imaginary_part) :- sub((1,2), (3,4), (X,Y)), X =:= -2, Y =:= -2.

    test(multiply_purely_real_numbers) :- mul((1,0), (2,0), (X,Y)), X =:= 2, Y =:= 0.

    test(multiply_purely_imaginary_numbers) :- mul((0,1), (0,2), (X,Y)), X =:= -2, Y =:= 0.

    test(multiply_numbers_with_real_and_imaginary_part) :- mul((1,2), (3,4), (X,Y)), X =:= -5, Y =:= 10.

    test(divide_purely_real_numbers) :- div((1,0), (2,0), (X,Y)), X =:= 0.5, Y =:= 0.

    test(divide_purely_imaginary_numbers) :- div((0,1), (0,2), (X,Y)), X =:= 0.5, Y =:= 0.

    test(divide_numbers_with_real_and_imaginary_part) :- div((1,2), (3,4), (X,Y)), X =:= 0.44, Y =:= 0.08.

    test(absolute_value_of_a_positive_purely_real_number) :- abs((5,0), R), R =:= 5.

    test(absolute_value_of_a_negative_purely_real_number) :- abs((-5,0), R), R =:= 5.

    test(absolute_value_of_a_positive_purely_imaginary_number) :- abs((0,5), R), R =:= 5.

    test(absolute_value_of_a_negative_purely_real_number) :- abs((0,-5), R), R =:= 5.

    test(absolute_value_of_a_number_with_real_and_imaginary_part) :- abs((3,4), R), R =:= 5.

    test(absolute_value_of_larger_number_with_real_and_imaginary_part) :-  abs((68, 285), R), R =:= 293.

    test(conjugate_a_purely_real_number) :- conjugate((5,0), (X,Y)), X =:= 5, Y =:= 0.

    test(conjugate_a_purely_imaginary_number) :- conjugate((0,5), (X,Y)), X =:= 0, Y =:= -5 .

    test(conjugate_a_number_with_real_and_imaginary_part) :- conjugate((1,1), (X,Y)), X =:= 1, Y =:= -1.

:- end_tests(complex_numbers).
