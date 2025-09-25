# Gaming Analytics Master Code - Simplified & Error-Free Version
# Online Gaming Behavior Analysis with Data Type Handling

from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# MongoDB Configuration
uri = "mongodb+srv://aftabshikalgar3425_db_user:0lJ6nOVqtHPqYVCw@dataset1.uxppyjf.mongodb.net/?retryWrites=true&w=majority"

class GamingAnalytics:
    def __init__(self):
        """Initialize MongoDB connection and load data once"""
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.db = self.client['my_database']
            self.collection = self.db['my_collection']
            self.data = None
            self.load_data()
        except Exception as e:
            print(f"Connection error: {e}")
            self.data = []
    
    def load_data(self):
        """Load all data from MongoDB into memory for faster analysis"""
        print("Loading data from MongoDB...")
        try:
            cursor = self.collection.find({})
            self.data = list(cursor)
            print(f"Loaded {len(self.data)} records successfully!")
        except Exception as e:
            print(f"Data loading error: {e}")
            self.data = []
    
    def safe_convert_to_float(self, value):
        """Safely convert value to float, return 0 if conversion fails"""
        try:
            if value is None or value == '' or value == 'null':
                return 0.0
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def safe_convert_to_int(self, value):
        """Safely convert value to int, return 0 if conversion fails"""
        try:
            if value is None or value == '' or value == 'null':
                return 0
            return int(float(value))  # Convert to float first, then int
        except (ValueError, TypeError):
            return 0
    
    def extract_fields(self, fields, data_types=None):
        """Extract specific fields from loaded data with type conversion"""
        result = {field: [] for field in fields}
        
        if not data_types:
            data_types = {field: 'float' for field in fields}
        
        for doc in self.data:
            valid_doc = True
            temp_values = {}
            
            # Check and convert all fields
            for field in fields:
                if field not in doc:
                    valid_doc = False
                    break
                
                if data_types.get(field) == 'int':
                    temp_values[field] = self.safe_convert_to_int(doc[field])
                elif data_types.get(field) == 'float':
                    temp_values[field] = self.safe_convert_to_float(doc[field])
                else:  # string
                    temp_values[field] = str(doc[field]) if doc[field] is not None else 'Unknown'
            
            if valid_doc:
                for field in fields:
                    result[field].append(temp_values[field])
        
        return result
    
    def scenario_1_age_gaming_intensity(self):
        """
        Scenario 1: Age vs Gaming Intensity Analysis
        Shows correlation between player age and gaming habits
        """
        print("\n=== SCENARIO 1: Age vs Gaming Intensity Analysis ===")
        
        fields = ['Age', 'PlayTimeHours', 'SessionsPerWeek', 'AvgSessionDurationMinutes']
        data_types = {'Age': 'int', 'PlayTimeHours': 'float', 'SessionsPerWeek': 'int', 'AvgSessionDurationMinutes': 'float'}
        data = self.extract_fields(fields, data_types)
        
        if len(data['Age']) < 10:
            print("Insufficient data for analysis")
            return
        
        # Create 2x2 subplot
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Age vs Gaming Intensity Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Age vs Play Time Scatter
        ax1.scatter(data['Age'], data['PlayTimeHours'], alpha=0.6, color='blue', s=30)
        ax1.set_xlabel('Player Age')
        ax1.set_ylabel('Total Play Time (Hours)')
        ax1.set_title('Age vs Play Time Correlation')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Age Distribution Histogram
        ax2.hist(data['Age'], bins=25, color='lightgreen', alpha=0.8, edgecolor='black')
        ax2.set_xlabel('Player Age')
        ax2.set_ylabel('Number of Players')
        ax2.set_title('Player Age Distribution')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Sessions per Week vs Age
        ax3.scatter(data['Age'], data['SessionsPerWeek'], alpha=0.6, color='red', s=30)
        ax3.set_xlabel('Player Age')
        ax3.set_ylabel('Gaming Sessions Per Week')
        ax3.set_title('Age vs Gaming Frequency')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Average Session Duration vs Age
        ax4.scatter(data['Age'], data['AvgSessionDurationMinutes'], alpha=0.6, color='purple', s=30)
        ax4.set_xlabel('Player Age')
        ax4.set_ylabel('Avg Session Duration (Minutes)')
        ax4.set_title('Age vs Session Length')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Statistical insights
        print(f"📊 Age Analysis Results:")
        print(f"   • Age range: {min(data['Age'])} - {max(data['Age'])} years")
        print(f"   • Average age: {np.mean(data['Age']):.1f} years")
        print(f"   • Average play time: {np.mean(data['PlayTimeHours']):.1f} hours")
        print(f"   • Average sessions per week: {np.mean(data['SessionsPerWeek']):.1f}")
        print(f"   • Average session duration: {np.mean(data['AvgSessionDurationMinutes']):.1f} minutes")
    
    def scenario_2_monetization_analysis(self):
        """
        Scenario 2: Player Spending and Engagement Analysis
        Shows relationship between spending and player engagement
        """
        print("\n=== SCENARIO 2: Player Spending & Engagement Analysis ===")
        
        fields = ['InGamePurchases', 'PlayerLevel', 'LoyaltyIndex', 'PlayTimeHours']
        data_types = {'InGamePurchases': 'float', 'PlayerLevel': 'int', 'LoyaltyIndex': 'float', 'PlayTimeHours': 'float'}
        data = self.extract_fields(fields, data_types)
        
        if len(data['InGamePurchases']) < 10:
            print("Insufficient data for analysis")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Player Monetization & Engagement Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Play Time vs Spending
        ax1.scatter(data['PlayTimeHours'], data['InGamePurchases'], alpha=0.6, color='green', s=30)
        ax1.set_xlabel('Play Time (Hours)')
        ax1.set_ylabel('In-Game Purchases ($)')
        ax1.set_title('Gaming Time vs Spending')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Player Level Distribution
        ax2.hist(data['PlayerLevel'], bins=30, color='orange', alpha=0.8, edgecolor='black')
        ax2.set_xlabel('Player Level')
        ax2.set_ylabel('Number of Players')
        ax2.set_title('Player Level Distribution')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Loyalty vs Spending
        ax3.scatter(data['LoyaltyIndex'], data['InGamePurchases'], alpha=0.6, color='purple', s=30)
        ax3.set_xlabel('Loyalty Index')
        ax3.set_ylabel('In-Game Purchases ($)')
        ax3.set_title('Player Loyalty vs Spending')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Spending Distribution
        spending_data = [x for x in data['InGamePurchases'] if x > 0]  # Only non-zero spenders
        if spending_data:
            ax4.hist(spending_data, bins=25, color='gold', alpha=0.8, edgecolor='black')
            ax4.set_xlabel('In-Game Purchases ($)')
            ax4.set_ylabel('Number of Players')
            ax4.set_title('Spending Distribution (Paying Players Only)')
        else:
            ax4.text(0.5, 0.5, 'No spending data available', ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title('Spending Distribution')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Statistical insights
        total_spenders = len([x for x in data['InGamePurchases'] if x > 0])
        total_players = len(data['InGamePurchases'])
        
        print(f"💰 Monetization Analysis Results:")
        print(f"   • Total players analyzed: {total_players}")
        print(f"   • Paying players: {total_spenders} ({(total_spenders/total_players)*100:.1f}%)")
        print(f"   • Average spending (all): ${np.mean(data['InGamePurchases']):.2f}")
        if total_spenders > 0:
            avg_paying = np.mean([x for x in data['InGamePurchases'] if x > 0])
            print(f"   • Average spending (paying players): ${avg_paying:.2f}")
        print(f"   • Average player level: {np.mean(data['PlayerLevel']):.1f}")
        print(f"   • Average loyalty index: {np.mean(data['LoyaltyIndex']):.1f}")
    
    def scenario_3_social_gaming_analysis(self):
        """
        Scenario 3: Social Behavior in Gaming
        Analyzes social interaction and community aspects
        """
        print("\n=== SCENARIO 3: Social Gaming Behavior Analysis ===")
        
        fields = ['SocialInteractionScore', 'TeamPlayerScore', 'SessionsPerWeek', 'PlayTimeHours']
        data_types = {'SocialInteractionScore': 'float', 'TeamPlayerScore': 'float', 'SessionsPerWeek': 'int', 'PlayTimeHours': 'float'}
        data = self.extract_fields(fields, data_types)
        
        if len(data['SocialInteractionScore']) < 10:
            print("Insufficient data for analysis")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Social Gaming Behavior Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Social Interaction vs Team Score
        ax1.scatter(data['SocialInteractionScore'], data['TeamPlayerScore'], alpha=0.6, color='blue', s=30)
        ax1.set_xlabel('Social Interaction Score')
        ax1.set_ylabel('Team Player Score')
        ax1.set_title('Social Interaction vs Teamwork')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Social Interaction Distribution
        ax2.hist(data['SocialInteractionScore'], bins=25, color='lightblue', alpha=0.8, edgecolor='black')
        ax2.set_xlabel('Social Interaction Score')
        ax2.set_ylabel('Number of Players')
        ax2.set_title('Social Interaction Distribution')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Gaming Frequency vs Social Score
        ax3.scatter(data['SessionsPerWeek'], data['SocialInteractionScore'], alpha=0.6, color='green', s=30)
        ax3.set_xlabel('Gaming Sessions Per Week')
        ax3.set_ylabel('Social Interaction Score')
        ax3.set_title('Gaming Frequency vs Social Interaction')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Team Player Score Distribution
        ax4.hist(data['TeamPlayerScore'], bins=25, color='coral', alpha=0.8, edgecolor='black')
        ax4.set_xlabel('Team Player Score')
        ax4.set_ylabel('Number of Players')
        ax4.set_title('Team Player Score Distribution')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        print(f"👥 Social Gaming Analysis Results:")
        print(f"   • Average social interaction score: {np.mean(data['SocialInteractionScore']):.2f}")
        print(f"   • Average team player score: {np.mean(data['TeamPlayerScore']):.2f}")
        print(f"   • High social players (score > 7): {len([x for x in data['SocialInteractionScore'] if x > 7])}")
        print(f"   • Strong team players (score > 15): {len([x for x in data['TeamPlayerScore'] if x > 15])}")
    
    def scenario_4_game_preferences(self):
        """
        Scenario 4: Game Genre and Difficulty Preferences
        Shows what types of games players prefer
        """
        print("\n=== SCENARIO 4: Game Preferences Analysis ===")
        
        fields = ['GameGenre', 'PlayerLevel', 'AchievementsUnlocked', 'PlayTimeHours']
        data_types = {'GameGenre': 'string', 'PlayerLevel': 'int', 'AchievementsUnlocked': 'int', 'PlayTimeHours': 'float'}
        data = self.extract_fields(fields, data_types)
        
        if len(data['GameGenre']) < 10:
            print("Insufficient data for analysis")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Game Preferences & Player Progression Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Genre Distribution
        genre_counts = Counter(data['GameGenre'])
        top_genres = dict(genre_counts.most_common(8))  # Top 8 genres
        
        ax1.bar(range(len(top_genres)), list(top_genres.values()), color='skyblue', edgecolor='black')
        ax1.set_xlabel('Game Genre')
        ax1.set_ylabel('Number of Players')
        ax1.set_title('Popular Game Genres')
        ax1.set_xticks(range(len(top_genres)))
        ax1.set_xticklabels(list(top_genres.keys()), rotation=45, ha='right')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Player Level vs Achievements
        ax2.scatter(data['PlayerLevel'], data['AchievementsUnlocked'], alpha=0.6, color='gold', s=30)
        ax2.set_xlabel('Player Level')
        ax2.set_ylabel('Achievements Unlocked')
        ax2.set_title('Player Progression vs Achievements')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Play Time by Top Genres
        genre_playtime = {}
        for i, genre in enumerate(data['GameGenre']):
            if genre in top_genres:
                if genre not in genre_playtime:
                    genre_playtime[genre] = []
                genre_playtime[genre].append(data['PlayTimeHours'][i])
        
        if genre_playtime:
            genre_avg_time = {genre: np.mean(times) for genre, times in genre_playtime.items()}
            ax3.bar(range(len(genre_avg_time)), list(genre_avg_time.values()), color='lightcoral', edgecolor='black')
            ax3.set_xlabel('Game Genre')
            ax3.set_ylabel('Average Play Time (Hours)')
            ax3.set_title('Average Play Time by Genre')
            ax3.set_xticks(range(len(genre_avg_time)))
            ax3.set_xticklabels(list(genre_avg_time.keys()), rotation=45, ha='right')
            ax3.grid(True, alpha=0.3)
        
        # Plot 4: Achievement Distribution
        ax4.hist(data['AchievementsUnlocked'], bins=25, color='lightgreen', alpha=0.8, edgecolor='black')
        ax4.set_xlabel('Achievements Unlocked')
        ax4.set_ylabel('Number of Players')
        ax4.set_title('Achievement Distribution')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        print(f"🎯 Game Preferences Analysis Results:")
        print(f"   • Most popular genre: {max(genre_counts, key=genre_counts.get)} ({genre_counts[max(genre_counts, key=genre_counts.get)]} players)")
        print(f"   • Average player level: {np.mean(data['PlayerLevel']):.1f}")
        print(f"   • Average achievements: {np.mean(data['AchievementsUnlocked']):.1f}")
        print(f"   • High achievers (>50 achievements): {len([x for x in data['AchievementsUnlocked'] if x > 50])}")
    
    def scenario_5_player_segments(self):
        """
        Scenario 5: Player Segmentation Analysis
        Segments players based on behavior patterns
        """
        print("\n=== SCENARIO 5: Player Segmentation Analysis ===")
        
        fields = ['PlayTimeHours', 'InGamePurchases', 'SessionsPerWeek', 'PlayerLevel']
        data_types = {'PlayTimeHours': 'float', 'InGamePurchases': 'float', 'SessionsPerWeek': 'int', 'PlayerLevel': 'int'}
        data = self.extract_fields(fields, data_types)
        
        if len(data['PlayTimeHours']) < 10:
            print("Insufficient data for analysis")
            return
        
        # Define segments based on play time and spending
        play_time_median = np.median(data['PlayTimeHours'])
        spending_median = np.median(data['InGamePurchases'])
        
        segments = []
        colors = []
        
        for i in range(len(data['PlayTimeHours'])):
            play_time = data['PlayTimeHours'][i]
            spending = data['InGamePurchases'][i]
            
            if play_time > play_time_median and spending > spending_median:
                segments.append('Heavy Spenders')
                colors.append('gold')
            elif play_time > play_time_median and spending <= spending_median:
                segments.append('Time Invested')
                colors.append('blue')
            elif play_time <= play_time_median and spending > spending_median:
                segments.append('Quick Spenders')
                colors.append('red')
            else:
                segments.append('Casual Players')
                colors.append('lightgray')
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Player Segmentation Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Segmentation Scatter Plot
        ax1.scatter(data['PlayTimeHours'], data['InGamePurchases'], c=colors, alpha=0.7, s=40)
        ax1.axhline(y=spending_median, color='black', linestyle='--', alpha=0.5, label='Spending Median')
        ax1.axvline(x=play_time_median, color='black', linestyle='--', alpha=0.5, label='Time Median')
        ax1.set_xlabel('Play Time (Hours)')
        ax1.set_ylabel('In-Game Purchases ($)')
        ax1.set_title('Player Segments (Time vs Spending)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Segment Distribution
        segment_counts = Counter(segments)
        ax2.pie(segment_counts.values(), labels=segment_counts.keys(), autopct='%1.1f%%', startangle=90)
        ax2.set_title('Player Segment Distribution')
        
        # Plot 3: Sessions per Week by Segment
        segment_sessions = {}
        for i, segment in enumerate(segments):
            if segment not in segment_sessions:
                segment_sessions[segment] = []
            segment_sessions[segment].append(data['SessionsPerWeek'][i])
        
        segment_avg_sessions = {seg: np.mean(sessions) for seg, sessions in segment_sessions.items()}
        ax3.bar(range(len(segment_avg_sessions)), list(segment_avg_sessions.values()), 
                color=['gold', 'blue', 'red', 'lightgray'])
        ax3.set_xlabel('Player Segment')
        ax3.set_ylabel('Average Sessions per Week')
        ax3.set_title('Gaming Frequency by Segment')
        ax3.set_xticks(range(len(segment_avg_sessions)))
        ax3.set_xticklabels(list(segment_avg_sessions.keys()), rotation=45, ha='right')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Player Level by Segment
        segment_levels = {}
        for i, segment in enumerate(segments):
            if segment not in segment_levels:
                segment_levels[segment] = []
            segment_levels[segment].append(data['PlayerLevel'][i])
        
        segment_avg_levels = {seg: np.mean(levels) for seg, levels in segment_levels.items()}
        ax4.bar(range(len(segment_avg_levels)), list(segment_avg_levels.values()), 
                color=['gold', 'blue', 'red', 'lightgray'])
        ax4.set_xlabel('Player Segment')
        ax4.set_ylabel('Average Player Level')
        ax4.set_title('Player Level by Segment')
        ax4.set_xticks(range(len(segment_avg_levels)))
        ax4.set_xticklabels(list(segment_avg_levels.keys()), rotation=45, ha='right')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        print(f"🎮 Player Segmentation Results:")
        for segment, count in segment_counts.items():
            avg_spending = np.mean([data['InGamePurchases'][i] for i, s in enumerate(segments) if s == segment])
            avg_time = np.mean([data['PlayTimeHours'][i] for i, s in enumerate(segments) if s == segment])
            percentage = (count / len(segments)) * 100
            print(f"   • {segment}: {count} players ({percentage:.1f}%) - Avg: ${avg_spending:.2f}, {avg_time:.1f}h")
    
    def display_menu(self):
        """Display the main menu for scenario selection"""
        print("\n" + "="*70)
        print("🎮 GAMING ANALYTICS - Online Gaming Behavior Analysis 🎮")
        print("="*70)
        print("Choose a scenario for analysis:")
        print("1. 📊 Age vs Gaming Intensity Analysis")
        print("2. 💰 Player Spending & Engagement Analysis")
        print("3. 👥 Social Gaming Behavior Analysis")
        print("4. 🎯 Game Preferences & Progression Analysis")
        print("5. 🏷️  Player Segmentation Analysis")
        print("6. Exit")
        print("-"*70)
    
    def run_analysis(self):
        """Main function to run the interactive analysis"""
        if not self.data:
            print("❌ No data available. Please check your MongoDB connection.")
            return
        
        while True:
            self.display_menu()
            
            try:
                choice = input("Enter your choice (1-6): ").strip()
                
                if choice == '1':
                    self.scenario_1_age_gaming_intensity()
                elif choice == '2':
                    self.scenario_2_monetization_analysis()
                elif choice == '3':
                    self.scenario_3_social_gaming_analysis()
                elif choice == '4':
                    self.scenario_4_game_preferences()
                elif choice == '5':
                    self.scenario_5_player_segments()
                elif choice == '6':
                    print("🎮 Thank you for using Gaming Analytics! Have a great day! 🎮")
                    break
                else:
                    print("❌ Invalid choice. Please enter a number between 1-6.")
                
                input("\n✅ Press Enter to continue to main menu...")
                
            except KeyboardInterrupt:
                print("\n👋 Exiting Gaming Analytics...")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")
    
    def close_connection(self):
        """Safely close MongoDB connection"""
        try:
            if hasattr(self, 'client'):
                self.client.close()
        except:
            pass  # Ignore errors during cleanup

# Main execution
if __name__ == "__main__":
    print("🚀 Starting Gaming Analytics System...")
    analyzer = GamingAnalytics()
    
    try:
        analyzer.run_analysis()
    finally:
        analyzer.close_connection()
        print("Connection closed successfully!")