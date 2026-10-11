#!/usr/bin/env python3
"""Compute the expected answers for evals/calculation.md (K01, K02, K03, K05, K06)."""
import math

run_cost = 5_000_000
net_take = (5 - 1) / 10_000
k01 = run_cost / (12 * net_take)
print(f"K01 breakeven volume a month: USD {k01:,.0f}")

per_client = 0.30 * 100_000_000
k02 = math.ceil(k01 / per_client)
print(f"K02 clients: {k01 / per_client:.2f} -> {k02}")

f, c, r = 5, 1, 1
k03 = r / (f - c - r)
print(f"K03 extra volume for payback: {k03:.1%}")

balance, yld, share = 10_000_000, 0.04, 0.80
k05 = balance * yld * share
print(f"K05 income a year: USD {k05:,.0f}")

floor = 3_250_000
k06 = floor / (yld * share)
print(f"K06 balance for the floor: USD {k06:,.0f}")
