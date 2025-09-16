#!/usr/bin/env python3
"""
Nginx Browser Log Analysis Script

This script analyzes nginx logs to compare browser behavior and generate reports.
"""

import re
import json
from collections import defaultdict, Counter
from datetime import datetime
import argparse
from pathlib import Path


class BrowserLogAnalyzer:
    def __init__(self, log_file_path):
        self.log_file_path = Path(log_file_path)
        self.requests = []
        self.browser_stats = defaultdict(list)
        
    def parse_log_line(self, line):
        """Parse a single nginx log line using the custom browser_comparison format"""
        # Pattern for the custom log format
        pattern = r'(\S+) - (\S+) \[(.*?)\] "([^"]+)" (\d+) (\d+) "([^"]*)" "([^"]*)" "([^"]*)" "([^"]*)" "([^"]*)" "([^"]*)" "([^"]*)" "([^"]*)" "([^"]*)" ([^\s]*) ([^\s]*)'
        
        match = re.match(pattern, line.strip())
        if not match:
            return None
            
        groups = match.groups()
        return {
            'ip': groups[0],
            'user': groups[1],
            'timestamp': groups[2],
            'request': groups[3],
            'status': int(groups[4]),
            'bytes_sent': int(groups[5]),
            'referer': groups[6],
            'user_agent': groups[7],
            'accept': groups[8],
            'accept_language': groups[9],
            'accept_encoding': groups[10],
            'connection': groups[11],
            'cache_control': groups[12],
            'dnt': groups[13],
            'upgrade_insecure': groups[14],
            'request_time': float(groups[15]) if groups[15] != '-' else 0,
            'upstream_time': groups[16] if groups[16] != '-' else None
        }
    
    def identify_browser(self, user_agent):
        """Identify browser from user agent string"""
        user_agent_lower = user_agent.lower()
        
        if 'chrome' in user_agent_lower and 'edg' in user_agent_lower:
            return 'Edge'
        elif 'chrome' in user_agent_lower and 'safari' in user_agent_lower:
            return 'Chrome'
        elif 'firefox' in user_agent_lower:
            return 'Firefox'
        elif 'safari' in user_agent_lower and 'chrome' not in user_agent_lower:
            return 'Safari'
        elif 'opera' in user_agent_lower:
            return 'Opera'
        else:
            return 'Other'
    
    def parse_logs(self):
        """Parse the entire log file"""
        if not self.log_file_path.exists():
            print(f"Log file {self.log_file_path} not found!")
            return
        
        with open(self.log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                request = self.parse_log_line(line)
                if request:
                    request['line_number'] = line_num
                    browser = self.identify_browser(request['user_agent'])
                    request['browser'] = browser
                    self.requests.append(request)
                    self.browser_stats[browser].append(request)
    
    def generate_summary(self):
        """Generate a summary report"""
        total_requests = len(self.requests)
        
        print(f"\n🔍 NGINX BROWSER LOG ANALYSIS REPORT")
        print("=" * 50)
        print(f"📊 Total Requests: {total_requests}")
        print(f"📁 Log File: {self.log_file_path}")
        
        if total_requests == 0:
            print("❌ No requests found in log file")
            return
        
        # Browser distribution
        print(f"\n🌐 Browser Distribution:")
        browser_counts = Counter(req['browser'] for req in self.requests)
        for browser, count in browser_counts.most_common():
            percentage = (count / total_requests) * 100
            print(f"  {browser}: {count} requests ({percentage:.1f}%)")
        
        # Status codes
        print(f"\n📈 Response Status Codes:")
        status_counts = Counter(req['status'] for req in self.requests)
        for status, count in status_counts.most_common():
            percentage = (count / total_requests) * 100
            print(f"  {status}: {count} requests ({percentage:.1f}%)")
        
        # Average response times by browser
        print(f"\n⏱️  Average Response Times by Browser:")
        for browser, requests in self.browser_stats.items():
            if requests:
                times = [req['request_time'] for req in requests if req['request_time'] > 0]
                if times:
                    avg_time = sum(times) / len(times)
                    print(f"  {browser}: {avg_time:.3f}s (from {len(times)} requests)")
        
        # Most requested paths
        print(f"\n🔗 Most Requested Paths:")
        paths = []
        for req in self.requests:
            request_parts = req['request'].split(' ')
            if len(request_parts) >= 2:
                paths.append(request_parts[1])
        
        path_counts = Counter(paths)
        for path, count in path_counts.most_common(10):
            percentage = (count / total_requests) * 100
            print(f"  {path}: {count} requests ({percentage:.1f}%)")
    
    def browser_comparison(self):
        """Compare browser behaviors"""
        print(f"\n🔍 DETAILED BROWSER COMPARISON")
        print("=" * 50)
        
        for browser, requests in self.browser_stats.items():
            if not requests:
                continue
                
            print(f"\n🌐 {browser} Analysis ({len(requests)} requests):")
            
            # Unique user agents for this browser
            user_agents = set(req['user_agent'] for req in requests)
            print(f"  User Agent Variants: {len(user_agents)}")
            for ua in list(user_agents)[:3]:  # Show first 3
                print(f"    - {ua}")
            if len(user_agents) > 3:
                print(f"    ... and {len(user_agents) - 3} more")
            
            # Accept headers analysis
            accept_headers = Counter(req['accept'] for req in requests)
            print(f"  Most common Accept header:")
            for accept, count in accept_headers.most_common(1):
                print(f"    {accept} ({count} times)")
            
            # Language preferences
            languages = Counter(req['accept_language'] for req in requests)
            print(f"  Language preferences:")
            for lang, count in languages.most_common(2):
                if lang and lang != '-':
                    print(f"    {lang} ({count} times)")
            
            # Response time stats
            times = [req['request_time'] for req in requests if req['request_time'] > 0]
            if times:
                min_time = min(times)
                max_time = max(times)
                avg_time = sum(times) / len(times)
                print(f"  Response times: avg={avg_time:.3f}s, min={min_time:.3f}s, max={max_time:.3f}s")
    
    def export_json_report(self, output_file):
        """Export analysis results to JSON"""
        report = {
            'summary': {
                'total_requests': len(self.requests),
                'log_file': str(self.log_file_path),
                'analysis_time': datetime.now().isoformat()
            },
            'browser_distribution': dict(Counter(req['browser'] for req in self.requests)),
            'status_codes': dict(Counter(req['status'] for req in self.requests)),
            'browsers': {}
        }
        
        for browser, requests in self.browser_stats.items():
            if requests:
                times = [req['request_time'] for req in requests if req['request_time'] > 0]
                report['browsers'][browser] = {
                    'request_count': len(requests),
                    'user_agents': list(set(req['user_agent'] for req in requests)),
                    'avg_response_time': sum(times) / len(times) if times else 0,
                    'status_codes': dict(Counter(req['status'] for req in requests))
                }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n📄 JSON report exported to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Analyze nginx browser logs')
    parser.add_argument('log_file', help='Path to nginx log file')
    parser.add_argument('--json', help='Export JSON report to file')
    parser.add_argument('--detailed', action='store_true', help='Show detailed browser comparison')
    
    args = parser.parse_args()
    
    analyzer = BrowserLogAnalyzer(args.log_file)
    analyzer.parse_logs()
    analyzer.generate_summary()
    
    if args.detailed:
        analyzer.browser_comparison()
    
    if args.json:
        analyzer.export_json_report(args.json)


if __name__ == '__main__':
    main()