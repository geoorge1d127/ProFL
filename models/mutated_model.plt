:- begin_tests(triangle).

    test(all_sides_are_equal) :- triangle(2, 2, 2, "equilateral").

    test(any_side_is_unequal, [fail]) :- triangle(2, 3, 2, "equilateral").

    test(no_sides_are_equal, [fail]) :- triangle(5, 4, 6, "equilateral").

    test(all_zero_sides_are_not_a_triangle, [fail]) :- triangle(0, 0, 0, "equilateral").

    test(all_sides_are_floats_and_equal) :- triangle((0.5), (0.5), (0.5), "equilateral").


    test(last_two_sides_equal) :- triangle(3, 4, 4, "isosceles").

    test(first_two_sides_equal) :- triangle(4, 4, 3, "isosceles").

    test(first_and_last_sides_equal) :- triangle(4, 3, 4, "isosceles").

    test(equilateral_triangles_are_also_isosceles) :- triangle(4, 4, 4, "isosceles").

    test(no_sides_are_equal, [fail]) :- triangle(2, 3, 4, "isosceles").

    test(first_triangle_inequality_violation, [fail]) :- triangle(1, 1, 3, "isosceles").

    test(second_triangle_inequality_violation, [fail]) :- triangle(1, 3, 1, "isosceles").

    test(third_triangle_inequality_violation, [fail]) :- triangle(3, 1, 1, "isosceles").

    test(sides_may_be_floats) :- triangle((0.5), (0.4), (0.5), "isosceles").

    test(no_sides_are_equal) :- triangle(5, 4, 6, "scalene").

    test(all_sides_are_equal, [fail]) :- triangle(4, 4, 4, "scalene").

    test(two_sides_are_equal, [fail]) :- triangle(4, 4, 3, "scalene").

    test(may_not_violate_triangle_inequality, [fail]) :- triangle(7, 3, 2, "scalene").

    test(small_scalene_triangle_with_floating_point_values) :- triangle((0.5), (0.4), (0.6), "scalene").

:- end_tests(triangle).
