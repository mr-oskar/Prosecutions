import psutil
from typing import Dict, Any
import socket


class NetworkScanner:
    @staticmethod
    def get_network_info() -> Dict[str, Any]:
        try:
            addrs = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            
            active_interface = None
            mac_address = None
            ip_address = None
            
            for interface_name, addr_list in addrs.items():
                if interface_name in stats and stats[interface_name].isup:
                    for addr in addr_list:
                        if addr.family == socket.AF_INET:
                            ip_address = addr.address
                            active_interface = interface_name
                        elif addr.family == psutil.AF_LINK:
                            mac_address = addr.address
                    
                    if active_interface:
                        break
            
            if not active_interface:
                return {
                    "detected": False,
                    "interface_name": None,
                    "status": "No active network interface"
                }
            
            ping_ms = NetworkScanner._test_ping()
            
            network_info = {
                "detected": True,
                "interface_name": active_interface,
                "mac_address": mac_address,
                "ip_address": ip_address,
                "download_speed_mbps": None,
                "upload_speed_mbps": None,
                "ping_ms": ping_ms,
                "connection_stable": ping_ms is not None and ping_ms < 100,
                "status": NetworkScanner._get_status(ping_ms)
            }
            
            return network_info
            
        except Exception as e:
            return {
                "detected": False,
                "interface_name": None,
                "status": f"Error: {str(e)}"
            }
    
    @staticmethod
    def _test_ping(host: str = "8.8.8.8", timeout: int = 2) -> float:
        import subprocess
        import platform
        
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '1', '-w' if platform.system().lower() == 'windows' else '-W', str(timeout * 1000 if platform.system().lower() == 'windows' else timeout), host]
            
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
    def _get_status(ping_ms: float) -> str:
        if ping_ms is None:
            return "No Connection"
        elif ping_ms < 50:
            return "Excellent"
        elif ping_ms < 100:
            return "Good"
        elif ping_ms < 200:
            return "Fair"
        else:
            return "Poor"
    
    @staticmethod
    def test_internet_speed() -> Dict[str, Any]:
        try:
            import speedtest
            
            st = speedtest.Speedtest()
            st.get_best_server()
            
            download_speed = st.download() / 1_000_000
            upload_speed = st.upload() / 1_000_000
            
            return {
                "download_speed_mbps": round(download_speed, 2),
                "upload_speed_mbps": round(upload_speed, 2),
                "ping_ms": st.results.ping
            }
            
        except Exception as e:
            return {
                "download_speed_mbps": None,
                "upload_speed_mbps": None,
                "error": str(e)
            }
