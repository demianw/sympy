from __future__ import print_function, division

from sympy.core import S, C, sympify, cacheit
from sympy.core.function import Function, ArgumentIndexError, _coeff_isneg

from sympy.functions.elementary.miscellaneous import sqrt

###############################################################################
########################### HYPERBOLIC FUNCTIONS ##############################
###############################################################################


class HyperbolicFunction(Function):
    """
    Base class for hyperbolic functions.

    See Also
    ========

    sinh, cosh, tanh, coth
    """

    unbranched = True


class sinh(HyperbolicFunction):
    r"""
    The hyperbolic sine function, `\frac{e^x - e^{-x}}{2}`.

    * sinh(x) -> Returns the hyperbolic sine of x

    See Also
    ========

    cosh, tanh, asinh
    """
    nargs = 1

    def fdiff(self, argindex=1):
        """
        Returns the first derivative of this function.
        """
        if argindex == 1:
            return cosh(self.args[0])
        else:
            raise ArgumentIndexError(self, argindex)

    def inverse(self, argindex=1):
        """
        Returns the inverse of this function.
        """
        return asinh

    @classmethod
    def eval(cls, arg):
        arg = sympify(arg)

        if arg.is_Number:
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Infinity:
                return S.Infinity
            elif arg is S.NegativeInfinity:
                return S.NegativeInfinity
            elif arg is S.Zero:
                return S.Zero
            elif arg.is_negative:
                return -cls(-arg)
        else:
            if arg is S.ComplexInfinity:
                return S.NaN

            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                return S.ImaginaryUnit * C.sin(i_coeff)
            else:
                if _coeff_isneg(arg):
                    return -cls(-arg)

            if arg.func == asinh:
                return arg.args[0]

            if arg.func == acosh:
                x = arg.args[0]
                return sqrt(x - 1) * sqrt(x + 1)

            if arg.func == atanh:
                x = arg.args[0]
                return x/sqrt(1 - x**2)

            if arg.func == acoth:
                x = arg.args[0]
                return 1/(sqrt(x - 1) * sqrt(x + 1))

    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        """
        Returns the next term in the Taylor series expansion.
        """
        if n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)

            if len(previous_terms) > 2:
                p = previous_terms[-2]
                return p * x**2 / (n*(n - 1))
            else:
                return x**(n) / C.factorial(n)

    def _eval_conjugate(self):
        return self.func(self.args[0].conjugate())

    def as_real_imag(self, deep=True, **hints):
        """
        Returns this function as a complex coordinate.
        """
        if self.args[0].is_real:
            if deep:
                hints['complex'] = False
                return (self.expand(deep, **hints), S.Zero)
            else:
                return (self, S.Zero)
        if deep:
            re, im = self.args[0].expand(deep, **hints).as_real_imag()
        else:
            re, im = self.args[0].as_real_imag()
        return (sinh(re)*C.cos(im), cosh(re)*C.sin(im))

    def _eval_expand_complex(self, deep=True, **hints):
        re_part, im_part = self.as_real_imag(deep=deep, **hints)
        return re_part + im_part*S.ImaginaryUnit

    def _eval_expand_trig(self, deep=True, **hints):
        if deep:
            arg = self.args[0].expand(deep, **hints)
        else:
            arg = self.args[0]
        x = None
        if arg.is_Add: # TODO, implement more if deep stuff here
            x, y = arg.as_two_terms()
        else:
            coeff, terms = arg.as_coeff_Mul(rational=True)
            if coeff is not S.One and coeff.is_Integer and terms is not S.One:
                x = terms
                y = (coeff - 1)*x
        if x is not None:
            return (sinh(x)*cosh(y) + sinh(y)*cosh(x)).expand(trig=True)
        return sinh(arg)

    def _eval_rewrite_as_exp(self, arg):
        return (C.exp(arg) - C.exp(-arg)) / 2

    def _eval_rewrite_as_cosh(self, arg):
        return -S.ImaginaryUnit*cosh(arg + S.Pi*S.ImaginaryUnit/2)

    def _eval_rewrite_as_tanh(self, arg):
        tanh_half = tanh(S.Half*arg)
        return 2*tanh_half/(1 - tanh_half**2)

    def _eval_rewrite_as_coth(self, arg):
        coth_half = coth(S.Half*arg)
        return 2*coth_half/(coth_half**2 - 1)

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if x in arg.free_symbols and C.Order(1, x).contains(arg):
            return S.One
        else:
            return self.func(arg)

    def _eval_is_real(self):
        return self.args[0].is_real

    def _eval_is_bounded(self):
        arg = self.args[0]
        if arg.is_imaginary:
            return True

    def _sage_(self):
        import sage.all as sage
        return sage.sinh(self.args[0]._sage_())


