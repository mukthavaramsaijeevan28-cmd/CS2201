def solve_cryptarithmetic():
    print("=" * 60)
    print("PROBLEM 4: Cryptarithmetic – SEND + MORE = MONEY")
    print("=" * 60)
    print("\n    S E N D")
    print("  + M O R E")
    print("  ---------")
    print("  M O N E Y\n")
  
    from itertools import permutations
 
    letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
 
    print("  Searching for solution...\n")
 
    for perm in permutations(range(10), 8):
        assign = dict(zip(letters, perm))
        S, E, N, D = assign['S'], assign['E'], assign['N'], assign['D']
        M, O, R, Y = assign['M'], assign['O'], assign['R'], assign['Y']
 
        # Leading digits cannot be 0
        if S == 0 or M == 0:
            continue
 
        SEND  = 1000*S + 100*E + 10*N + D
        MORE  = 1000*M + 100*O + 10*R + E
        MONEY = 10000*M + 1000*O + 100*N + 10*E + Y
 
        if SEND + MORE == MONEY:
            print(f"  Solution found!")
            print(f"\n  Letter assignments: {assign}")
            print(f"\n    {SEND}")
            print(f"  + {MORE}")
            print(f"  -----")
            print(f"  {MONEY}")
            print(f"\n  Verification: {SEND} + {MORE} = {MONEY}  ->  "
                  f"{'CORRECT' if SEND + MORE == MONEY else 'WRONG'}")
            return
 
    print("  No solution found.")
    print()


if __name__ == '__main__':
    solve_cryptarithmetic()
 