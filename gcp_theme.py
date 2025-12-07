"""
GCP Theme - Professional Multi-Color Design
Provides Google Cloud Platform-branded UI components with Google's signature colors
"""

import streamlit as st
from typing import Optional

class GCPTheme:
    """Google Cloud Platform Theme - Professional Multi-Color"""
    
    # Google Brand Colors
    BLUE = "#4285F4"         # Google Blue
    RED = "#EA4335"          # Google Red
    YELLOW = "#FBBC04"       # Google Yellow
    GREEN = "#34A853"        # Google Green
    
    # UI Colors
    DARK = "#1A237E"         # Dark blue (headers)
    LIGHT = "#FFFFFF"        # White (text)
    GREY = "#5F6368"         # Medium grey
    LIGHT_GREY = "#F8F9FA"   # Light grey (backgrounds)
    
    # Semantic Colors
    SUCCESS = "#34A853"      # Green
    WARNING = "#FBBC04"      # Yellow
    ERROR = "#EA4335"        # Red
    INFO = "#4285F4"         # Blue
    
    @staticmethod
    def gcp_header(title: str, subtitle: str = "", icon: str = "🔴"):
        """
        GCP header with dark blue background and white text
        High contrast: 10.8:1 ratio (exceeds WCAG AAA 7:1 standard)
        """
        html = f"""
        <div style="
            background: linear-gradient(135deg, #1A237E 0%, #283593 100%);
            padding: 30px;
            border-radius: 12px;
            border-left: 5px solid #4285F4;
            margin-bottom: 25px;
            box-shadow: 0 4px 12px rgba(66,133,244,0.3);
        ">
            <h1 style="color: #FFFFFF; margin: 0; font-weight: 600; font-size: 2em;">
                {icon} {title}
            </h1>
            {f'<p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 1.1em;">{subtitle}</p>' if subtitle else ""}
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    @staticmethod
    def gcp_metric_card(label: str, value: str, icon: str = None, delta: str = None, metric_type: str = "default"):
        """
        GCP metric card with Google's multi-color accents
        Renders immediately - no need for st.markdown() after calling
        
        metric_type: 'cost', 'performance', 'alert', or 'default'
        """
        # Determine accent color based on metric type
        accent_colors = {
            "cost": "#34A853",       # Green
            "performance": "#FBBC04", # Yellow
            "alert": "#EA4335",      # Red
            "default": "#4285F4"     # Blue
        }
        accent_color = accent_colors.get(metric_type, "#4285F4")
        
        # Determine delta color
        delta_color = "#34A853"  # Green for positive
        if delta and "-" in str(delta):
            delta_color = "#EA4335"  # Red for negative
        
        html = f"""
        <div style="
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid {accent_color};
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        ">
            {f'<div style="color: #5F6368; font-size: 1.8em; margin-bottom: 8px;">{icon}</div>' if icon else ""}
            <div style="color: {accent_color}; font-size: 0.85em; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">
                {label}
            </div>
            <div style="color: #1A237E; font-size: 2.2em; font-weight: 700; margin-top: 8px; line-height: 1;">
                {value}
            </div>
            {f'<div style="color: {delta_color}; font-size: 0.95em; margin-top: 8px; font-weight: 500;">{delta}</div>' if delta else ""}
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    @staticmethod
    def gcp_info_box(title: str, content: str, box_type: str = "info"):
        """
        GCP info box with Google color styling
        Types: info, success, warning, error
        """
        colors = {
            "info": {"bg": "#E8F0FE", "border": "#4285F4", "icon": "ℹ️"},
            "success": {"bg": "#E6F4EA", "border": "#34A853", "icon": "✅"},
            "warning": {"bg": "#FEF7E0", "border": "#FBBC04", "icon": "⚠️"},
            "error": {"bg": "#FCE8E6", "border": "#EA4335", "icon": "❌"}
        }
        
        style = colors.get(box_type, colors["info"])
        
        html = f"""
        <div style="
            background-color: {style['bg']};
            padding: 20px;
            border-radius: 8px;
            border-left: 5px solid {style['border']};
            margin: 15px 0;
        ">
            <div style="font-weight: 600; color: #1A237E; margin-bottom: 8px; font-size: 1.1em;">
                {style['icon']} {title}
            </div>
            <div style="color: #5F6368; line-height: 1.6;">
                {content}
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    @staticmethod
    def gcp_section_header(text: str, icon: str = "📋"):
        """GCP section header with Google colors"""
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #1A237E 0%, #4285F4 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 6px;
            margin: 20px 0 15px 0;
            font-weight: 600;
            font-size: 1.2em;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            {icon} {text}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def gcp_status_badge(status: str):
        """GCP status badge with Google colors"""
        colors = {
            "active": {"bg": "#E6F4EA", "text": "#34A853", "label": "Active"},
            "running": {"bg": "#E6F4EA", "text": "#34A853", "label": "Running"},
            "stopped": {"bg": "#FCE8E6", "text": "#EA4335", "label": "Stopped"},
            "pending": {"bg": "#FEF7E0", "text": "#FBBC04", "label": "Pending"},
            "disabled": {"bg": "#F8F9FA", "text": "#5F6368", "label": "Disabled"}
        }
        
        style = colors.get(status.lower(), {"bg": "#E8F0FE", "text": "#4285F4", "label": status})
        
        return f"""
        <span style="
            background-color: {style['bg']};
            color: {style['text']};
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            display: inline-block;
        ">
            {style['label']}
        </span>
        """
    
    @staticmethod
    def gcp_progress_bar(percentage: int, label: str = "", color_scheme: str = "auto"):
        """
        GCP progress bar with Google colors
        color_scheme: 'auto', 'blue', 'green', 'yellow', 'red'
        """
        # Determine color
        if color_scheme == "auto":
            if percentage >= 90:
                color = "#EA4335"  # Red - critical
            elif percentage >= 75:
                color = "#FBBC04"  # Yellow - warning
            else:
                color = "#34A853"  # Green - good
        else:
            colors = {
                "blue": "#4285F4",
                "green": "#34A853",
                "yellow": "#FBBC04",
                "red": "#EA4335"
            }
            color = colors.get(color_scheme, "#4285F4")
        
        html = f"""
        <div style="margin: 15px 0;">
            {f'<div style="color: #5F6368; font-size: 0.9em; margin-bottom: 5px;">{label}</div>' if label else ""}
            <div style="
                background-color: #F8F9FA;
                border-radius: 10px;
                height: 24px;
                position: relative;
                overflow: hidden;
            ">
                <div style="
                    background: linear-gradient(90deg, {color} 0%, {color}CC 100%);
                    width: {percentage}%;
                    height: 100%;
                    border-radius: 10px;
                    transition: width 0.3s ease;
                "></div>
                <div style="
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    color: {'white' if percentage > 50 else '#1A237E'};
                    font-weight: 600;
                    font-size: 0.85em;
                ">
                    {percentage}%
                </div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    @staticmethod
    def gcp_card(title: str, content: str, icon: str = None, accent: str = "blue"):
        """
        GCP card component with colored accent
        accent: 'blue', 'red', 'yellow', 'green'
        """
        accent_colors = {
            "blue": "#4285F4",
            "red": "#EA4335",
            "yellow": "#FBBC04",
            "green": "#34A853"
        }
        accent_color = accent_colors.get(accent, "#4285F4")
        
        html = f"""
        <div style="
            background-color: white;
            border: 1px solid #E8EAED;
            border-left: 4px solid {accent_color};
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        ">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                {f'<span style="font-size: 1.5em; margin-right: 10px;">{icon}</span>' if icon else ""}
                <h3 style="margin: 0; color: #1A237E; font-size: 1.2em;">{title}</h3>
            </div>
            <div style="color: #5F6368; line-height: 1.6;">
                {content}
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    @staticmethod
    def gcp_multi_color_divider():
        """GCP divider with Google's signature 4 colors"""
        st.markdown("""
        <div style="
            height: 4px;
            background: linear-gradient(90deg, 
                #4285F4 0%, 
                #EA4335 33%, 
                #FBBC04 66%, 
                #34A853 100%);
            margin: 20px 0;
            border-radius: 2px;
        "></div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def gcp_table_header():
        """GCP table header styling"""
        st.markdown("""
        <style>
        .gcp-table th {
            background-color: #1A237E !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 12px !important;
        }
        .gcp-table td {
            padding: 10px !important;
            border-bottom: 1px solid #E8EAED !important;
        }
        .gcp-table tr:hover {
            background-color: #F8F9FA !important;
        }
        </style>
        """, unsafe_allow_html=True)

# Helper functions for quick access
def gcp_header(title: str, subtitle: str = "", icon: str = "🔴"):
    """Quick access to GCP header"""
    GCPTheme.gcp_header(title, subtitle, icon)

def gcp_metric_card(label: str, value: str, icon: str = None, delta: str = None, metric_type: str = "default"):
    """Quick access to GCP metric card"""
    GCPTheme.gcp_metric_card(label, value, icon, delta, metric_type)

def gcp_info_box(title: str, content: str, box_type: str = "info"):
    """Quick access to GCP info box"""
    GCPTheme.gcp_info_box(title, content, box_type)

def gcp_section_header(text: str, icon: str = "📋"):
    """Quick access to GCP section header"""
    GCPTheme.gcp_section_header(text, icon)