class cosh(HyperbolicFunction):
    r"""
    The hyperbolic cosine function, `\frac{e^x + e^{-x}}{2}`.

    * cosh(x) -> Returns the hyperbolic cosine of x

    See Also
    ========

    sinh, tanh, acosh
    """
    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return sinh(self.args[0])
        else:
            raise ArgumentIndexError(self, argindex)

    @classmethod
    def eval(cls, arg):
        arg = sympify(arg)

        if arg.is_Number:
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Infinity:
                return S.Infinity
            elif arg is S.NegativeInfinity:
                return S.Infinity
            elif arg is S.Zero:
                return S.One
            elif arg.is_negative:
                return cls(-arg)
        else:
            if arg is S.ComplexInfinity:
                return S.NaN

            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                return C.cos(i_coeff)
            else:
                if _coeff_isneg(arg):
                    return cls(-arg)

            if arg.func == asinh:
                return sqrt(1 + arg.args[0]**2)

            if arg.func == acosh:
                return arg.args[0]

            if arg.func == atanh:
                return 1/sqrt(1 - arg.args[0]**2)

            if arg.func == acoth:
                x = arg.args[0]
                return x/(sqrt(x - 1) * sqrt(x + 1))

    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n < 0 or n % 2 == 1:
            return S.Zero
        else:
            x = sympify(x)

            if len(previous_terms) > 2:
                p = previous_terms[-2]
                return p * x**2 / (n*(n - 1))
            else:
                return x**(n)/C.factorial(n)

    def _eval_conjugate(self):
        return self.func(self.args[0].conjugate())

    def as_real_imag(self, deep=True, **hints):
        if self.args[0].is_real:
            if deep:
                hints['complex'] = False
                return (self.expand(deep, **hints), S.Zero)
            else:
                return (self, S.Zero)
        if deep:
            re, im = self.args[0].expand(deep, **hints).as_real_imag()
        else:
            re, im = self.args[0].as_real_imag()

        return (cosh(re)*C.cos(im), sinh(re)*C.sin(im))

    def _eval_expand_complex(self, deep=True, **hints):
        re_part, im_part = self.as_real_imag(deep=deep, **hints)
        return re_part + im_part*S.ImaginaryUnit

    def _eval_expand_trig(self, deep=True, **hints):
        if deep:
            arg = self.args[0].expand(deep, **hints)
        else:
            arg = self.args[0]
        x = None
        if arg.is_Add: # TODO, implement more if deep stuff here
            x, y = arg.as_two_terms()
        else:
            coeff, terms = arg.as_coeff_Mul(rational=True)
            if coeff is not S.One and coeff.is_Integer and terms is not S.One:
                x = terms
                y = (coeff - 1)*x
        if x is not None:
            return (cosh(x)*cosh(y) + sinh(x)*sinh(y)).expand(trig=True)
        return cosh(arg)

    def _eval_rewrite_as_exp(self, arg):
        return (C.exp(arg) + C.exp(-arg)) / 2

    def _eval_rewrite_as_sinh(self, arg):
        return -S.ImaginaryUnit*sinh(arg + S.Pi*S.ImaginaryUnit/2)

    def _eval_rewrite_as_tanh(self, arg):
        tanh_half = tanh(S.Half*arg)**2
        return (1 + tanh_half)/(1 - tanh_half)

    def _eval_rewrite_as_coth(self, arg):
        coth_half = coth(S.Half*arg)**2
        return (coth_half + 1)/(coth_half - 1)

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if x in arg.free_symbols and C.Order(1, x).contains(arg):
            return S.One
        else:
            return self.func(arg)

    def _eval_is_real(self):
        return self.args[0].is_real

    def _eval_is_bounded(self):
        arg = self.args[0]
        if arg.is_imaginary:
            return True

    def _sage_(self):
        import sage.all as sage
        return sage.cosh(self.args[0]._sage_())


