#!/usr/bin/env python3
"""
MineCloud Status Page
"""

from flask import Flask, render_template_string
from mcstatus import JavaServer
import os
import socket

app = Flask(__name__)

# Configuration Docker Compose : 
# Hostname = "minecraft"
MINECRAFT_HOST = os.getenv("MINECRAFT_HOST", "minecraft")
MINECRAFT_PORT = int(os.getenv("MINECRAFT_PORT", 25565))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="30">
    <title>MineCloud - Status</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #fff;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 500px;
            width: 90%;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #00d4ff, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .status-card {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        }
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .status-dot { width: 15px; height: 15px; border-radius: 50%; }
        .online .status-dot { background: #00ff88; box-shadow: 0 0 20px #00ff88; animation: pulse 2s infinite; }
        .offline .status-dot { background: #ff4757; box-shadow: 0 0 20px #ff4757; }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.1); }
        }
        .stats { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 20px; }
        .stat-box { background: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 15px; }
        .stat-label { color: #888; font-size: 0.8rem; text-transform: uppercase; }
        .stat-value { font-size: 1.2rem; font-weight: bold; color: #00d4ff; margin-top: 5px; }
        .server-address { font-family: monospace; background: rgba(0, 212, 255, 0.1); padding: 10px; border-radius: 8px; color: #00d4ff; }
        .motd { margin-top: 15px; font-style: italic; color: #ccc; font-size: 0.9rem; }
        .footer { margin-top: 30px; color: #666; font-size: 0.8rem; }
    </style>
</head>
<body>
    <div class="container">
        <div style="font-size: 48px;">⛏️</div>
        <h1>MineCloud</h1>
        <p style="color: #aaa; margin-bottom: 20px;">Monitoring Temps Réel</p>

        <div class="status-card">
            <div class="status-indicator {{ 'online' if server_online else 'offline' }}">
                <span class="status-dot"></span>
                <span>{{ 'EN LIGNE' if server_online else 'HORS LIGNE' }}</span>
            </div>

            {% if server_online %}
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-label">Joueurs</div>
                    <div class="stat-value">{{ players_online }} / {{ players_max }}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Latence</div>
                    <div class="stat-value">{{ latency }} ms</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Version</div>
                    <div class="stat-value">{{ version }}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Statut</div>
                    <div class="stat-value">OK</div>
                </div>
            </div>
            <p class="motd">{{ motd }}</p>
            {% else %}
            <p style="color: #ff6b6b;">{{ error_message }}</p>
            {% endif %}
        </div>

        <div style="margin-top: 20px;">
            <p style="color: #888; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 5px;">IP du Serveur</p>
            <p class="server-address">{{ server_address }}:{{ server_port }}</p>
        </div>

        <div class="footer">
            <p>MineCloud Ops &copy; 2026 - GamingCorp</p>
        </div>
    </div>
</body>
</html>
"""

def get_server_status():
    result = {
        "server_online": False,
        "players_online": 0, "players_max": 0,
        "version": "N/A", "latency": 0, "motd": "",
        "error_message": "Serveur injoignable",
        "server_address": MINECRAFT_HOST, "server_port": MINECRAFT_PORT
    }
    try:
        # Short Timeout
        server = JavaServer.lookup(f"{MINECRAFT_HOST}:{MINECRAFT_PORT}", timeout=3)
        status = server.status()

        result["server_online"] = True
        result["players_online"] = status.players.online
        result["players_max"] = status.players.max
        result["version"] = status.version.name
        result["latency"] = round(status.latency, 1)

        # Extraction
        if hasattr(status, 'description'):
            desc = status.description
            result["motd"] = desc.to_plain() if hasattr(desc, 'to_plain') else str(desc)

    except Exception as e:
        result["error_message"] = f"Erreur : {str(e)}"
    return result

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, **get_server_status())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
