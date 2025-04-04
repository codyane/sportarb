import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure visualizations
plt.style.use('ggplot')
sns.set_palette("husl")

def generate_fake_ipl_matches(num_matches=100):
    """Generate theoretical IPL match odds with a tighter range for non-arbitrage."""
    matches = {}
    for i in range(1, num_matches + 1):
        matches[f"Match {i}"] = {
            "Team A": {
                "Bookmaker1": round(np.random.uniform(1.8, 2.2), 2),
                "Bookmaker2": round(np.random.uniform(1.8, 2.2), 2),
            },
            "Team B": {
                "Bookmaker1": round(np.random.uniform(1.8, 2.2), 2),
                "Bookmaker2": round(np.random.uniform(1.8, 2.2), 2),
            }
        }
    return matches

def calculate_arbitrage(match_data, investment=1000):
    """Calculate arbitrage opportunities and return team odds as well."""
    results = {}
    for team, odds in match_data.items():
        best_odds = max(odds.values())
        implied_prob = 1 / best_odds
        results[team] = {
            'best_odds': best_odds,
            'implied_prob': implied_prob
        }
    
    total_prob = sum(v['implied_prob'] for v in results.values())
    
    if total_prob < 1:
        stakes = {team: (investment * results[team]['implied_prob']) / total_prob 
                  for team in results}
        returns = {team: stakes[team] * results[team]['best_odds']
                   for team in results}
        profit = min(returns.values()) - investment
        
        return {
            'arbitrage': True,
            'total_prob': total_prob,
            'stakes': stakes,
            'profit': round(profit, 2),
            'returns': returns,
            'team_odds': {team: results[team]['best_odds'] for team in results}
        }
    return {
        'arbitrage': False,
        'team_odds': {team: results[team]['best_odds'] for team in results}
    }

def animate_profit_scatter(matches, investment=1000, delay=0.1):
    """
    Animate a scatter plot showing arbitrage profit per match (only matches with arbitrage).
    """
    arbitrage_results = []  # Holds data for matches with arbitrage
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for idx, (match_name, match_data) in enumerate(matches.items(), 1):
        result = calculate_arbitrage(match_data, investment)
        if result.get('arbitrage', False):
            arbitrage_results.append({
                'Match': match_name,
                'Profit': result['profit'],
                'Team A Odds': result['team_odds'].get('Team A', None),
                'Team B Odds': result['team_odds'].get('Team B', None)
            })
        
        ax.clear()
        if arbitrage_results:
            df = pd.DataFrame(arbitrage_results)
            sns.scatterplot(data=df, x='Match', y='Profit', ax=ax, s=100, color='blue')
            # Annotate points with team odds
            for i in range(df.shape[0]):
                label = f"A: {df['Team A Odds'][i]}\nB: {df['Team B Odds'][i]}"
                ax.text(df['Match'][i], df['Profit'][i], label, ha='center', va='bottom', fontsize=8)
            ax.set_title(f"Arbitrage Profit Scatter (Matches with arbitrage: {len(df)})")
            ax.axhline(y=0, color='black', linestyle='--')
            plt.setp(ax.get_xticklabels(), rotation=45)
        else:
            ax.set_title(f"Arbitrage Profit Scatter (No arbitrage found till match {idx})")
        
        plt.tight_layout()
        plt.pause(delay)
    
    plt.ioff()
    plt.show()

def animate_cumulative_profit(matches, investment=1000, delay=0.1):
    """
    Animate a line chart showing the cumulative profit across all matches.
    Every match is processed (if no arbitrage, profit is 0).
    """
    cumulative_profit = 0
    cumulative_profits = []
    match_numbers = []
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for idx, (match_name, match_data) in enumerate(matches.items(), 1):
        result = calculate_arbitrage(match_data, investment)
        profit = result.get('profit', 0)
        cumulative_profit += profit
        cumulative_profits.append(cumulative_profit)
        match_numbers.append(idx)
        
        ax.clear()
        ax.plot(match_numbers, cumulative_profits, marker='o', linestyle='-', color='green')
        ax.set_title(f"Cumulative Profit (After {idx} Matches)")
        ax.set_xlabel("Match Number")
        ax.set_ylabel("Cumulative Profit (₹)")
        ax.axhline(y=0, color='black', linestyle='--')
        if cumulative_profits:
            ax.text(idx, cumulative_profits[-1], f"₹{cumulative_profits[-1]:.2f}", fontsize=9, ha='right', va='bottom')
        
        plt.tight_layout()
        plt.pause(delay)
    
    plt.ioff()
    plt.show()

def animate_profit_distribution(matches, investment=1000, delay=0.1):
    """
    Animate a histogram of arbitrage profit distribution as matches are processed.
    Only matches with arbitrage contribute to the distribution.
    """
    profit_list = []
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for idx, (match_name, match_data) in enumerate(matches.items(), 1):
        result = calculate_arbitrage(match_data, investment)
        if result.get('arbitrage', False):
            profit_list.append(result['profit'])
        
        ax.clear()
        if profit_list:
            sns.histplot(profit_list, bins=15, kde=True, ax=ax, color='#2196F3')
            ax.axvline(x=np.mean(profit_list), color='red', label=f"Mean: ₹{np.mean(profit_list):.2f}")
            ax.legend()
            ax.set_title(f"Profit Distribution (After {idx} Matches)")
            ax.set_xlabel("Profit per Match (₹)")
        else:
            ax.set_title(f"Profit Distribution (No arbitrage found till match {idx})")
        
        plt.tight_layout()
        plt.pause(delay)
    
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    # Generate sample data for 100 IPL matches with a tighter odds range
    matches = generate_fake_ipl_matches(num_matches=100)
    
    print("\nAnimating arbitrage profit scatter plot...")
    animate_profit_scatter(matches, delay=0.1)
    
    print("\nAnimating cumulative profit line chart...")
    animate_cumulative_profit(matches, delay=0.1)
    
    print("\nAnimating profit distribution histogram...")
    animate_profit_distribution(matches, delay=0.1)
    
    # Detailed analysis for all matches (terminal output)
    print("\n" + "="*50)
    print("Detailed Analysis for All Matches:")
    print("="*50)
    arbitrage_matches = []
    total_profit = 0
    for match_name, match_data in matches.items():
        result = calculate_arbitrage(match_data)
        if result.get('arbitrage', False):
            arbitrage_matches.append({
                'Match': match_name,
                'Total Probability (%)': round(result['total_prob'] * 100, 2),
                'Guaranteed Profit (₹)': result['profit'],
                'Team A Odds': result['team_odds'].get('Team A', None),
                'Team B Odds': result['team_odds'].get('Team B', None)
            })
            total_profit += result['profit']
    
    if arbitrage_matches:
        df_analysis = pd.DataFrame(arbitrage_matches)
        print(df_analysis.to_string(index=False))
        print("\nTotal Guaranteed Profit across arbitrage opportunities: ₹{:.2f}".format(total_profit))
    else:
        print("No arbitrage opportunities found in any match.")