class tanh(HyperbolicFunction):
    r"""
    The hyperbolic tangent function, `\frac{\sinh(x)}{\cosh(x)}`.

    * tanh(x) -> Returns the hyperbolic tangent of x

    See Also
    ========

    sinh, cosh, atanh
    """
    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return S.One - tanh(self.args[0])**2
        else:
            raise ArgumentIndexError(self, argindex)

    def inverse(self, argindex=1):
        """
        Returns the inverse of this function.
        """
        return atanh

    @classmethod
    def eval(cls, arg):
        arg = sympify(arg)

        if arg.is_Number:
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Infinity:
                return S.One
            elif arg is S.NegativeInfinity:
                return S.NegativeOne
            elif arg is S.Zero:
                return S.Zero
            elif arg.is_negative:
                return -cls(-arg)
        else:
            if arg is S.ComplexInfinity:
                return S.NaN

            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                if _coeff_isneg(i_coeff):
                    return -S.ImaginaryUnit * C.tan(-i_coeff)
                return S.ImaginaryUnit * C.tan(i_coeff)
            else:
                if _coeff_isneg(arg):
                    return -cls(-arg)

            if arg.func == asinh:
                x = arg.args[0]
                return x/sqrt(1 + x**2)

            if arg.func == acosh:
                x = arg.args[0]
                return sqrt(x - 1) * sqrt(x + 1) / x

            if arg.func == atanh:
                return arg.args[0]

            if arg.func == acoth:
                return 1/arg.args[0]

    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)

            a = 2**(n + 1)

            B = C.bernoulli(n + 1)
            F = C.factorial(n + 1)

            return a*(a - 1) * B/F * x**n

    def _eval_conjugate(self):
        return self.func(self.args[0].conjugate())

    def as_real_imag(self, deep=True, **hints):
        if self.args[0].is_real:
            if deep:
                hints['complex'] = False
                return (self.expand(deep, **hints), S.Zero)
            else:
                return (self, S.Zero)
        if deep:
            re, im = self.args[0].expand(deep, **hints).as_real_imag()
        else:
            re, im = self.args[0].as_real_imag()
        denom = sinh(re)**2 + C.cos(im)**2
        return (sinh(re)*cosh(re)/denom, C.sin(im)*C.cos(im)/denom)

    def _eval_rewrite_as_exp(self, arg):
        neg_exp, pos_exp = C.exp(-arg), C.exp(arg)
        return (pos_exp - neg_exp)/(pos_exp + neg_exp)

    def _eval_rewrite_as_sinh(self, arg):
        return S.ImaginaryUnit*sinh(arg)/sinh(S.Pi*S.ImaginaryUnit/2 - arg)

    def _eval_rewrite_as_cosh(self, arg):
        return S.ImaginaryUnit*cosh(S.Pi*S.ImaginaryUnit/2 - arg)/cosh(arg)

    def _eval_rewrite_as_coth(self, arg):
        return 1/coth(arg)

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if x in arg.free_symbols and C.Order(1, x).contains(arg):
            return S.One
        else:
            return self.func(arg)

    def _eval_is_real(self):
        return self.args[0].is_real

    def _eval_is_bounded(self):
        arg = self.args[0]
        if arg.is_real:
            return True

    def _sage_(self):
        import sage.all as sage
        return sage.tanh(self.args[0]._sage_())


