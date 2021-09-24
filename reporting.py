

def report_counts(d: dict):
    """converts dict counts into printable report"""
    sorted_counts = sorted(d.items(), key=lambda x: x[1])
    print()
    print(f'STONKS MENTIONED (descending)')
    print( '-----------------------------')
    for stonk, count in sorted_counts:
        print(f'{stonk.ljust(9)} ({count})')


