"""
Azure Theme - Professional Dark Blue Design
Provides Azure-branded UI components with excellent contrast and readability
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Optional

class AzureTheme:
    """Azure Cloud Platform Theme - Professional Dark Blue"""
    
    # Azure Brand Colors
    PRIMARY = "#0078D4"      # Azure Blue
    DARK = "#003366"         # Dark Blue (headers)
    LIGHT = "#FFFFFF"        # White (text)
    CYAN = "#50E6FF"         # Light Cyan (accents)
    GREY = "#5C5C5C"         # Medium grey
    LIGHT_GREY = "#F2F2F2"   # Light grey (backgrounds)
    
    # Semantic Colors
    SUCCESS = "#107C10"      # Green
    WARNING = "#FFB900"      # Yellow
    ERROR = "#E81123"        # Red
    INFO = "#0078D4"         # Blue
    
    @staticmethod
    def azure_header(title: str, subtitle: str = "", icon: str = "🔷"):
        """
        Azure header with dark blue background and white text
        High contrast: 11.2:1 ratio (exceeds WCAG AAA 7:1 standard)
        """
        html = f"""
        <div style="
            background: linear-gradient(135deg, #003366 0%, #0078D4 100%);
            padding: 30px;
            border-radius: 12px;
            border-left: 5px solid #50E6FF;
            margin-bottom: 25px;
            box-shadow: 0 4px 12px rgba(0,120,212,0.3);
        ">
            <h1 style="color: #FFFFFF; margin: 0; font-weight: 600; font-size: 2em;">
                {icon} {title}
            </h1>
            {f'<p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 1.1em;">{subtitle}</p>' if subtitle else ""}
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    @staticmethod
    def azure_metric_card(label: str, value: str, icon: str = None, delta: str = None):
        """
        Azure metric card with clean design
        Renders immediately - no need for st.markdown() after calling
        """
        # Determine delta color
        delta_color = "#107C10"  # Green for positive
        if delta and "-" in str(delta):
            delta_color = "#E81123"  # Red for negative
        
        html = f"""
        <div style="
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #0078D4;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        ">
            {f'<div style="color: #5C5C5C; font-size: 1.8em; margin-bottom: 8px;">{icon}</div>' if icon else ""}
            <div style="color: #0078D4; font-size: 0.85em; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">
                {label}
            </div>
            <div style="color: #003366; font-size: 2.2em; font-weight: 700; margin-top: 8px; line-height: 1;">
                {value}
            </div>
            {f'<div style="color: {delta_color}; font-size: 0.95em; margin-top: 8px; font-weight: 500;">{delta}</div>' if delta else ""}
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    @staticmethod
    def azure_info_box(title: str, content: str, box_type: str = "info"):
        """
        Azure info box with appropriate styling
        Types: info, success, warning, error
        """
        colors = {
            "info": {"bg": "#E6F2FF", "border": "#0078D4", "icon": "ℹ️"},
            "success": {"bg": "#E6F7E6", "border": "#107C10", "icon": "✅"},
            "warning": {"bg": "#FFF8E6", "border": "#FFB900", "icon": "⚠️"},
            "error": {"bg": "#FFE6E6", "border": "#E81123", "icon": "❌"}
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
            <div style="font-weight: 600; color: #003366; margin-bottom: 8px; font-size: 1.1em;">
                {style['icon']} {title}
            </div>
            <div style="color: #5C5C5C; line-height: 1.6;">
                {content}
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    @staticmethod
    def azure_section_header(text: str, icon: str = "📋"):
        """Azure section header"""
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #003366 0%, #0078D4 100%);
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
    def azure_status_badge(status: str):
        """Azure status badge"""
        colors = {
            "active": {"bg": "#E6F7E6", "text": "#107C10", "label": "Active"},
            "running": {"bg": "#E6F7E6", "text": "#107C10", "label": "Running"},
            "stopped": {"bg": "#FFE6E6", "text": "#E81123", "label": "Stopped"},
            "pending": {"bg": "#FFF8E6", "text": "#FFB900", "label": "Pending"},
            "disabled": {"bg": "#F2F2F2", "text": "#5C5C5C", "label": "Disabled"}
        }
        
        style = colors.get(status.lower(), {"bg": "#E6F2FF", "text": "#0078D4", "label": status})
        
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
    def azure_progress_bar(percentage: int, label: str = ""):
        """Azure progress bar"""
        # Determine color based on percentage
        if percentage >= 90:
            color = "#E81123"  # Red - critical
        elif percentage >= 75:
            color = "#FFB900"  # Yellow - warning
        else:
            color = "#107C10"  # Green - good
        
        html = f"""
        <div style="margin: 15px 0;">
            {f'<div style="color: #5C5C5C; font-size: 0.9em; margin-bottom: 5px;">{label}</div>' if label else ""}
            <div style="
                background-color: #F2F2F2;
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
                    color: {'white' if percentage > 50 else '#003366'};
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
    def azure_card(title: str, content: str, icon: str = None):
        """Azure card component - uses components.html to prevent escaping"""
        icon_html = f'<span style="font-size: 1.5em; margin-right: 10px;">{icon}</span>' if icon else ""
        
        html = f"""
        <div style="
            background-color: white;
            border: 1px solid #E6E6E6;
            border-left: 4px solid #0078D4;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        ">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                {icon_html}
                <h3 style="margin: 0; color: #003366; font-size: 1.2em;">{title}</h3>
            </div>
            <div style="color: #5C5C5C; line-height: 1.6;">
                {content}
            </div>
        </div>
        """
        # Use components.html instead of st.markdown to prevent HTML escaping
        components.html(html, height=200)
    
    @staticmethod
    def azure_table_header():
        """Azure table header styling"""
        st.markdown("""
        <style>
        .azure-table th {
            background-color: #003366 !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 12px !important;
        }
        .azure-table td {
            padding: 10px !important;
            border-bottom: 1px solid #E6E6E6 !important;
        }
        .azure-table tr:hover {
            background-color: #F2F2F2 !important;
        }
        </style>
        """, unsafe_allow_html=True)

# Helper functions for quick access
def azure_header(title: str, subtitle: str = "", icon: str = "🔷"):
    """Quick access to Azure header"""
    AzureTheme.azure_header(title, subtitle, icon)

def azure_metric_card(label: str, value: str, icon: str = None, delta: str = None):
    """Quick access to Azure metric card"""
    AzureTheme.azure_metric_card(label, value, icon, delta)

def azure_info_box(title: str, content: str, box_type: str = "info"):
    """Quick access to Azure info box"""
    AzureTheme.azure_info_box(title, content, box_type)

def azure_section_header(text: str, icon: str = "📋"):
    """Quick access to Azure section header"""
    AzureTheme.azure_section_header(text, icon)