class coth(HyperbolicFunction):
    r"""
    The hyperbolic cotangent function, `\frac{\cosh(x)}{\sinh(x)}`.

    * coth(x) -> Returns the hyperbolic cotangent of x
    """
    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return -1/sinh(self.args[0])**2
        else:
            raise ArgumentIndexError(self, argindex)

    def inverse(self, argindex=1):
        """
        Returns the inverse of this function.
        """
        return acoth

    @classmethod
    def eval(cls, arg):
        arg = sympify(arg)

        if arg.is_Number:
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Infinity:
                return S.One
            elif arg is S.NegativeInfinity:
                return S.NegativeOne
            elif arg is S.Zero:
                return S.Zero
            elif arg.is_negative:
                return -cls(-arg)
        else:
            if arg is S.ComplexInfinity:
                return S.NaN

            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                if _coeff_isneg(i_coeff):
                    return S.ImaginaryUnit * C.cot(-i_coeff)
                return -S.ImaginaryUnit * C.cot(i_coeff)
            else:
                if _coeff_isneg(arg):
                    return -cls(-arg)

            if arg.func == asinh:
                x = arg.args[0]
                return sqrt(1 + x**2)/x

            if arg.func == acosh:
                x = arg.args[0]
                return x/(sqrt(x - 1) * sqrt(x + 1))

            if arg.func == atanh:
                return 1/arg.args[0]

            if arg.func == acoth:
                return arg.args[0]

    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n == 0:
            return 1 / sympify(x)
        elif n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)

            B = C.bernoulli(n + 1)
            F = C.factorial(n + 1)

            return 2**(n + 1) * B/F * x**n

    def _eval_conjugate(self):
        return self.func(self.args[0].conjugate())

    def as_real_imag(self, deep=True, **hints):
        if self.args[0].is_real:
            if deep:
                hints['complex'] = False
                return (self.expand(deep, **hints), S.Zero)
            else:
                return (self, S.Zero)
        if deep:
            re, im = self.args[0].expand(deep, **hints).as_real_imag()
        else:
            re, im = self.args[0].as_real_imag()
        denom = sinh(re)**2 + C.sin(im)**2
        return (sinh(re)*cosh(re)/denom, -C.sin(im)*C.cos(im)/denom)

    def _eval_rewrite_as_exp(self, arg):
        neg_exp, pos_exp = C.exp(-arg), C.exp(arg)
        return (pos_exp + neg_exp)/(pos_exp - neg_exp)

    def _eval_rewrite_as_sinh(self, arg):
        return -S.ImaginaryUnit*sinh(S.Pi*S.ImaginaryUnit/2 - arg)/sinh(arg)

    def _eval_rewrite_as_cosh(self, arg):
        return -S.ImaginaryUnit*cosh(arg)/cosh(S.Pi*S.ImaginaryUnit/2 - arg)

    def _eval_rewrite_as_tanh(self, arg):
        return 1/tanh(arg)

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if x in arg.free_symbols and C.Order(1, x).contains(arg):
            return S.One
        else:
            return self.func(arg)

    def _sage_(self):
        import sage.all as sage
        return sage.coth(self.args[0]._sage_())


###############################################################################
############################# HYPERBOLIC INVERSES #############################
###############################################################################

