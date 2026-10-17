"""Local critical-zero collisions in the frozen V13 analytic families.

No root is searched on import. These are numerical evaluators, not interval
existence/absence certificates. ``normalization_height`` supplies a positive,
constant multiplier. The default Hardy phase removes Gamma's small modulus,
and its first two phase derivatives are included explicitly. Never pass
derivative=2 to mpmath 1.3.0's dirichlet function:
only its first derivative is implemented. Second derivatives below use the
explicit Hurwitz formula instead.
"""
from __future__ import annotations

from dataclasses import dataclass
import mpmath as mp

from v640_racines import CHARACTER_INDICES, _phases, reconstruct_pair


def periodic_jet(table, s, order=2):
    """L,L',L'' from Hurwitz derivatives, with eight guard decimal digits.

    The optional order is 0, 1 or 2. The periodic table need not be a character.
    This formula is intended away from s=1, where pole cancellation should be
    evaluated separately rather than as a sum of infinite terms.
    """
    if order not in (0, 1, 2):
        raise ValueError("The implemented jet order is 0, 1 or 2")
    q = len(table)
    if q < 2:
        raise ValueError("A nontrivial periodic table is required")
    s = mp.mpc(s)
    if s == 1:
        raise ValueError("The Hurwitz jet does not handle pole cancellation at s=1")
    with mp.workdps(mp.mp.dps + 8):
        logarithm = mp.log(q)
        sums = [mp.mpc(0) for _ in range(order + 1)]
        for a in range(1, q + 1):
            weight = table[a % q]
            if not weight:
                continue
            values = [mp.zeta(s, (a, q), derivative=n) for n in range(order + 1)]
            sums[0] += weight * values[0]
            if order >= 1:
                sums[1] += weight * (values[1] - logarithm * values[0])
            if order == 2:
                sums[2] += weight * (values[2] - 2 * logarithm * values[1]
                                     + logarithm ** 2 * values[0])
        result = [value / mp.power(q, s) for value in sums]
    return tuple(+value for value in result)


@dataclass
class Family:
    """c_sigma(r)=cos(r)e_i + sigma sin(r)u for the frozen analytic u."""
    anchor_k: int
    side: str
    anchor_table: list
    direction_table: list
    direction: list
    phases: list
    digits: int
    normalization_height: object = 0
    normalization: str = "hardy"

    @property
    def sign(self):
        return 1 if self.side == "plus" else -1

    @property
    def scale(self):
        return mp.exp(mp.pi * abs(mp.mpf(self.normalization_height)) / 4)

    def evaluate(self, s, r):
        """Uncompleted F_sigma(s,r); operations use the caller's mp precision."""
        return (mp.cos(r) * mp.dirichlet(s, self.anchor_table)
                + self.sign * mp.sin(r) * mp.dirichlet(s, self.direction_table))

    def completed(self, t, r):
        """Holomorphic in t locally near the real critical-height axis."""
        s = mp.mpf(".5") + mp.j * t
        if self.normalization == "hardy":
            # Holomorphic continuation of P(t)/|P(t)| near a real t. Unlike
            # taking abs(P) for complex t, this is suitable for complex roots.
            factor = mp.exp((mp.loggamma(mp.mpf(".75") + mp.j * t / 2)
                             - mp.loggamma(mp.mpf(".75") - mp.j * t / 2)) / 2
                            + mp.j * t * mp.log(13 / mp.pi) / 2)
        else:
            factor = mp.power(13 / mp.pi, (s + 1) / 2) * mp.gamma((s + 1) / 2)
        return self.scale * factor * self.evaluate(s, r)

    def critical(self, r, t):
        """Real critical-line evaluation; use reality_defect to audit projection."""
        return self.completed(t, r).real

    def _part_jet(self, table, t, order=2):
        s = mp.mpf(".5") + mp.j * t
        values = periodic_jet(table, s, order)
        if self.normalization == "hardy":
            if mp.im(t):
                raise ValueError("Hardy part jets are for real critical heights")
            argument = mp.mpf(".75") + mp.j * t / 2
            theta = mp.im(mp.loggamma(argument)) + t * mp.log(13 / mp.pi) / 2
            factor = self.scale * mp.exp(mp.j * theta)
            theta_prime = (mp.re(mp.digamma(argument)) + mp.log(13 / mp.pi)) / 2
            result = [factor * values[0]]
            if order >= 1:
                result.append(mp.j * factor * (values[1] + theta_prime * values[0]))
            if order == 2:
                theta_second = -mp.im(mp.polygamma(1, argument)) / 4
                result.append(factor * (-values[2] - 2 * theta_prime * values[1]
                                       + (mp.j * theta_second - theta_prime ** 2) * values[0]))
            return tuple(result)
        factor = self.scale * mp.power(13 / mp.pi, (s + 1) / 2) * mp.gamma((s + 1) / 2)
        result = [factor * values[0]]
        if order >= 1:
            alpha = (mp.log(13 / mp.pi) + mp.digamma((s + 1) / 2)) / 2
            result.append(mp.j * factor * (values[1] + alpha * values[0]))
        if order == 2:
            beta = mp.polygamma(1, (s + 1) / 2) / 4
            result.append(-factor * (values[2] + 2 * alpha * values[1]
                                     + (alpha ** 2 + beta) * values[0]))
        return tuple(result)

    def parts(self, t, order=2):
        """Completed X_i,Y_u and t-jets; full complex values retained."""
        return (self._part_jet(self.anchor_table, t, order),
                self._part_jet(self.direction_table, t, order))

    def jet(self, r, t):
        """Return Hasse coefficients Z,Z_t,Z_tt/2 and unfolding derivatives."""
        x, y = self.parts(t, 2)
        cosine, sine, sign = mp.cos(r), mp.sin(r), self.sign
        complex_values = {
            "Z": cosine * x[0] + sign * sine * y[0],
            "Z_t": cosine * x[1] + sign * sine * y[1],
            "Z_tt": cosine * x[2] + sign * sine * y[2],
            "Z_r": -sine * x[0] + sign * cosine * y[0],
            "Z_rt": -sine * x[1] + sign * cosine * y[1],
        }
        result = {key: value.real for key, value in complex_values.items()}
        result["hasse_t2"] = result["Z_tt"] / 2
        result["reality_defect"] = max(abs(value.imag) for value in complex_values.values())
        result["interval_certification"] = False
        return result

    def wronskian(self, t):
        """W=X Y'-X'Y; necessary for every critical double collision."""
        x, y = self.parts(t, 1)
        return (x[0] * y[1] - x[1] * y[0]).real

    def radius_from_height(self, t):
        """Unique candidate in [0,pi); None if X=Y=0 numerically exactly.

        The caller must enforce its registered radius bounds and independently
        check Z=Z_t=0. A Wronskian zero alone is not a collision certificate.
        """
        x, y = self.parts(t, 0)
        a, b = x[0].real, self.sign * y[0].real
        if a == 0 and b == 0:
            return None
        return mp.atan2(-a, b) % mp.pi


