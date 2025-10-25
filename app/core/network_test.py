import psutil
import socket
import subprocess
import platform
import time
from typing import Dict, Any, List, Optional


class NetworkScanner:
    @staticmethod
    def get_network_info() -> Dict[str, Any]:
        try:
            addrs = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            io_counters = psutil.net_io_counters()
            
            interfaces = []
            active_interface = None
            mac_address = None
            ip_address = None
            ipv6_address = None
            
            for interface_name, addr_list in addrs.items():
                if interface_name in stats and stats[interface_name].isup:
                    interface_data = {
                        "name": interface_name,
                        "is_up": stats[interface_name].isup,
                        "speed_mbps": stats[interface_name].speed,
                        "mtu": stats[interface_name].mtu,
                        "addresses": []
                    }
                    
                    for addr in addr_list:
                        if addr.family == socket.AF_INET:
                            ip_address = addr.address
                            interface_data["addresses"].append({
                                "type": "IPv4",
                                "address": addr.address,
                                "netmask": addr.netmask
                            })
                            if not active_interface:
                                active_interface = interface_name
                        elif addr.family == socket.AF_INET6:
                            ipv6_address = addr.address
                            interface_data["addresses"].append({
                                "type": "IPv6",
                                "address": addr.address,
                                "netmask": addr.netmask
                            })
                        elif addr.family == psutil.AF_LINK:
                            mac_address = addr.address
                            interface_data["addresses"].append({
                                "type": "MAC",
                                "address": addr.address
                            })
                    
                    interfaces.append(interface_data)
            
            if not active_interface:
                return {
                    "detected": False,
                    "interface_name": None,
                    "status": "No active network interface"
                }
            
            ping_ms = NetworkScanner._test_ping()
            connection_quality = NetworkScanner._assess_connection_quality(ping_ms)
            
            network_info = {
                "detected": True,
                "active_interface": active_interface,
                "all_interfaces": interfaces,
                "mac_address": mac_address,
                "ip_address": ip_address,
                "ipv6_address": ipv6_address,
                "total_bytes_sent_gb": round(io_counters.bytes_sent / (1024**3), 2),
                "total_bytes_received_gb": round(io_counters.bytes_recv / (1024**3), 2),
                "packets_sent": io_counters.packets_sent,
                "packets_received": io_counters.packets_recv,
                "errors_in": io_counters.errin,
                "errors_out": io_counters.errout,
                "drops_in": io_counters.dropin,
                "drops_out": io_counters.dropout,
                "download_speed_mbps": None,
                "upload_speed_mbps": None,
                "ping_ms": ping_ms,
                "connection_quality": connection_quality,
                "connection_stable": ping_ms is not None and ping_ms < 100,
                "status": NetworkScanner._get_status(ping_ms),
                "health_score": NetworkScanner._calculate_health_score(ping_ms, io_counters.errin, io_counters.errout)
            }
            
            return network_info
            
        except Exception as e:
            return {
                "detected": False,
                "interface_name": None,
                "status": f"Error: {str(e)}"
            }
    
    @staticmethod
    def _test_ping(host: str = "8.8.8.8", timeout: int = 3) -> Optional[float]:
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
            timeout_value = str(timeout * 1000) if platform.system().lower() == 'windows' else str(timeout)
            
            command = ['ping', param, '1', timeout_param, timeout_value, host]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=timeout + 1)
            
            if result.returncode == 0:
                output = result.stdout
                if 'time=' in output.lower():
                    for line in output.split('\n'):
                        if 'time=' in line.lower():
                            time_str = line.split('time=')[1].split()[0]
                            time_str = time_str.replace('ms', '').strip()
                            return round(float(time_str), 2)
                return 50.0
            return None
            
        except Exception:
            return None
    
    @staticmethod
    def _assess_connection_quality(ping_ms: Optional[float]) -> str:
        if ping_ms is None:
            return "No Connection"
        elif ping_ms < 20:
            return "Excellent"
        elif ping_ms < 50:
            return "Very Good"
        elif ping_ms < 100:
            return "Good"
        elif ping_ms < 150:
            return "Fair"
        else:
            return "Poor"
    
    @staticmethod
    def _get_status(ping_ms: Optional[float]) -> str:
        if ping_ms is None:
            return "No Internet Connection"
        elif ping_ms < 50:
            return "Excellent"
        elif ping_ms < 100:
            return "Good"
        elif ping_ms < 200:
            return "Fair"
        else:
            return "Poor - High Latency"
    
    @staticmethod
    def _calculate_health_score(ping_ms: Optional[float], errors_in: int, errors_out: int) -> int:
        score = 100
        
        if ping_ms is None:
            score -= 50
        elif ping_ms > 200:
            score -= 40
        elif ping_ms > 100:
            score -= 25
        elif ping_ms > 50:
            score -= 10
        
        total_errors = errors_in + errors_out
        if total_errors > 1000:
            score -= 20
        elif total_errors > 100:
            score -= 10
        
        return max(0, score)
    
    @staticmethod
    def test_internet_speed() -> Dict[str, Any]:
        try:
            import speedtest
            
            print("Starting internet speed test... This may take 30-60 seconds...")
            
            st = speedtest.Speedtest()
            print("Finding best server...")
            st.get_best_server()
            
            print("Testing download speed...")
            download_speed = st.download() / 1_000_000
            
            print("Testing upload speed...")
            upload_speed = st.upload() / 1_000_000
            
            server_info = st.results.server
            
            return {
                "test_passed": True,
                "download_speed_mbps": round(download_speed, 2),
                "upload_speed_mbps": round(upload_speed, 2),
                "ping_ms": round(st.results.ping, 2),
                "server_name": server_info['name'],
                "server_country": server_info['country'],
                "server_sponsor": server_info['sponsor'],
                "timestamp": st.results.timestamp,
                "performance_rating": NetworkScanner._get_speed_rating(download_speed, upload_speed)
            }
            
        except Exception as e:
            return {
                "test_passed": False,
                "download_speed_mbps": None,
                "upload_speed_mbps": None,
                "error": str(e)
            }
    
    @staticmethod
    def _get_speed_rating(download_mbps: float, upload_mbps: float) -> str:
        if download_mbps > 100:
            return "Excellent - High-speed connection"
        elif download_mbps > 50:
            return "Very Good - Fast connection"
        elif download_mbps > 25:
            return "Good - Adequate for most uses"
        elif download_mbps > 10:
            return "Fair - Basic browsing and streaming"
        else:
            return "Poor - Slow connection"
    
    @staticmethod
    def perform_advanced_ping_test(host: str = "8.8.8.8", count: int = 20) -> Dict[str, Any]:
        try:
            print(f"Performing advanced ping test to {host} with {count} packets...")
            
            ping_times = []
            failed_pings = 0
            
            for i in range(count):
                ping_result = NetworkScanner._test_ping(host)
                if ping_result is not None:
                    ping_times.append(ping_result)
                else:
                    failed_pings += 1
                time.sleep(0.2)
            
            if not ping_times:
                return {
                    "test_passed": False,
                    "error": "All pings failed"
                }
            
            avg_ping = sum(ping_times) / len(ping_times)
            min_ping = min(ping_times)
            max_ping = max(ping_times)
            
            jitter = sum(abs(ping_times[i] - ping_times[i-1]) for i in range(1, len(ping_times))) / (len(ping_times) - 1) if len(ping_times) > 1 else 0
            
            packet_loss = (failed_pings / count) * 100
            
            return {
                "test_passed": True,
                "host": host,
                "packets_sent": count,
                "packets_received": len(ping_times),
                "packets_lost": failed_pings,
                "packet_loss_percent": round(packet_loss, 2),
                "min_ping_ms": round(min_ping, 2),
                "max_ping_ms": round(max_ping, 2),
                "average_ping_ms": round(avg_ping, 2),
                "jitter_ms": round(jitter, 2),
                "connection_stability": NetworkScanner._get_stability_rating(packet_loss, jitter),
                "performance_rating": NetworkScanner._get_ping_test_rating(avg_ping, packet_loss, jitter)
            }
            
        except Exception as e:
            return {
                "test_passed": False,
                "error": str(e)
            }
    
    @staticmethod
    def _get_stability_rating(packet_loss: float, jitter: float) -> str:
        if packet_loss == 0 and jitter < 5:
            return "Excellent - Very stable"
        elif packet_loss < 1 and jitter < 10:
            return "Good - Stable"
        elif packet_loss < 5 and jitter < 20:
            return "Fair - Moderately stable"
        else:
            return "Poor - Unstable connection"
    
    @staticmethod
    def _get_ping_test_rating(avg_ping: float, packet_loss: float, jitter: float) -> str:
        if avg_ping < 30 and packet_loss == 0 and jitter < 5:
            return "Excellent - Ideal for gaming and real-time applications"
        elif avg_ping < 50 and packet_loss < 1 and jitter < 10:
            return "Very Good - Suitable for most online activities"
        elif avg_ping < 100 and packet_loss < 3 and jitter < 20:
            return "Good - Adequate for general use"
        elif avg_ping < 150 and packet_loss < 5:
            return "Fair - May experience some lag"
        else:
            return "Poor - High latency or unstable connection"