class asinh(Function):
    """
    The inverse hyperbolic sine function.

    * asinh(x) -> Returns the inverse hyperbolic sine of x

    See Also
    ========

    acosh, atanh, sinh
    """
    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return 1/sqrt(self.args[0]**2 + 1)
        else:
            raise ArgumentIndexError(self, argindex)

    @classmethod
    def eval(cls, arg):
        arg = sympify(arg)

        if arg.is_Number:
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Infinity:
                return S.Infinity
            elif arg is S.NegativeInfinity:
                return S.NegativeInfinity
            elif arg is S.Zero:
                return S.Zero
            elif arg is S.One:
                return C.log(sqrt(2) + 1)
            elif arg is S.NegativeOne:
                return C.log(sqrt(2) - 1)
            elif arg.is_negative:
                return -cls(-arg)
        else:
            if arg is S.ComplexInfinity:
                return S.ComplexInfinity

            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                return S.ImaginaryUnit * C.asin(i_coeff)
            else:
                if _coeff_isneg(arg):
                    return -cls(-arg)

    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)
            if len(previous_terms) >= 2 and n > 2:
                p = previous_terms[-2]
                return -p * (n - 2)**2/(n*(n - 1)) * x**2
            else:
                k = (n - 1) // 2
                R = C.RisingFactorial(S.Half, k)
                F = C.factorial(k)
                return (-1)**k * R / F * x**n / n

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if x in arg.free_symbols and C.Order(1, x).contains(arg):
            return arg
        else:
            return self.func(arg)

    def inverse(self, argindex=1):
        """
        Returns the inverse of this function.
        """
        return sinh

    def _sage_(self):
        import sage.all as sage
        return sage.asinh(self.args[0]._sage_())


class acosh(Function):
    """
    The inverse hyperbolic cosine function.

    * acosh(x) -> Returns the inverse hyperbolic cosine of x

    See Also
    ========

    asinh, atanh, cosh
    """
    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return 1/sqrt(self.args[0]**2 - 1)
        else:
            raise ArgumentIndexError(self, argindex)

    @classmethod
    def eval(cls, arg):
        arg = sympify(arg)

        if arg.is_Number:
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Infinity:
                return S.Infinity
            elif arg is S.NegativeInfinity:
                return S.Infinity
            elif arg is S.Zero:
                return S.Pi*S.ImaginaryUnit / 2
            elif arg is S.One:
                return S.Zero
            elif arg is S.NegativeOne:
                return S.Pi*S.ImaginaryUnit

        if arg.is_number:
            cst_table = {
                S.ImaginaryUnit: C.log(S.ImaginaryUnit*(1 + sqrt(2))),
                -S.ImaginaryUnit: C.log(-S.ImaginaryUnit*(1 + sqrt(2))),
                S.Half: S.Pi/3,
                -S.Half: 2*S.Pi/3,
                sqrt(2)/2: S.Pi/4,
                -sqrt(2)/2: 3*S.Pi/4,
                1/sqrt(2): S.Pi/4,
                -1/sqrt(2): 3*S.Pi/4,
                sqrt(3)/2: S.Pi/6,
                -sqrt(3)/2: 5*S.Pi/6,
                (sqrt(3) - 1)/sqrt(2**3): 5*S.Pi/12,
                -(sqrt(3) - 1)/sqrt(2**3): 7*S.Pi/12,
                sqrt(2 + sqrt(2))/2: S.Pi/8,
                -sqrt(2 + sqrt(2))/2: 7*S.Pi/8,
                sqrt(2 - sqrt(2))/2: 3*S.Pi/8,
                -sqrt(2 - sqrt(2))/2: 5*S.Pi/8,
                (1 + sqrt(3))/(2*sqrt(2)): S.Pi/12,
                -(1 + sqrt(3))/(2*sqrt(2)): 11*S.Pi/12,
                (sqrt(5) + 1)/4: S.Pi/5,
                -(sqrt(5) + 1)/4: 4*S.Pi/5
            }

            if arg in cst_table:
                if arg.is_real:
                    return cst_table[arg]*S.ImaginaryUnit
                return cst_table[arg]

        if arg is S.ComplexInfinity:
            return S.Infinity

        i_coeff = arg.as_coefficient(S.ImaginaryUnit)

        if i_coeff is not None:
            if _coeff_isneg(i_coeff):
                return S.ImaginaryUnit * C.acos(i_coeff)
            return S.ImaginaryUnit * C.acos(-i_coeff)
        else:
            if _coeff_isneg(arg):
                return -cls(-arg)

    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n == 0:
            return S.Pi*S.ImaginaryUnit / 2
        elif n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)
            if len(previous_terms) >= 2 and n > 2:
                p = previous_terms[-2]
                return p * (n - 2)**2/(n*(n - 1)) * x**2
            else:
                k = (n - 1) // 2
                R = C.RisingFactorial(S.Half, k)
                F = C.factorial(k)
                return -R / F * S.ImaginaryUnit * x**n / n

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if x in arg.free_symbols and C.Order(1, x).contains(arg):
            return arg
        else:
            return self.func(arg)

    def inverse(self, argindex=1):
        """
        Returns the inverse of this function.
        """
        return cosh

    def _sage_(self):
        import sage.all as sage
        return sage.acosh(self.args[0]._sage_())


