"""Validated periodic Dirichlet jets: explicit EM tail, elementary intervals only.

The analytic remainder is bounded by the periodic Bernoulli Fourier series,
then Cauchy's estimate. No interval zeta, Gamma, numerical differentiation or
floating-point character table is used. Backend: mpmath 1.3.0 iv primitives.
"""
from fractions import Fraction
from math import comb,factorial
import mpmath as mp
from v639_contraintes import exact_phases,minor_direction,conj,point,enclosure,endpoint_fraction

def lower(x):return endpoint_fraction(x._mpi_[0])
def upper(x):return endpoint_fraction(x._mpi_[1])
def interval(a,b):
    a,b=point(a),point(b)
    return mp.iv.make_mpf((a._mpi_[0],b._mpi_[1]))
def abs_upper(x):return max(abs(lower(x)),abs(upper(x)))
def magnitude(z):return mp.iv.sqrt(point(abs_upper(z.real))**2+point(abs_upper(z.imag))**2)
def symmetric(radius):return interval(-upper(radius),upper(radius))
def complex_exp(z):
    amplitude=mp.iv.exp(z.real)
    return amplitude*mp.iv.mpc(mp.iv.cos(z.imag),mp.iv.sin(z.imag))
def rounded_midpoint(x,places=12):
    q=(lower(x)+upper(x))/2;scaled=q*10**places
    integer=(scaled.numerator*2+scaled.denominator)//(2*scaled.denominator)
    return Fraction(integer,10**places)
def bernoulli(n):
    values=[Fraction(1)]
    for j in range(1,n+1):values.append(-sum(Fraction(comb(j+1,k))*values[k] for k in range(j))/(j+1))
    return values[n]
def serial(z,places=18):
    if hasattr(z,'_mpci_'):return {'real':enclosure(z.real,places),'imag':enclosure(z.imag,places)}
    return enclosure(z,places)

