from proof_of_possession import Polynomial, get_Fr


def test_polynomials_point_calculation():
    coefficients = [get_Fr(2), get_Fr(0), get_Fr(1)]
    polynomial = Polynomial(coefficients=coefficients)
    print(polynomial(get_Fr(1)))


if __name__ == "__main__":
    test_polynomials_point_calculation()