class atanh(Function):
    """
    The inverse hyperbolic tangent function.

    * atanh(x) -> Returns the inverse hyperbolic tangent of x

    See Also
    ========

    asinh, acosh, tanh
    """
    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return 1/(1 - self.args[0]**2)
        else:
            raise ArgumentIndexError(self, argindex)

    @classmethod
    def eval(cls, arg):
        arg = sympify(arg)

        if arg.is_Number:
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Zero:
                return S.Zero
            elif arg is S.One:
                return S.Infinity
            elif arg is S.NegativeOne:
                return S.NegativeInfinity
            elif arg is S.Infinity:
                return -S.ImaginaryUnit * C.atan(arg)
            elif arg is S.NegativeInfinity:
                return S.ImaginaryUnit * C.atan(-arg)
            elif arg.is_negative:
                return -cls(-arg)
        else:
            if arg is S.ComplexInfinity:
                return S.NaN

            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                return S.ImaginaryUnit * C.atan(i_coeff)
            else:
                if _coeff_isneg(arg):
                    return -cls(-arg)

    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)
            return x**n / n

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if x in arg.free_symbols and C.Order(1, x).contains(arg):
            return arg
        else:
            return self.func(arg)

    def inverse(self, argindex=1):
        """
        Returns the inverse of this function.
        """
        return tanh

    def _sage_(self):
        import sage.all as sage
        return sage.atanh(self.args[0]._sage_())


class acoth(Function):
    """
    The inverse hyperbolic cotangent function.

    * acoth(x) -> Returns the inverse hyperbolic cotangent of x
    """
    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return 1/(1 - self.args[0]**2)
        else:
            raise ArgumentIndexError(self, argindex)

    @classmethod
    def eval(cls, arg):
        arg = sympify(arg)

        if arg.is_Number:
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Infinity:
                return S.Zero
            elif arg is S.NegativeInfinity:
                return S.Zero
            elif arg is S.Zero:
                return S.Pi*S.ImaginaryUnit / 2
            elif arg is S.One:
                return S.Infinity
            elif arg is S.NegativeOne:
                return S.NegativeInfinity
            elif arg.is_negative:
                return -cls(-arg)
        else:
            if arg is S.ComplexInfinity:
                return 0

            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                return -S.ImaginaryUnit * C.acot(i_coeff)
            else:
                if _coeff_isneg(arg):
                    return -cls(-arg)

    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n == 0:
            return S.Pi*S.ImaginaryUnit / 2
        elif n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)
            return x**n / n

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if x in arg.free_symbols and C.Order(1, x).contains(arg):
            return arg
        else:
            return self.func(arg)

    def inverse(self, argindex=1):
        """
        Returns the inverse of this function.
        """
        return coth

    def _sage_(self):
        import sage.all as sage
        return sage.acoth(self.args[0]._sage_())
