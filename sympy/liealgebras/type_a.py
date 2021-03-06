from __future__ import print_function, division

from sympy.core import Set, Dict, Tuple
from sympy.liealgebras.cartan_type import Standard_Cartan, CartanType
from sympy.matrices import eye


class TypeA(Standard_Cartan):
    """
    This class contains the information about
    the A series of simple Lie algebras.
    ====
    """

    def __init__(self, n):
        assert n >= 1
        Standard_Cartan.__init__(self, "A", n)


    def dimension(self):
        """
        Return the dimension of the vector space
        V underlying the Lie algebra
        Example
        ========
        >>> from sympy.liealgebras.cartan_type import CartanType
        >>> c = CartanType("A4")
        >>> c.dimension()
        5
        """
        return self.n+1


    def basic_root(self, i, j):
        """
        This is a method just to generate roots
        with a 1 iin the ith position and a -1
        in the jth postion.

        """

        n = self.n
        root = [0]*(n+1)
        root[i] = 1
        root[j] = -1
        return root

    def simple_root(self, i):
        """
        Returns the ith simple root for the A series.

        Examples
        ========
        >>> from sympy.liealgebras.cartan_type import CartanType
        >>> c = CartanType("A4")
        >>> c.simple_root(1)
        [1, -1, 0, 0, 0]

        """

        return self.basic_root(i-1, i)

    def highest_root(self):
        """
        Returns the heighest weight root for A_n
        """

        return self.basic_root(0, self.n)

    def roots(self):
        """
        Returns the total number of roots for A_n
        """
        n = self.n
        return n*(n+1)

    def cartan_matrix(self):
        """
        Returns the Cartan matrix for A_n.
        The Cartan matrix matrix for a Lie algebra is
        generated by assigning an ordering to the simple
        roots, (alpha[1], ...., alpha[l]).  Then the ijth
        entry of the Cartan matrix is (<alpha[i],alpha[j]>).

        Example
        =======
        >>> from sympy.liealgebras.cartan_type import CartanType
        >>> c = CartanType('A4')
        >>> c.cartan_matrix()
        Matrix([
        [ 2, -1,  0,  0],
        [-1,  2, -1,  0],
        [ 0, -1,  2, -1],
        [ 0,  0, -1,  2]])

        """

        n = self.n
        m = 2 * eye(n)
        i = 1
        while i < n-1:
            m[i, i+1] = -1
            m[i, i-1] = -1
            i += 1
        m[0,1] = -1
        m[n-1, n-2] = -1
        return m

    def basis(self):
        """
        Returns the number of independent generators of A_n
        """
        n = self.n
        return n**2 - 1

    def lie_algebra(self):
        """
        Returns the Lie algebra associated with A_n
        """
        n = self.n
        return "su(" + str(n + 1) + ")"

    def dynkin_diagram(self):
        n = self.n
        diag = "---".join("0" for i in range(1, n+1)) + "\n"
        diag += "   ".join(str(i) for i in range(1, n+1))
        return diag