class IntervalFamily:
    def __init__(self,pair,side='plus',digits=50,N=32,M=12):
        if N<2 or M<1 or digits<30 or side not in ('plus','minus'):raise ValueError('Invalid interval plan')
        self.digits,self.N,self.M=digits,N,M
        self.sign=1 if side=='plus' else -1
        _,z=exact_phases(digits)
        indices=(1,3,5,7,9,11);anchor=indices.index(pair['character_k']);support=tuple(indices.index(k) for k in pair['support_character_k'])
        direction,p=minor_direction(z,anchor,support)
        if upper(p)<0:direction=[-x for x in direction]
        elif lower(p)<=0:raise ValueError('Minor orientation not separated from zero')
        dl={pow(2,j,13):j for j in range(12)};tables=[]
        for k in indices:
            tables.append([mp.iv.mpc(0)]+[mp.iv.mpc(mp.iv.cos(2*mp.iv.pi*point(Fraction((k*dl[a])%12,12))),mp.iv.sin(2*mp.iv.pi*point(Fraction((k*dl[a])%12,12)))) for a in range(1,13)])
        self.anchor=[z[anchor]*tables[anchor][a] for a in range(13)]
        self.direction=[sum((direction[j]*z[j]*tables[j][a] for j in range(6)),mp.iv.mpc(0)) for a in range(13)]
        self.logs={a:[mp.iv.log(point(13*n+a)) for n in range(N)] for a in range(1,13)}
        self.tail_logs={a:mp.iv.log(point(13*N+a)) for a in range(1,13)}
        self.tail_coefficients={a:[point(bernoulli(2*k)*Fraction(13**(2*k-1),factorial(2*k)*(13*N+a)**(2*k-1))) for k in range(1,M+1)] for a in range(1,13)}
        # A declared rectangle covering the complete planned contour and root boxes.
        self.domain=mp.iv.mpc(interval('0.29','0.71'),interval('4.65','5.08'))
        self.delta=point(Fraction(1,8));sigma=lower(self.domain.real)-Fraction(1,8)
        tau=abs_upper(self.domain.imag)+Fraction(1,8);sigma_high=upper(self.domain.real)+Fraction(1,8)
        product=point(1)
        for j in range(2*M):
            real_max=max(abs(sigma+j),abs(sigma_high+j))
            product*=mp.iv.sqrt(point(real_max)**2+point(tau)**2)
        # zeta(2M)<=1+1/(2M-1), by the integral test. All bases exceed one.
        c=2*(point(1)+point(Fraction(1,2*M-1)))/(2*mp.iv.pi)**(2*M)
        y=point(Fraction(N*13+1,13));decay=mp.iv.exp(point(1-sigma-2*M)*mp.iv.log(y))
        hurwitz=c*product*decay/point(sigma+2*M-1)
        scaling=mp.iv.exp(-point(sigma)*mp.iv.log(13))
        weights=[sum((magnitude(table[a]) for a in range(1,13)),point(0)) for table in (self.anchor,self.direction)]
        self.remainders=[[point(factorial(k))*hurwitz*scaling*w/self.delta**k for k in range(3)] for w in weights]

    def jets(self,s,order=2):
        if order not in (0,1,2):raise ValueError('Only analytic derivative orders 0..2 are implemented')
        s=mp.iv.mpc(s)
        if lower(s.real)<lower(self.domain.real) or upper(s.real)>upper(self.domain.real) or lower(s.imag)<lower(self.domain.imag) or upper(s.imag)>upper(self.domain.imag):raise ValueError('Outside the registered analytic remainder rectangle')
        rising={};p0=mp.iv.mpc(1);p1=p2=mp.iv.mpc(0)
        for j in range(2*self.M-1):
            factor=s+j;p0,p1,p2=p0*factor,p1*factor+p0,p2*factor+2*p1
            if (j+1)%2:rising[j+1]=(p0,p1,p2)
        result=[[mp.iv.mpc(0) for _ in range(order+1)] for _ in range(2)]
        for a in range(1,13):
            value=[mp.iv.mpc(0) for _ in range(order+1)]
            for L in self.logs[a]:
                e=complex_exp(-s*L);value[0]+=e
                if order>=1:value[1]-=L*e
                if order>=2:value[2]+=L*L*e
            L=self.tail_logs[a];e=complex_exp(-s*L);v=13*self.N+a;g=1/(s-1)
            value[0]+=e*(point(Fraction(v,13))*g+point(Fraction(1,2)))
            if order>=1:value[1]+=e*(point(Fraction(v,13))*(-g*g-L*g)-L/2)
            if order>=2:value[2]+=e*(point(Fraction(v,13))*(2*g**3+2*L*g*g+L*L*g)+L*L/2)
            for k,c in enumerate(self.tail_coefficients[a],1):
                p0,p1,p2=rising[2*k-1]
                value[0]+=c*e*p0
                if order>=1:value[1]+=c*e*(p1-L*p0)
                if order>=2:value[2]+=c*e*(p2-2*L*p1+L*L*p0)
            for family,table in zip(result,(self.anchor,self.direction)):
                for k in range(order+1):family[k]+=table[a]*value[k]
        for family,bounds in zip(result,self.remainders):
            for k in range(order+1):family[k]+=mp.iv.mpc(symmetric(bounds[k]),symmetric(bounds[k]))
        return result

    def function_jet(self,r,s,order=2):
        x,y=self.jets(s,order);c,d=mp.iv.cos(r),self.sign*mp.iv.sin(r)
        return [c*x[k]+d*y[k] for k in range(order+1)]

    def critical_system(self,r,t,omega=mp.iv.mpc(1)):
        x,y=self.jets(mp.iv.mpc(point(Fraction(1,2)),t),2)
        c,d=mp.iv.cos(r),self.sign*mp.iv.sin(r);cr,dr=-mp.iv.sin(r),self.sign*mp.iv.cos(r)
        f=[c*x[k]+d*y[k] for k in range(3)];fr=[cr*x[k]+dr*y[k] for k in range(2)]
        Hr=(omega*fr[0]).real;Ht=(omega*mp.iv.mpc(0,1)*f[1]).real
        Hrt=(omega*mp.iv.mpc(0,1)*fr[1]).real;Htt=-(omega*f[2]).real
        return {'values':[(omega*f[0]).real,Ht],'jacobian':[[Hr,Ht],[Hrt,Htt]],'anchor_projection':(omega*x[0]).real,'H_r':Hr,'H_tt':Htt}

def rational_inverse(matrix,places=12):
    a,b=map(lambda x:rounded_midpoint(x,places),matrix[0]);c,d=map(lambda x:rounded_midpoint(x,places),matrix[1]);det=a*d-b*c
    if not det:raise ValueError('Singular rational preconditioner')
    return [[d/det,-b/det],[-c/det,a/det]]

def contraction_certificate(centre,halfwidth,values,jacobian,preconditioner):
    C=[[point(q) for q in row] for row in preconditioner];B=[interval(q-halfwidth,q+halfwidth) for q in centre]
    remainder=[[point(1 if i==j else 0)-sum((C[i][k]*jacobian[k][j] for k in range(2)),point(0)) for j in range(2)] for i in range(2)]
    shift=[point(centre[i])-sum((C[i][k]*values[k] for k in range(2)),point(0)) for i in range(2)]
    K=[shift[i]+sum((remainder[i][j]*interval(-halfwidth,halfwidth) for j in range(2)),point(0)) for i in range(2)]
    q=max(sum(abs_upper(x) for x in row) for row in remainder)
    strict=all(lower(K[i])>centre[i]-halfwidth and upper(K[i])<centre[i]+halfwidth for i in range(2))
    determinant=jacobian[0][0]*jacobian[1][1]-jacobian[0][1]*jacobian[1][0]
    return {'accepted':strict and q<1,'strict_inclusion':strict,'contraction_upper':str(q),'K_intervals':K,'box_intervals':B,'jacobian_determinant':determinant,'preconditioner':preconditioner,'remainder_matrix':remainder}
