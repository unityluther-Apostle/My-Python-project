# report.py
from nicegui import ui

def report(row_data):
    """
    Accepts student data records and generates a beautifully styled, 
    printable HTML report card customized for primary school presentation.
    """
    html_report_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{ size: A4; margin: 20px; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                padding: 25px; 
                color: #2c3e50; 
                background-color: #ffffff;
            }}
            
            /* Primary School Theme Frame Border */
            .report-card-border {{
                border: 8px double #800000;
                padding: 20px;
                border-radius: 12px;
                background-color: #fffdfa;
            }}
            
            /* Header Accent Styling */
            .header {{ 
                text-align: center; 
                border-bottom: 3px dashed #800000; 
                padding-bottom: 15px; 
                margin-bottom: 25px; 
            }}
            .school-title {{ 
                font-size: 30px; 
                font-weight: 800; 
                color: #800000; 
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 4px;
            }}
            .report-title {{ 
                font-size: 16px; 
                font-weight: 600;
                letter-spacing: 2px; 
                color: #d97706; 
                text-transform: uppercase;
            }}
            
            /* Metadata Grid Layout */
            .meta-table {{ 
                width: 100%; 
                margin-bottom: 25px; 
                border-collapse: separate;
                border-spacing: 0 8px;
            }}
            .meta-table td {{ 
                padding: 8px 12px; 
                font-size: 14px; 
                background-color: #f8fafc;
                border-top: 1px solid #e2e8f0;
                border-bottom: 1px solid #e2e8f0;
            }}
            .meta-table td:first-child, .meta-table td:nth-child(3) {{
                border-left: 1px solid #e2e8f0;
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
            }}
            .meta-table td:second-child, .meta-table td:last-child {{
                border-right: 1px solid #e2e8f0;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }}
            .bold {{ font-weight: 700; color: #1e293b; }}
            
            /* Academic Table Design Matrix */
            .marks-table {{ 
                width: 100%; 
                border-collapse: collapse; 
                margin-top: 10px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            }}
            .marks-table th {{ 
                background-color: #800000; 
                color: white; 
                text-align: left; 
                padding: 12px; 
                font-size: 13px; 
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .marks-table td {{ 
                padding: 12px; 
                border-bottom: 1px solid #e2e8f0; 
                font-size: 14px; 
            }}
            .marks-table tr:nth-child(even) {{
                background-color: #fffbfb;
            }}
            .grade-badge {{
                display: inline-block;
                padding: 3px 10px;
                background-color: #fef3c7;
                color: #d97706;
                border-radius: 4px;
                font-weight: bold;
            }}
            
            /* Performance Summary Box Panels */
            .summary-grid {{
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                margin-top: 25px;
            }}
            .metric-card {{
                flex: 1;
                min-width: 150px;
                background-color: #fdf8f6;
                border: 1px solid #f5e6e1;
                border-radius: 8px;
                padding: 12px;
                text-align: center;
            }}
            .metric-title {{ font-size: 11px; font-weight: 700; text-transform: uppercase; color: #7f1d1d; margin-bottom: 4px; }}
            .metric-value {{ font-size: 18px; font-weight: 800; color: #800000; }}
            
            .remarks-box {{
                width: 100%;
                margin-top: 15px;
                background-color: #fafafa;
                border-left: 4px solid #d97706;
                padding: 15px;
                border-radius: 4px;
                box-sizing: border-box;
            }}
            
            /* Sign-off Validation Blocks */
            .footer-sign {{ 
                margin-top: 60px; 
                display: flex; 
                justify-content: space-between; 
                font-size: 13px;
                font-weight: 600; 
                color: #475569;
            }}
            .signature-line {{
                border-top: 1px dashed #94a3b8;
                padding-top: 8px;
                width: 220px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="report-card-border">
            <div class="header">
                <div class="school-title">🎓 AIM PRE-SCHOOL</div>
                <div class="report-title">Official Student Terminal Report Card</div>
            </div>
            
            <table class="meta-table">
                <tr>
                    <td class="bold" width="18%">STUDENT NAME:</td><td width="32%">{row_data['Name']}</td>
                    <td class="bold" width="18%">CLASS LEVEL:</td><td width="32%">{row_data['Class']}</td>
                </tr>
                <tr>
                    <td class="bold">ADMIN NO:</td><td>{row_data['Admin']}</td>
                    <td class="bold">EXAM TYPE:</td><td>{row_data['ExamType']}</td>
                </tr>
                <tr>
                    <td class="bold">TERM DATE:</td><td>{row_data['ExamDate']}</td>
                    <td class="bold">ATTENDANCE:</td><td>{row_data['Attendance']} days</td>
                </tr>
            </table>

            <h4 style="color: #800000; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;">Subject Assessment Details</h4>
            <table class="marks-table">
                <thead>
                    <tr>
                        <th width="50%">Subject Name</th>
                        <th width="25%">Marks Attained</th>
                        <th width="25%">Letter Grade</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Mathematics</td><td class="bold">{row_data['Maths']}%</td><td><span class="grade-badge">{row_data['Maths_Grade']}</span></td></tr>
                    <tr><td>English Language</td><td class="bold">{row_data['English']}%</td><td><span class="grade-badge">{row_data['English_Grade']}</span></td></tr>
                    <tr><td>Social Studies (S.S.T)</td><td class="bold">{row_data['SST']}%</td><td><span class="grade-badge">{row_data['SST_Grade']}</span></td></tr>
                    <tr><td>Integrated Science</td><td class="bold">{row_data['Science']}%</td><td><span class="grade-badge">{row_data['Science_Grade']}</span></td></tr>
                </tbody>
            </table>
        
            <div class="summary-grid">
                <div class="metric-card">
                    <div class="metric-title">Total Score</div>
                    <div class="metric-value">{row_data['Total']}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">Average Percentage</div>
                    <div class="metric-value">{row_data['Average']:.1f}%</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">Final Grade</div>
                    <div class="metric-value">{row_data['Grade']}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">Class Position</div>
                    <div class="metric-value">Position {row_data['Rank']}</div>
                </div>
            </div>

            <div class="remarks-box">
                <span class="bold" style="color: #d97706; font-size: 12px; text-transform: uppercase; display: block; margin-bottom: 4px;">Class Teacher's Remarks:</span>
                <span style="font-style: italic; font-size: 14px; color: #334155;">"{row_data['Remarks']}"</span>
            </div>

            <div class="footer-sign">
                <div class="signature-line">Class Teacher Signature</div>
                <div class="signature-line">Headteacher Signature</div>
            </div>
        </div>
    </body>
    </html>
    """

    
    return html_report_content