def make_family(pair, side="plus", digits=80, normalization_height=0,
                normalization="hardy"):
    """Rebuild solely from the existing frozen anchor/radius/minor recipe."""
    if side not in ("plus", "minus"):
        raise ValueError("side must be plus or minus")
    if normalization not in ("hardy", "completed"):
        raise ValueError("normalization must be hardy or completed")
    with mp.workdps(digits):
        rebuilt = reconstruct_pair(pair, digits)
        phases, tables = _phases()
        anchor = CHARACTER_INDICES.index(int(pair["character_k"]))
        anchor_table = [phases[anchor] * value for value in tables[anchor]]
        direction_table = [sum(rebuilt["direction"][j] * phases[j] * tables[j][a]
                               for j in range(6)) for a in range(13)]
        return Family(int(pair["character_k"]), side, anchor_table,
                      direction_table, rebuilt["direction"], phases, digits,
                      mp.mpf(normalization_height), normalization)


def companion_form(z_r, z_tt, delta_r):
    """Second-jet model. mu here is linearized, not a prepared exact discriminant."""
    z_r, z_tt, delta_r = map(mp.mpf, (z_r, z_tt, delta_r))
    if z_r == 0 or z_tt == 0:
        raise ValueError("A transverse order-two collision needs Z_r Z_tt != 0")
    kappa = -2 * z_r / z_tt
    return {"kappa": kappa, "mu_linear": kappa * delta_r,
            "companion": mp.matrix([[0, 1], [kappa * delta_r, 0]]),
            "exact_prepared_discriminant": False}


def operator_certificate(mu):
    """Exact algebraic identities for real mu, with its local metric signature."""
    mu = mp.mpf(mu)
    h = mp.matrix([[0, 1], [mu, 0]])
    j = mp.matrix([[0, 1], [1, 0]])
    g = j * h
    return {"H": h, "J": j, "JH": g,
            "J_self_adjoint_residual": h.T * j - j * h,
            "G_self_adjoint_residual": h.T * g - g * h,
            "positive_metric": mu > 0,
            "signature": (2, 0, 0) if mu > 0 else (1, 1, 0) if mu < 0 else (1, 0, 1),
            "critical_real_branches": mu > 0,
            "off_line_pair": mu < 0,
            "collision": mu == 0,
            "global_RH_implication": False}
