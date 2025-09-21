Rivixo - Mood-Based Music Discovery App
A unique music discovery application that suggests songs based on your current mood! Built with Python and Tkinter, Rivixo helps you find the perfect soundtrack for any emotional state.

🎵 What is Rivixo?
Rivixo is a desktop application that connects your emotional state with personalized music recommendations. Instead of browsing through endless playlists, simply rate your mood on a scale of 1-10, and Rivixo will instantly suggest a song that matches your vibe.

✨ Key Features
Mood-Based Recommendations: Get song suggestions tailored to your current emotional state (1-10 scale)

Multi-Platform Support: Search songs on both Spotify (app preferred) and YouTube

Personal Song Library: Build your own mood-based music collection

Recent Songs History: Track and manage your recently added songs

Dark/Light Theme: Toggle between themes for comfortable viewing

Standalone Executable: No installation required - just download and run!

Cross-Platform Compatibility: Works on Windows, macOS, and Linux

🚀 How to Use Rivixo
For End Users (Easy)
Download the ready-to-use executable file (Rivixo.exe)

Double-click to launch the application

No installation or dependencies required

For Developers
Ensure you have Python 3.x installed

Install required libraries: pip install tkinter

Run the application: python Rivixo.py

🎮 How It Works
Main Screen:

Enter your current mood (1-10)

Select your preferred platform (Spotify or YouTube)

Click "Open Suggested Song!" to get a recommendation

Your List Screen:

Add songs to specific mood categories (1-10)

View and manage recently added songs

Remove songs from your collection

Platform Integration:

Spotify: Opens directly in the Spotify app if installed, otherwise uses web player

YouTube: Opens search results in your default browser

📊 Mood Rating System
1-3: Low energy, melancholic, or calm moods

4-6: Balanced, neutral, or contemplative moods

7-8: Upbeat, positive, or energetic moods

9-10: High energy, euphoric, or excited moods

📁 Project Structure
Rivixo.py - Main application source code

Rivixo.exe - Standalone executable (no installation needed)

icon.png - Application icon

rivixolist/ - Directory containing mood-based song lists (1.txt to 10.txt)

Automatically created save files for persistent data

🎨 Interface Features
Clean, intuitive user interface

Responsive design that works on different screen sizes

Theme switching between light and dark modes

Easy navigation between main and management screens

Visual feedback for all actions

💡 Tips for Best Experience
Build Your Library: Add songs to different mood categories when you discover them

Use Specific Moods: The more precise your mood rating, the better the recommendations

Platform Choice: Use Spotify for higher quality audio, YouTube for wider selection

Regular Updates: Add new songs regularly to keep recommendations fresh

Theme Preference: Switch to dark mode for nighttime listening sessions

🔧 Technical Details
Built with Python and Tkinter for cross-platform compatibility

Uses system URI handlers for platform integration

Implements efficient file-based storage for song collections

Includes error handling for robust user experience

Supports UTF-8 encoding for international song titles
