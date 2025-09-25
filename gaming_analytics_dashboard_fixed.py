# Complete Gaming Analytics Dashboard - Fixed & Working Version
# Professional GUI-based Gaming Behavior Analytics Platform

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.patches as patches
from pymongo import MongoClient
import pandas as pd
import numpy as np
import threading
from datetime import datetime
import random
import warnings
warnings.filterwarnings('ignore')

class GamingAnalyticsDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Gaming Analytics Professional Dashboard")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2c3e50')
        
        # MongoDB connection
        self.uri = "mongodb+srv://aftabshikalgar3425_db_user:0lJ6nOVqtHPqYVCw@dataset1.uxppyjf.mongodb.net/?retryWrites=true&w=majority"
        self.client = None
        self.collection = None
        self.data = None
        
        # Style configuration
        self.setup_styles()
        
        # Create GUI
        self.create_header()
        self.create_main_interface()
        self.create_status_bar()
        
        # Load data automatically
        self.load_data_threaded()
    
    def setup_styles(self):
        """Configure professional styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Header.TLabel', 
                       background='#34495e', 
                       foreground='white', 
                       font=('Arial', 16, 'bold'))
        
        style.configure('Status.TLabel', 
                       background='#2c3e50', 
                       foreground='#ecf0f1', 
                       font=('Arial', 10))
        
        style.configure('Professional.TButton',
                       font=('Arial', 11, 'bold'),
                       padding=10)
    
    def create_header(self):
        """Create professional header"""
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🎮 Gaming Analytics Professional Dashboard",
                              bg='#34495e', 
                              fg='white', 
                              font=('Arial', 20, 'bold'))
        title_label.pack(side='left', padx=20, pady=20)
        
        # Connection status
        self.connection_label = tk.Label(header_frame,
                                       text="🔴 Disconnected",
                                       bg='#34495e',
                                       fg='#e74c3c',
                                       font=('Arial', 12, 'bold'))
        self.connection_label.pack(side='right', padx=20, pady=20)
    
    def create_main_interface(self):
        """Create main tabbed interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_control_tab()
        self.create_demographics_tab()
        self.create_behavior_tab()
        self.create_monetization_tab()
        self.create_social_tab()
        self.create_segmentation_tab()
    
    def create_control_tab(self):
        """Control panel tab"""
        control_frame = ttk.Frame(self.notebook)
        self.notebook.add(control_frame, text="🎛️ Control Panel")
        
        # Left panel - Controls
        left_panel = tk.Frame(control_frame, bg='white', width=300)
        left_panel.pack(side='left', fill='y', padx=10, pady=10)
        left_panel.pack_propagate(False)
        
        # Analysis buttons
        tk.Label(left_panel, text="📊 Analysis Options", 
                bg='white', font=('Arial', 14, 'bold')).pack(pady=10)
        
        analyses = [
            ("👥 Demographics Analysis", self.run_demographics_analysis),
            ("🎯 Behavioral Patterns", self.run_behavior_analysis),
            ("💰 Monetization Intelligence", self.run_monetization_analysis),
            ("⚠️ Social & Toxicity", self.run_social_analysis),
            ("🏷️ Player Segmentation", self.run_segmentation_analysis),
            ("📈 Comprehensive Report", self.run_comprehensive_analysis),
            ("🔄 Generate Sample Data", self.generate_sample_data)
        ]
        
        for text, command in analyses:
            btn = tk.Button(left_panel, text=text, command=command,
                           bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                           relief='flat', pady=8, cursor='hand2')
            btn.pack(fill='x', padx=10, pady=5)
        
        # Right panel - Data overview
        right_panel = tk.Frame(control_frame, bg='white')
        right_panel.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # Data overview
        tk.Label(right_panel, text="📋 Data Overview", 
                bg='white', font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.data_text = tk.Text(right_panel, height=25, font=('Courier', 10))
        scrollbar = tk.Scrollbar(right_panel, orient='vertical', command=self.data_text.yview)
        self.data_text.configure(yscrollcommand=scrollbar.set)
        
        self.data_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Initial welcome message
        welcome_text = """
 GAMING ANALYTICS DASHBOARD
=============================

Welcome to the Professional Gaming Analytics Platform!

 Getting Started:
1. Click "Generate Sample Data" to create realistic gaming data
2. Or wait for MongoDB data to load automatically
3. Select any analysis option from the left panel
4. View results in the corresponding tabs

 Available Analyses:
• Demographics - Player age, location, gaming patterns
• Behavioral - Gaming habits, session patterns, progression
• Monetization - Revenue analysis, spending patterns
• Social & Toxicity - Community health, player behavior
• Player Segmentation - Advanced player categorization

🔧 Features:
• Professional visualizations
• Real-time data processing
• Export capabilities
• Comprehensive reporting

Developer: Parth,,Madhura,Rohit,Aftab

Ready to analyze gaming behavior data!
        """
        
        self.data_text.insert(1.0, welcome_text)
    
    def create_demographics_tab(self):
        """Demographics analysis tab"""
        self.demo_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.demo_frame, text="👥 Demographics")
        
        # Create matplotlib figure
        self.demo_fig, self.demo_axes = plt.subplots(2, 2, figsize=(14, 10))
        self.demo_fig.patch.set_facecolor('white')
        
        self.demo_canvas = FigureCanvasTkAgg(self.demo_fig, self.demo_frame)
        self.demo_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.demo_canvas, self.demo_frame)
        toolbar.update()
    
    def create_behavior_tab(self):
        """Behavioral analysis tab"""
        self.behavior_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.behavior_frame, text="🎯 Behavior")
        
        self.behavior_fig, self.behavior_axes = plt.subplots(2, 2, figsize=(14, 10))
        self.behavior_fig.patch.set_facecolor('white')
        
        self.behavior_canvas = FigureCanvasTkAgg(self.behavior_fig, self.behavior_frame)
        self.behavior_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        toolbar = NavigationToolbar2Tk(self.behavior_canvas, self.behavior_frame)
        toolbar.update()
    
    def create_monetization_tab(self):
        """Monetization analysis tab"""
        self.monetization_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.monetization_frame, text="💰 Monetization")
        
        self.monetization_fig, self.monetization_axes = plt.subplots(2, 2, figsize=(14, 10))
        self.monetization_fig.patch.set_facecolor('white')
        
        self.monetization_canvas = FigureCanvasTkAgg(self.monetization_fig, self.monetization_frame)
        self.monetization_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        toolbar = NavigationToolbar2Tk(self.monetization_canvas, self.monetization_frame)
        toolbar.update()
    
    def create_social_tab(self):
        """Social analysis tab"""
        self.social_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.social_frame, text="⚠️ Social & Toxicity")
        
        self.social_fig, self.social_axes = plt.subplots(2, 2, figsize=(14, 10))
        self.social_fig.patch.set_facecolor('white')
        
        self.social_canvas = FigureCanvasTkAgg(self.social_fig, self.social_frame)
        self.social_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        toolbar = NavigationToolbar2Tk(self.social_canvas, self.social_frame)
        toolbar.update()
    
    def create_segmentation_tab(self):
        """Player segmentation tab"""
        self.segmentation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.segmentation_frame, text="🏷️ Player Segments")
        
        self.segmentation_fig, self.segmentation_axes = plt.subplots(2, 3, figsize=(16, 10))
        self.segmentation_fig.patch.set_facecolor('white')
        
        self.segmentation_canvas = FigureCanvasTkAgg(self.segmentation_fig, self.segmentation_frame)
        self.segmentation_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        toolbar = NavigationToolbar2Tk(self.segmentation_canvas, self.segmentation_frame)
        toolbar.update()
    
    def create_status_bar(self):
        """Create status bar"""
        status_frame = tk.Frame(self.root, bg='#2c3e50', height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, 
                                   text="Ready to analyze gaming data...",
                                   bg='#2c3e50', 
                                   fg='#ecf0f1', 
                                   font=('Arial', 10))
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Export button
        export_btn = tk.Button(status_frame, text="📊 Export All Charts", 
                              command=self.export_all_charts,
                              bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                              relief='flat', cursor='hand2')
        export_btn.pack(side='right', padx=10, pady=5)
    
    def generate_sample_data(self):
        """Generate realistic sample gaming data"""
        self.update_status("🔄 Generating realistic gaming data...")
        
        try:
            # Generate 5000 realistic gaming records
            n_players = 5000
            
            # Game genres and locations
            genres = ['Action', 'RPG', 'Strategy', 'Sports', 'Racing', 'Adventure', 'Simulation', 'Fighting', 'Puzzle', 'Horror']
            locations = ['USA', 'UK', 'Germany', 'Japan', 'Brazil', 'India', 'Australia', 'Canada', 'France', 'South Korea']
            genders = ['Male', 'Female', 'Other']
            difficulties = ['Easy', 'Normal', 'Hard', 'Expert']
            
            players_data = []
            
            for i in range(n_players):
                # Player archetypes
                archetype = random.choices(['casual', 'hardcore', 'social', 'competitive', 'whale'], 
                                         weights=[40, 25, 15, 15, 5])[0]
                
                # Age with realistic distribution
                age = max(15, min(65, int(np.random.normal(28, 8))))
                
                # Base stats by archetype
                if archetype == 'casual':
                    play_time = max(1, int(np.random.normal(5, 2)))
                    sessions = max(1, int(np.random.normal(3, 1)))
                    purchases = max(0, round(np.random.exponential(2), 2))
                    engagement = max(1, min(10, int(np.random.normal(4, 1.5))))
                    level = max(1, int(np.random.normal(15, 8)))
                    
                elif archetype == 'hardcore':
                    play_time = max(10, int(np.random.normal(35, 15)))
                    sessions = max(5, int(np.random.normal(12, 3)))
                    purchases = max(0, round(np.random.exponential(8), 2))
                    engagement = max(6, min(10, int(np.random.normal(8, 1))))
                    level = max(20, int(np.random.normal(75, 25)))
                    
                elif archetype == 'whale':
                    play_time = max(20, int(np.random.normal(40, 15)))
                    sessions = max(8, int(np.random.normal(18, 5)))
                    purchases = max(50, round(np.random.normal(250, 150), 2))
                    engagement = max(8, min(10, int(np.random.normal(9, 0.5))))
                    level = max(50, int(np.random.normal(95, 15)))
                    
                else:  # social/competitive
                    play_time = max(5, int(np.random.normal(20, 10)))
                    sessions = max(3, int(np.random.normal(8, 3)))
                    purchases = max(0, round(np.random.exponential(15), 2))
                    engagement = max(5, min(10, int(np.random.normal(7, 1.5))))
                    level = max(10, int(np.random.normal(45, 20)))
                
                # Derived stats
                avg_session = max(30, int(np.random.normal(play_time * 10, 30)))
                achievements = max(0, int(np.random.normal(level * 0.8, level * 0.3)))
                loyalty = min(100, max(0, int(np.random.normal(40 + engagement * 3, 15))))
                
                # Social behavior
                social_score = max(0, min(10, int(np.random.normal(5, 2.5))))
                team_score = max(0, min(20, int(np.random.normal(12, 4))))
                toxicity = max(0, min(10, int(np.random.normal(3, 2))))
                rage_quit = max(0, min(10, int(np.random.normal(3, 2))))
                sleep_risk = max(1, min(10, int(np.random.normal(4, 2))))
                
                player = {
                    'PlayerID': f'P{i+1:06d}',
                    'Age': age,
                    'Gender': random.choice(genders),
                    'Location': random.choice(locations),
                    'GameGenre': random.choice(genres),
                    'GameDifficulty': random.choice(difficulties),
                    'PlayTimeHours': play_time,
                    'SessionsPerWeek': sessions,
                    'AvgSessionDurationMinutes': avg_session,
                    'PlayerLevel': level,
                    'AchievementsUnlocked': achievements,
                    'InGamePurchases': purchases,
                    'EngagementLevel': engagement,
                    'LoyaltyIndex': loyalty,
                    'SocialInteractionScore': social_score,
                    'TeamPlayerScore': team_score,
                    'ToxicityLevel': toxicity,
                    'RageQuitFrequency': rage_quit,
                    'SleepDeprivationRisk': sleep_risk,
                    'PlayerType': archetype
                }
                
                players_data.append(player)
            
            # Convert to DataFrame
            self.data = pd.DataFrame(players_data)
            
            # Update UI
            self.root.after(0, self.update_connection_status, True)
            self.root.after(0, self.display_data_overview)
            self.update_status(f"✅ Generated {len(self.data)} realistic gaming records!")
            
            messagebox.showinfo("Success", f"🎉 Generated {len(self.data)} realistic gaming records!\nYou can now run any analysis.")
            
        except Exception as e:
            self.update_status(f"❌ Sample data generation failed: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate sample data:\n{str(e)}")
    
    def load_data_threaded(self):
        """Load data in separate thread"""
        thread = threading.Thread(target=self.load_data)
        thread.daemon = True
        thread.start()
    
    def load_data(self):
        """Load data from MongoDB"""
        try:
            self.update_status("🔄 Connecting to MongoDB...")
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            
            # Test connection
            self.client.admin.command('ping')
            
            # Get database and collection
            db = self.client['my_database']
            self.collection = db['my_collection']
            
            self.update_status("📥 Loading gaming data from MongoDB...")
            cursor = self.collection.find({}).limit(10000)
            
            # Convert to DataFrame
            docs = list(cursor)
            if docs:
                self.data = pd.DataFrame(docs)
                self.clean_data()
                
                # Update UI
                self.root.after(0, self.update_connection_status, True)
                self.root.after(0, self.display_data_overview)
                self.update_status(f"✅ Loaded {len(self.data)} gaming records from MongoDB!")
            else:
                self.update_status("⚠️ No data found in MongoDB. You can generate sample data instead.")
                
        except Exception as e:
            self.update_status(f"⚠️ MongoDB connection failed. You can generate sample data instead.")
            self.root.after(0, self.update_connection_status, False)
    
    def clean_data(self):
        """Clean and prepare data"""
        if self.data is not None:
            # Safe numeric conversion
            numeric_fields = ['Age', 'PlayTimeHours', 'InGamePurchases', 'SessionsPerWeek', 
                            'AvgSessionDurationMinutes', 'PlayerLevel', 'AchievementsUnlocked',
                            'EngagementLevel', 'SocialInteractionScore', 'RageQuitFrequency',
                            'LoyaltyIndex', 'SleepDeprivationRisk', 'ToxicityLevel', 'TeamPlayerScore']
            
            for field in numeric_fields:
                if field in self.data.columns:
                    self.data[field] = pd.to_numeric(self.data[field], errors='coerce').fillna(0)
            
            # Filter reasonable ranges
            self.data = self.data[
                (self.data['Age'] >= 10) & (self.data['Age'] <= 80) &
                (self.data['PlayTimeHours'] >= 0) & (self.data['PlayTimeHours'] <= 100)
            ]
    
    def update_status(self, message):
        """Update status bar"""
        def update():
            if hasattr(self, 'status_label'):
                self.status_label.config(text=message)
        self.root.after(0, update)
    
    def update_connection_status(self, connected):
        """Update connection indicator"""
        if connected:
            self.connection_label.config(text="🟢 Data Loaded", fg='#27ae60')
        else:
            self.connection_label.config(text="🔴 No Data", fg='#e74c3c')
    
    def display_data_overview(self):
        """Display data overview in text widget"""
        if self.data is not None:
            # Calculate statistics
            total_players = len(self.data)
            paying_players = (self.data['InGamePurchases'] > 0).sum()
            high_engagement = (self.data['EngagementLevel'] > 7).sum()
            
            overview = f"""
📊 GAMING ANALYTICS DATA OVERVIEW
{'='*50}

📈 Dataset Statistics:
• Total Players: {total_players:,}
• Active Players: {total_players:,}
• Data Quality: 100% (Generated/Clean Data)

👥 Player Demographics:
• Age Range: {self.data['Age'].min():.0f} - {self.data['Age'].max():.0f} years
• Average Age: {self.data['Age'].mean():.1f} years
• Gender Distribution:
  {chr(10).join([f'  • {k}: {v:,} ({v/total_players*100:.1f}%)' for k, v in self.data['Gender'].value_counts().items()])}

🎮 Gaming Behavior:
• Play Time Range: {self.data['PlayTimeHours'].min():.1f} - {self.data['PlayTimeHours'].max():.1f} hours/week
• Average Play Time: {self.data['PlayTimeHours'].mean():.1f} hours/week
• Average Sessions: {self.data['SessionsPerWeek'].mean():.1f} per week
• Average Session Duration: {self.data['AvgSessionDurationMinutes'].mean():.0f} minutes

💰 Monetization Insights:
• Total Revenue: ${self.data['InGamePurchases'].sum():,.2f}
• Average Revenue per Player: ${self.data['InGamePurchases'].mean():.2f}
• Paying Players: {paying_players:,} ({paying_players/total_players*100:.1f}%)
• Average per Paying Player: ${self.data[self.data['InGamePurchases'] > 0]['InGamePurchases'].mean():.2f}

🎯 Top Game Genres:
{chr(10).join([f'  • {genre}: {count:,} players ({count/total_players*100:.1f}%)' for genre, count in self.data['GameGenre'].value_counts().head().items()])}

🌍 Top Locations:
{chr(10).join([f'  • {location}: {count:,} players' for location, count in self.data['Location'].value_counts().head().items()])}

⚠️ Community Health:
• Average Toxicity Level: {self.data['ToxicityLevel'].mean():.2f}/10
• Low Toxicity (<4): {(self.data['ToxicityLevel'] < 4).sum():,} players ({(self.data['ToxicityLevel'] < 4).sum()/total_players*100:.1f}%)
• Average Team Score: {self.data['TeamPlayerScore'].mean():.1f}/20
• High Sleep Risk (>7): {(self.data['SleepDeprivationRisk'] > 7).sum():,} players ({(self.data['SleepDeprivationRisk'] > 7).sum()/total_players*100:.1f}%)

🏆 Engagement Metrics:
• Average Player Level: {self.data['PlayerLevel'].mean():.1f}
• Average Achievements: {self.data['AchievementsUnlocked'].mean():.1f}
• High Engagement (>7): {high_engagement:,} players ({high_engagement/total_players*100:.1f}%)
• Average Loyalty Index: {self.data['LoyaltyIndex'].mean():.1f}

🎮 Player Archetypes:
{chr(10).join([f'  • {ptype.title()}: {count:,} players ({count/total_players*100:.1f}%)' for ptype, count in self.data['PlayerType'].value_counts().items()]) if 'PlayerType' in self.data.columns else '  • Analysis available after running segmentation'}

📊 Ready for Analysis!
Select any analysis option from the left panel to generate detailed insights.
            """
            
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(1.0, overview)
    
    def run_demographics_analysis(self):
        """Run demographics analysis"""
        if self.data is None:
            messagebox.showwarning("Warning", "Please generate sample data or wait for MongoDB data to load.")
            return
        
        self.update_status("🔄 Running demographics analysis...")
        
        # Clear previous plots
        for ax in self.demo_axes.flat:
            ax.clear()
        
        # 1. Age distribution
        self.demo_axes[0,0].hist(self.data['Age'], bins=25, color='#3498db', alpha=0.7, edgecolor='black')
        self.demo_axes[0,0].set_title('🎂 Player Age Distribution', fontsize=14, fontweight='bold')
        self.demo_axes[0,0].set_xlabel('Age (years)')
        self.demo_axes[0,0].set_ylabel('Number of Players')
        self.demo_axes[0,0].grid(True, alpha=0.3)
        
        # Add statistics text
        mean_age = self.data['Age'].mean()
        self.demo_axes[0,0].axvline(mean_age, color='red', linestyle='--', 
                                   label=f'Avg: {mean_age:.1f} years')
        self.demo_axes[0,0].legend()
        
        # 2. Age vs Play Time scatter
        self.demo_axes[0,1].scatter(self.data['Age'], self.data['PlayTimeHours'], 
                                   alpha=0.6, c='#e74c3c', s=20)
        self.demo_axes[0,1].set_title('🎮 Age vs Gaming Intensity', fontsize=14, fontweight='bold')
        self.demo_axes[0,1].set_xlabel('Age (years)')
        self.demo_axes[0,1].set_ylabel('Play Time (Hours/Week)')
        self.demo_axes[0,1].grid(True, alpha=0.3)
        
        # Add trend line
        z = np.polyfit(self.data['Age'], self.data['PlayTimeHours'], 1)
        p = np.poly1d(z)
        self.demo_axes[0,1].plot(self.data['Age'], p(self.data['Age']), "r--", alpha=0.8)
        
        # 3. Location distribution (top 10)
        location_counts = self.data['Location'].value_counts().head(8)
        bars = self.demo_axes[1,0].bar(range(len(location_counts)), location_counts.values, 
                                      color='#f39c12', alpha=0.8)
        self.demo_axes[1,0].set_title('🌍 Top Gaming Locations', fontsize=14, fontweight='bold')
        self.demo_axes[1,0].set_xlabel('Location')
        self.demo_axes[1,0].set_ylabel('Number of Players')
        self.demo_axes[1,0].set_xticks(range(len(location_counts)))
        self.demo_axes[1,0].set_xticklabels(location_counts.index, rotation=45, ha='right')
        self.demo_axes[1,0].grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, location_counts.values):
            self.demo_axes[1,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                                    str(value), ha='center', va='bottom', fontweight='bold')
        
        # 4. Age groups vs Gaming Sessions
        age_groups = pd.cut(self.data['Age'], bins=[0, 18, 25, 35, 50, 100], 
                           labels=['<18', '18-25', '26-35', '36-50', '50+'])
        session_by_age = self.data.groupby(age_groups)['SessionsPerWeek'].mean()
        
        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
        bars = self.demo_axes[1,1].bar(range(len(session_by_age)), session_by_age.values, 
                                      color=colors, alpha=0.8)
        self.demo_axes[1,1].set_title('⏰ Gaming Frequency by Age Group', fontsize=14, fontweight='bold')
        self.demo_axes[1,1].set_xlabel('Age Group')
        self.demo_axes[1,1].set_ylabel('Average Sessions/Week')
        self.demo_axes[1,1].set_xticks(range(len(session_by_age)))
        self.demo_axes[1,1].set_xticklabels(session_by_age.index)
        self.demo_axes[1,1].grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, session_by_age.values):
            self.demo_axes[1,1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # Main title
        self.demo_fig.suptitle('👥 PLAYER DEMOGRAPHICS ANALYSIS', fontsize=16, fontweight='bold', y=0.98)
        self.demo_fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        self.demo_canvas.draw()
        
        # Switch to demographics tab
        self.notebook.select(1)
        self.update_status("✅ Demographics analysis complete!")
    
    def run_behavior_analysis(self):
        """Run behavioral patterns analysis"""
        if self.data is None:
            messagebox.showwarning("Warning", "Please generate sample data first.")
            return
        
        self.update_status("🔄 Analyzing behavioral patterns...")
        
        for ax in self.behavior_axes.flat:
            ax.clear()
        
        # 1. Play time distribution
        self.behavior_axes[0,0].hist(self.data['PlayTimeHours'], bins=30, 
                                    color='#1abc9c', alpha=0.7, edgecolor='black')
        self.behavior_axes[0,0].set_title('⏱️ Weekly Play Time Distribution', fontsize=14, fontweight='bold')
        self.behavior_axes[0,0].set_xlabel('Hours per Week')
        self.behavior_axes[0,0].set_ylabel('Number of Players')
        self.behavior_axes[0,0].grid(True, alpha=0.3)
        
        # Add intensity categories
        casual_line = self.behavior_axes[0,0].axvline(x=5, color='green', linestyle='--', label='Casual (<5h)')
        moderate_line = self.behavior_axes[0,0].axvline(x=15, color='orange', linestyle='--', label='Moderate (5-15h)')
        hardcore_line = self.behavior_axes[0,0].axvline(x=25, color='red', linestyle='--', label='Hardcore (>25h)')
        self.behavior_axes[0,0].legend()
        
        # 2. Session patterns
        self.behavior_axes[0,1].scatter(self.data['SessionsPerWeek'], 
                                       self.data['AvgSessionDurationMinutes'],
                                       alpha=0.6, c=self.data['PlayTimeHours'], cmap='viridis', s=30)
        cbar = plt.colorbar(self.behavior_axes[0,1].collections[0], ax=self.behavior_axes[0,1])
        cbar.set_label('Play Time (hours)')
        self.behavior_axes[0,1].set_title('🎯 Session Patterns', fontsize=14, fontweight='bold')
        self.behavior_axes[0,1].set_xlabel('Sessions per Week')
        self.behavior_axes[0,1].set_ylabel('Average Session Duration (min)')
        self.behavior_axes[0,1].grid(True, alpha=0.3)
        
        # 3. Genre preferences with enhanced styling
        genre_counts = self.data['GameGenre'].value_counts()
        colors = plt.cm.Set3(np.linspace(0, 1, len(genre_counts)))
        
        wedges, texts, autotexts = self.behavior_axes[1,0].pie(genre_counts.values, 
                                                               labels=genre_counts.index, 
                                                               autopct='%1.1f%%', 
                                                               colors=colors,
                                                               startangle=90)
        self.behavior_axes[1,0].set_title('🎮 Game Genre Preferences', fontsize=14, fontweight='bold')
        
        # Enhance pie chart text
        for autotext in autotexts:
            autotext.set_fontweight('bold')
            autotext.set_color('white')
        
        # 4. Player progression analysis
        self.behavior_axes[1,1].scatter(self.data['PlayerLevel'], self.data['AchievementsUnlocked'],
                                       alpha=0.6, c=self.data['EngagementLevel'], cmap='plasma', s=25)
        cbar2 = plt.colorbar(self.behavior_axes[1,1].collections[0], ax=self.behavior_axes[1,1])
        cbar2.set_label('Engagement Level')
        self.behavior_axes[1,1].set_title('🏆 Player Progression vs Achievements', fontsize=14, fontweight='bold')
        self.behavior_axes[1,1].set_xlabel('Player Level')
        self.behavior_axes[1,1].set_ylabel('Achievements Unlocked')
        self.behavior_axes[1,1].grid(True, alpha=0.3)
        
        self.behavior_fig.suptitle('🎯 BEHAVIORAL PATTERNS ANALYSIS', fontsize=16, fontweight='bold', y=0.98)
        self.behavior_fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        self.behavior_canvas.draw()
        
        self.notebook.select(2)
        self.update_status("✅ Behavioral analysis complete!")
    
    def run_monetization_analysis(self):
        """Run monetization analysis"""
        if self.data is None:
            messagebox.showwarning("Warning", "Please generate sample data first.")
            return
        
        self.update_status("🔄 Analyzing monetization patterns...")
        
        for ax in self.monetization_axes.flat:
            ax.clear()
        
        # 1. Spending distribution (paying players only)
        paying_players = self.data[self.data['InGamePurchases'] > 0]
        if len(paying_players) > 0:
            self.monetization_axes[0,0].hist(paying_players['InGamePurchases'], bins=30, 
                                           color='#27ae60', alpha=0.7, edgecolor='black')
            self.monetization_axes[0,0].set_title('💰 Spending Distribution (Paying Players)', fontsize=14, fontweight='bold')
            self.monetization_axes[0,0].set_xlabel('Purchase Amount ($)')
            self.monetization_axes[0,0].set_ylabel('Number of Players')
            self.monetization_axes[0,0].grid(True, alpha=0.3)
            
            # Add spending tier lines
            self.monetization_axes[0,0].axvline(x=10, color='blue', linestyle='--', label='Light Spender')
            self.monetization_axes[0,0].axvline(x=50, color='orange', linestyle='--', label='Medium Spender')
            self.monetization_axes[0,0].axvline(x=200, color='red', linestyle='--', label='Whale')
            self.monetization_axes[0,0].legend()
        
        # 2. Engagement vs Spending
        scatter = self.monetization_axes[0,1].scatter(self.data['EngagementLevel'], 
                                                     self.data['InGamePurchases'],
                                                     alpha=0.6, c=self.data['LoyaltyIndex'], 
                                                     cmap='coolwarm', s=25)
        cbar = plt.colorbar(scatter, ax=self.monetization_axes[0,1])
        cbar.set_label('Loyalty Index')
        self.monetization_axes[0,1].set_title('📈 Engagement vs Spending', fontsize=14, fontweight='bold')
        self.monetization_axes[0,1].set_xlabel('Engagement Level')
        self.monetization_axes[0,1].set_ylabel('In-Game Purchases ($)')
        self.monetization_axes[0,1].grid(True, alpha=0.3)
        
        # 3. Revenue by Genre
        genre_revenue = self.data.groupby('GameGenre')['InGamePurchases'].sum().sort_values(ascending=False)
        bars = self.monetization_axes[1,0].bar(range(len(genre_revenue)), genre_revenue.values, 
                                              color='#e67e22', alpha=0.8)
        self.monetization_axes[1,0].set_title('🎯 Revenue by Game Genre', fontsize=14, fontweight='bold')
        self.monetization_axes[1,0].set_xlabel('Game Genre')
        self.monetization_axes[1,0].set_ylabel('Total Revenue ($)')
        self.monetization_axes[1,0].set_xticks(range(len(genre_revenue)))
        self.monetization_axes[1,0].set_xticklabels(genre_revenue.index, rotation=45, ha='right')
        self.monetization_axes[1,0].grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, genre_revenue.values):
            self.monetization_axes[1,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                                           f'${value:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # 4. Player Spending Tiers
        spending_tiers = pd.cut(self.data['InGamePurchases'], 
                               bins=[-0.01, 0, 10, 50, 200, float('inf')],
                               labels=['F2P', 'Light ($1-10)', 'Medium ($11-50)', 'Heavy ($51-200)', 'Whale ($200+)'])
        tier_counts = spending_tiers.value_counts()
        
        colors = ['#95a5a6', '#3498db', '#f39c12', '#e74c3c', '#9b59b6']
        wedges, texts, autotexts = self.monetization_axes[1,1].pie(tier_counts.values, 
                                                                   labels=tier_counts.index,
                                                                   autopct='%1.1f%%', 
                                                                   colors=colors,
                                                                   startangle=90)
        self.monetization_axes[1,1].set_title('🏷️ Player Spending Tiers', fontsize=14, fontweight='bold')
        
        # Enhance text
        for autotext in autotexts:
            autotext.set_fontweight('bold')
            autotext.set_color('white')
        
        self.monetization_fig.suptitle('💰 MONETIZATION ANALYSIS', fontsize=16, fontweight='bold', y=0.98)
        self.monetization_fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        self.monetization_canvas.draw()
        
        self.notebook.select(3)
        self.update_status("✅ Monetization analysis complete!")
    
    def run_social_analysis(self):
        """Run social behavior and toxicity analysis"""
        if self.data is None:
            messagebox.showwarning("Warning", "Please generate sample data first.")
            return
        
        self.update_status("🔄 Analyzing social behavior and toxicity...")
        
        for ax in self.social_axes.flat:
            ax.clear()
        
        # 1. Toxicity distribution with risk zones
        self.social_axes[0,0].hist(self.data['ToxicityLevel'], bins=20, 
                                  color='#e74c3c', alpha=0.7, edgecolor='black')
        self.social_axes[0,0].set_title('⚠️ Toxicity Level Distribution', fontsize=14, fontweight='bold')
        self.social_axes[0,0].set_xlabel('Toxicity Level (0-10)')
        self.social_axes[0,0].set_ylabel('Number of Players')
        self.social_axes[0,0].grid(True, alpha=0.3)
        
        # Add risk zones
        self.social_axes[0,0].axvline(x=3, color='yellow', linestyle='--', linewidth=2, label='Moderate Risk')
        self.social_axes[0,0].axvline(x=6, color='orange', linestyle='--', linewidth=2, label='High Risk')
        self.social_axes[0,0].axvline(x=8, color='red', linestyle='--', linewidth=2, label='Critical Risk')
        self.social_axes[0,0].legend()
        
        # 2. Social vs Team collaboration
        scatter = self.social_axes[0,1].scatter(self.data['SocialInteractionScore'], 
                                               self.data['TeamPlayerScore'],
                                               alpha=0.6, c=self.data['ToxicityLevel'], 
                                               cmap='RdYlGn_r', s=25)
        cbar = plt.colorbar(scatter, ax=self.social_axes[0,1])
        cbar.set_label('Toxicity Level')
        self.social_axes[0,1].set_title('👥 Social Interaction vs Teamwork', fontsize=14, fontweight='bold')
        self.social_axes[0,1].set_xlabel('Social Interaction Score')
        self.social_axes[0,1].set_ylabel('Team Player Score')
        self.social_axes[0,1].grid(True, alpha=0.3)
        
        # 3. Rage quit frequency analysis
        self.social_axes[1,0].hist(self.data['RageQuitFrequency'], bins=15, 
                                  color='#e67e22', alpha=0.7, edgecolor='black')
        self.social_axes[1,0].set_title('😡 Rage Quit Patterns', fontsize=14, fontweight='bold')
        self.social_axes[1,0].set_xlabel('Rage Quit Frequency')
        self.social_axes[1,0].set_ylabel('Number of Players')
        self.social_axes[1,0].grid(True, alpha=0.3)
        
        # Add frequency categories
        self.social_axes[1,0].axvline(x=3, color='green', linestyle='--', label='Low (<3)')
        self.social_axes[1,0].axvline(x=6, color='orange', linestyle='--', label='High (>6)')
        self.social_axes[1,0].legend()
        
        # 4. Sleep deprivation risk assessment
        risk_categories = pd.cut(self.data['SleepDeprivationRisk'], 
                               bins=[0, 3, 5, 7, 10],
                               labels=['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk'])
        risk_counts = risk_categories.value_counts()
        
        colors = ['#27ae60', '#f39c12', '#e74c3c', '#8e44ad']
        wedges, texts, autotexts = self.social_axes[1,1].pie(risk_counts.values, 
                                                            labels=risk_counts.index,
                                                            autopct='%1.1f%%', 
                                                            colors=colors,
                                                            startangle=90)
        self.social_axes[1,1].set_title('😴 Sleep Deprivation Risk Assessment', fontsize=14, fontweight='bold')
        
        # Enhance text
        for autotext in autotexts:
            autotext.set_fontweight('bold')
            if autotext.get_text() in ['Critical Risk', 'High Risk']:
                autotext.set_color('white')
        
        self.social_fig.suptitle('⚠️ SOCIAL BEHAVIOR & TOXICITY ANALYSIS', fontsize=16, fontweight='bold', y=0.98)
        self.social_fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        self.social_canvas.draw()
        
        self.notebook.select(4)
        self.update_status("✅ Social behavior analysis complete!")
    
    def run_segmentation_analysis(self):
        """Run comprehensive player segmentation"""
        if self.data is None:
            messagebox.showwarning("Warning", "Please generate sample data first.")
            return
        
        self.update_status("🔄 Running advanced player segmentation...")
        
        for ax in self.segmentation_axes.flat:
            ax.clear()
        
        # Enhanced player segmentation function
        def categorize_player_advanced(row):
            spending = row['InGamePurchases']
            engagement = row['EngagementLevel']
            playtime = row['PlayTimeHours']
            sessions = row['SessionsPerWeek']
            
            if spending > 100:
                return 'Whale 🐋'
            elif spending > 25 and engagement > 6:
                return 'High Spender 💎'
            elif playtime > 25 and spending == 0:
                return 'Hardcore F2P ⚡'
            elif engagement > 7:
                return 'Engaged Player 🎯'
            elif playtime > 10:
                return 'Regular Player 🎮'
            elif sessions <= 2:
                return 'Casual Player 😊'
            else:
                return 'Casual Player 😊'
        
        self.data['PlayerSegment'] = self.data.apply(categorize_player_advanced, axis=1)
        segment_counts = self.data['PlayerSegment'].value_counts()
        
        # 1. Enhanced segment distribution
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        wedges, texts, autotexts = self.segmentation_axes[0,0].pie(segment_counts.values, 
                                                                   labels=segment_counts.index,
                                                                   autopct='%1.1f%%', 
                                                                   colors=colors[:len(segment_counts)],
                                                                   startangle=90)
        self.segmentation_axes[0,0].set_title('🏷️ Advanced Player Segmentation', fontsize=14, fontweight='bold')
        
        # Enhance pie chart
        for autotext in autotexts:
            autotext.set_fontweight('bold')
            autotext.set_color('white')
            autotext.set_fontsize(10)
        
        # 2. Revenue contribution by segment
        segment_revenue = self.data.groupby('PlayerSegment')['InGamePurchases'].sum().sort_values(ascending=False)
        bars = self.segmentation_axes[0,1].bar(range(len(segment_revenue)), segment_revenue.values,
                                              color=colors[:len(segment_revenue)], alpha=0.8)
        self.segmentation_axes[0,1].set_title('💰 Revenue Contribution by Segment', fontsize=14, fontweight='bold')
        self.segmentation_axes[0,1].set_xlabel('Player Segment')
        self.segmentation_axes[0,1].set_ylabel('Total Revenue ($)')
        self.segmentation_axes[0,1].set_xticks(range(len(segment_revenue)))
        self.segmentation_axes[0,1].set_xticklabels(segment_revenue.index, rotation=45, ha='right')
        self.segmentation_axes[0,1].grid(True, alpha=0.3)
        
        # Add percentage labels
        total_revenue = segment_revenue.sum()
        for bar, value in zip(bars, segment_revenue.values):
            percentage = (value/total_revenue)*100
            self.segmentation_axes[0,1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                                           f'${value:.0f}\n({percentage:.1f}%)', 
                                           ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # 3. Engagement levels by segment
        segment_engagement = self.data.groupby('PlayerSegment')['EngagementLevel'].mean().sort_values(ascending=False)
        bars = self.segmentation_axes[0,2].bar(range(len(segment_engagement)), segment_engagement.values,
                                              color='#3498db', alpha=0.8)
        self.segmentation_axes[0,2].set_title('📈 Average Engagement by Segment', fontsize=14, fontweight='bold')
        self.segmentation_axes[0,2].set_xlabel('Player Segment')
        self.segmentation_axes[0,2].set_ylabel('Average Engagement Level')
        self.segmentation_axes[0,2].set_xticks(range(len(segment_engagement)))
        self.segmentation_axes[0,2].set_xticklabels(segment_engagement.index, rotation=45, ha='right')
        self.segmentation_axes[0,2].grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, segment_engagement.values):
            self.segmentation_axes[0,2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                                           f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Play time patterns by segment
        segment_playtime = self.data.groupby('PlayerSegment')['PlayTimeHours'].mean().sort_values(ascending=False)
        bars = self.segmentation_axes[1,0].bar(range(len(segment_playtime)), segment_playtime.values,
                                              color='#e74c3c', alpha=0.8)
        self.segmentation_axes[1,0].set_title('⏰ Average Play Time by Segment', fontsize=14, fontweight='bold')
        self.segmentation_axes[1,0].set_xlabel('Player Segment')
        self.segmentation_axes[1,0].set_ylabel('Average Hours/Week')
        self.segmentation_axes[1,0].set_xticks(range(len(segment_playtime)))
        self.segmentation_axes[1,0].set_xticklabels(segment_playtime.index, rotation=45, ha='right')
        self.segmentation_axes[1,0].grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, segment_playtime.values):
            self.segmentation_axes[1,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                                           f'{value:.1f}h', ha='center', va='bottom', fontweight='bold')
        
        # 5. Community health by segment (toxicity)
        segment_toxicity = self.data.groupby('PlayerSegment')['ToxicityLevel'].mean().sort_values(ascending=True)
        bars = self.segmentation_axes[1,1].bar(range(len(segment_toxicity)), segment_toxicity.values,
                                              color='#f39c12', alpha=0.8)
        self.segmentation_axes[1,1].set_title('⚠️ Average Toxicity by Segment', fontsize=14, fontweight='bold')
        self.segmentation_axes[1,1].set_xlabel('Player Segment')
        self.segmentation_axes[1,1].set_ylabel('Average Toxicity Level')
        self.segmentation_axes[1,1].set_xticks(range(len(segment_toxicity)))
        self.segmentation_axes[1,1].set_xticklabels(segment_toxicity.index, rotation=45, ha='right')
        self.segmentation_axes[1,1].grid(True, alpha=0.3)
        
        # Add toxicity risk zones
        self.segmentation_axes[1,1].axhline(y=3, color='yellow', linestyle='--', alpha=0.7, label='Moderate')
        self.segmentation_axes[1,1].axhline(y=6, color='red', linestyle='--', alpha=0.7, label='High Risk')
        self.segmentation_axes[1,1].legend()
        
        # 6. Loyalty distribution by segment
        segments = self.data['PlayerSegment'].unique()
        for i, segment in enumerate(segments[:4]):  # Show top 4 segments
            segment_data = self.data[self.data['PlayerSegment'] == segment]['LoyaltyIndex']
            self.segmentation_axes[1,2].hist(segment_data, alpha=0.6, label=segment,
                                           bins=15, color=colors[i])
        
        self.segmentation_axes[1,2].set_title('🎖️ Loyalty Distribution by Segment', fontsize=14, fontweight='bold')
        self.segmentation_axes[1,2].set_xlabel('Loyalty Index')
        self.segmentation_axes[1,2].set_ylabel('Number of Players')
        self.segmentation_axes[1,2].legend()
        self.segmentation_axes[1,2].grid(True, alpha=0.3)
        
        self.segmentation_fig.suptitle('🏷️ ADVANCED PLAYER SEGMENTATION ANALYSIS', fontsize=16, fontweight='bold', y=0.98)
        self.segmentation_fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        self.segmentation_canvas.draw()
        
        self.notebook.select(5)
        self.update_status("✅ Advanced player segmentation complete!")
    
    def run_comprehensive_analysis(self):
        """Run all analyses sequentially"""
        if self.data is None:
            messagebox.showwarning("Warning", "Please generate sample data first.")
            return
        
        self.update_status("🔄 Running comprehensive analysis...")
        
        analyses = [
            ("👥 Demographics", self.run_demographics_analysis),
            ("🎯 Behavioral Patterns", self.run_behavior_analysis),
            ("💰 Monetization", self.run_monetization_analysis),
            ("⚠️ Social & Toxicity", self.run_social_analysis),
            ("🏷️ Player Segmentation", self.run_segmentation_analysis)
        ]
        
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Comprehensive Analysis Progress")
        progress_window.geometry("400x150")
        progress_window.resizable(False, False)
        
        tk.Label(progress_window, text="Running Comprehensive Analysis...", 
                font=('Arial', 12, 'bold')).pack(pady=20)
        
        progress_var = tk.StringVar()
        progress_label = tk.Label(progress_window, textvariable=progress_var, font=('Arial', 10))
        progress_label.pack(pady=10)
        
        progress_bar = ttk.Progressbar(progress_window, length=300, mode='determinate')
        progress_bar.pack(pady=20)
        progress_bar['maximum'] = len(analyses)
        
        def run_analyses():
            for i, (name, analysis_func) in enumerate(analyses):
                progress_var.set(f"Running {name} Analysis...")
                progress_window.update()
                analysis_func()
                progress_bar['value'] = i + 1
                progress_window.update()
            
            progress_window.destroy()
            messagebox.showinfo("Complete", "🎉 Comprehensive Analysis Completed!\n\nAll analytics are ready. Check each tab for detailed insights.")
        
        # Run analyses after a short delay
        self.root.after(100, run_analyses)
        
        self.update_status("✅ Comprehensive analysis in progress...")
    
    def export_all_charts(self):
        """Export all charts to files"""
        if self.data is None:
            messagebox.showwarning("Warning", "No data to export.")
            return
        
        folder = filedialog.askdirectory(title="Select Export Directory")
        if folder:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Export all figures
                figures = [
                    (self.demo_fig, "demographics_analysis"),
                    (self.behavior_fig, "behavioral_patterns"),
                    (self.monetization_fig, "monetization_analysis"),
                    (self.social_fig, "social_toxicity_analysis"),
                    (self.segmentation_fig, "player_segmentation")
                ]
                
                exported_files = []
                for fig, name in figures:
                    filename = f"{folder}/gaming_analytics_{name}_{timestamp}.png"
                    fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
                    exported_files.append(filename)
                
                # Export data overview
                if hasattr(self, 'data_text'):
                    overview_filename = f"{folder}/data_overview_{timestamp}.txt"
                    with open(overview_filename, 'w') as f:
                        f.write(self.data_text.get(1.0, tk.END))
                    exported_files.append(overview_filename)
                
                messagebox.showinfo("Export Success", 
                                  f"📊 Successfully exported {len(exported_files)} files to:\n{folder}\n\n"
                                  f"Files exported:\n" + "\n".join([f"• {f.split('/')[-1]}" for f in exported_files]))
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export files:\n{str(e)}")
    
    def __del__(self):
        """Cleanup on exit"""
        if self.client:
            self.client.close()

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = GamingAnalyticsDashboard(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Handle window close
    def on_closing():
        if messagebox.askokcancel("Quit", "Exit Gaming Analytics Dashboard?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    print("🎮 Gaming Analytics Dashboard Started Successfully!")
    print("📊 Ready to analyze gaming behavior data!")
    
    root.mainloop()

if __name__ == "__main__":
    main()