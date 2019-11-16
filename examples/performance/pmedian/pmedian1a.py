#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright 2017 National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and 
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain 
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________


from pyomo.environ import *
from pyomo.core.expr.numeric_expr import X_LinearExpression


def pyomo_create_model(options=None, model_options=None):
    import random

    random.seed(1000)

    model = AbstractModel()

    model.N = Param(within=PositiveIntegers)

    model.Locations = RangeSet(1,model.N)

    model.P = Param(within=RangeSet(1,model.N))

    model.M = Param(within=PositiveIntegers)

    model.Customers = RangeSet(1,model.M)

    model.d = Param(model.Locations, model.Customers, initialize=lambda n, m, model : random.uniform(1.0,2.0), within=Reals)

    model.x = Var(model.Locations, model.Customers, bounds=(0.0,1.0), initialize=0.0)

    model.y = Var(model.Locations, bounds=(0.0, 1.0), initialize=0.0)

    def rule(model):
        return X_LinearExpression(linear_coefs=[model.d[n,m] for n in model.Locations for m in model.Customers], linear_vars=[model.x[n,m] for n in model.Locations for m in model.Customers])
    model.obj = Objective(rule=rule)

    def rule(model, m):
        #return (sum( model.x[n,m] for n in model.Locations ), 1.0)
        return (X_LinearExpression(linear_coefs=[1 for n in model.Locations], linear_vars=[model.x[n,m] for n in model.Locations]), 1.0)
    model.single_x = Constraint(model.Customers, rule=rule)

    def rule(model, n,m):
        #return (X_LinearExpression(linear_coefs=(1 for n in model.Locations), linear_var=(model.x[n,m] for n in model.Locations))
        return (None, X_LinearExpression(linear_coefs=(1, -1), linear_vars=(model.x[n,m], model.y[n])), 0.0)
    model.bound_y = Constraint(model.Locations, model.Customers, rule=rule)

    def rule(model):
        #return (sum( model.y[n] for n in model.Locations ) - model.P, 0.0)
        return (X_LinearExpression(linear_coefs=[1 for n in model.Locations], linear_vars=[model.y[n] for n in model.Locations]), model.P.value)
    model.num_facilities = Constraint(rule=rule)

    return model
