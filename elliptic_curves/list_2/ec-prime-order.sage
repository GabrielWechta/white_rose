def generatePrimeOrderCurve(field):
	primeOrderCurveNotGenerated = True
	while primeOrderCurveNotGenerated:
		a = field.random_element()
		b = field.random_element()
		determinant = 4*a^3+27*b^2
		if (determinant != 0):
			E = EllipticCurve(field, [a, b])
			curveOrder = E.cardinality('pari')
			primeOrderCurveNotGenerated = not is_pseudoprime(curveOrder)
	return (E, curveOrder)



def generateDomainParameters(bitLength):
	p = random_prime(2^bitLength-1,False,2^(bitLength-1))
	field = GF(p)
	E, curveOrder = generatePrimeOrderCurve(field)
	basePoint = E.random_element()
	checkResult = curveOrder*basePoint

	if (checkResult == E(0)):
		print(E)
		print('Order of the curve: {}'.format(curveOrder))
		print('Basepoint in normalized projective coordinates: {}'.format(basePoint))

	

