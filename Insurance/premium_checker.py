import pandas as pd

def check_eis_premium(age):
    # Premium table last updated: 29/09/2024
    eis = pd.read_csv('eis_premium.csv')
    # Filter premium to applicable age band
    prem = eis[eis['Age']<=int(age)].iloc[-1,:]
    # Calculate cash component for main plan
    if prem['Preferred'] > prem['AWL']:
        prem['Preferred Cash'] = prem['Preferred'] - prem['AWL']
        prem['Preferred'] = prem['AWL']
    else:
        prem['Preferred Cash'] = 0
    if prem['Advantage'] > prem['AWL']:
        prem['Advantage Cash'] = prem['Advantage'] - prem['AWL']
        prem['Advantage'] = prem['AWL']
    else:
        prem['Advantage Cash'] = 0
    # Print out summary
    print(f'Annual Premiums as follows')
    print('-----------')
    print(f'Preferred: ${prem['Preferred']} CPFMA')
    if prem['Preferred Cash'] > 0:
        print(f'Preferred: ${prem['Preferred Cash']} cash')
    print(f'Deluxe Rider (5% copay): $${prem['Preferred Deluxe']} cash')
    print(f'Classic Rider (10% copay): $${prem['Preferred Classic']} cash')
    print('-----------')
    print(f'Advantage: ${prem['Advantage']} CPFMA')
    if prem['Preferred Cash'] > 0:
        print(f'Advantage: ${prem['Advantage Cash']} cash')
    print(f'Deluxe Rider (5% copay): $${prem['Advantage Deluxe']} cash')
    print(f'Classic Rider (10% copay): $${prem['Advantage Classic']} cash')
    print('-----------')
    print(prem)
    
def main():
    age = input(f'Age?')
    #age = 1
    check_eis_premium(age)

if __name__ == "__main__":
    main()