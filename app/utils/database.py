import sqlite3
import secrets
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import json


class Database:
    def __init__(self, db_path: str = "db/system_guardian.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                device_id TEXT,
                duration_days INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                scans_count INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id TEXT UNIQUE NOT NULL,
                subscription_code TEXT,
                device_id TEXT,
                scan_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subscription_code) REFERENCES subscriptions(code)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_unique_code(self, length: int = 16) -> str:
        return secrets.token_urlsafe(length)[:length].upper()
    
    def create_subscription(self, email: str, duration_days: int = 30, device_id: Optional[str] = None) -> Dict[str, Any]:
        code = self.generate_unique_code()
        created_at = datetime.now()
        expires_at = created_at + timedelta(days=duration_days)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO subscriptions (code, email, device_id, duration_days, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (code, email, device_id, duration_days, created_at, expires_at))
            
            conn.commit()
            subscription_id = cursor.lastrowid
            
            return {
                'id': subscription_id,
                'code': code,
                'email': email,
                'device_id': device_id,
                'duration_days': duration_days,
                'created_at': created_at.isoformat(),
                'expires_at': expires_at.isoformat(),
                'is_active': True,
                'scans_count': 0
            }
        finally:
            conn.close()
    
    def verify_subscription(self, code: str, device_id: Optional[str] = None) -> Dict[str, Any]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM subscriptions WHERE code = ? AND is_active = 1
            ''', (code,))
            
            row = cursor.fetchone()
            
            if not row:
                return {
                    'valid': False,
                    'message': 'الكود غير صحيح أو غير نشط / Invalid or inactive code'
                }
            
            expires_at = datetime.fromisoformat(row['expires_at'])
            
            if datetime.now() > expires_at:
                cursor.execute('UPDATE subscriptions SET is_active = 0 WHERE code = ?', (code,))
                conn.commit()
                return {
                    'valid': False,
                    'message': 'انتهت صلاحية الاشتراك / Subscription expired',
                    'expired_at': expires_at.isoformat()
                }
            
            if device_id and row['device_id'] and row['device_id'] != device_id:
                return {
                    'valid': False,
                    'message': 'هذا الكود مرتبط بجهاز آخر / Code is bound to another device'
                }
            
            if device_id and not row['device_id']:
                cursor.execute('UPDATE subscriptions SET device_id = ? WHERE code = ?', (device_id, code))
                conn.commit()
            
            return {
                'valid': True,
                'message': 'الاشتراك صالح / Subscription is valid',
                'subscription': {
                    'code': row['code'],
                    'email': row['email'],
                    'expires_at': expires_at.isoformat(),
                    'days_left': (expires_at - datetime.now()).days,
                    'scans_count': row['scans_count']
                }
            }
        finally:
            conn.close()
    
    def increment_scan_count(self, code: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE subscriptions SET scans_count = scans_count + 1 WHERE code = ?', (code,))
            conn.commit()
        finally:
            conn.close()
    
    def save_scan_result(self, scan_id: str, subscription_code: str, device_id: str, scan_data: Dict[str, Any]):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO scan_history (scan_id, subscription_code, device_id, scan_data)
                VALUES (?, ?, ?, ?)
            ''', (scan_id, subscription_code, device_id, json.dumps(scan_data)))
            conn.commit()
        finally:
            conn.close()
    
    def get_all_subscriptions(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM subscriptions ORDER BY created_at DESC')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    def renew_subscription(self, code: str, additional_days: int = 30) -> Dict[str, Any]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM subscriptions WHERE code = ?', (code,))
            row = cursor.fetchone()
            
            if not row:
                return {'success': False, 'message': 'الكود غير موجود / Code not found'}
            
            current_expires = datetime.fromisoformat(row['expires_at'])
            now = datetime.now()
            
            if current_expires > now:
                new_expires = current_expires + timedelta(days=additional_days)
            else:
                new_expires = now + timedelta(days=additional_days)
            
            cursor.execute('''
                UPDATE subscriptions 
                SET expires_at = ?, is_active = 1 
                WHERE code = ?
            ''', (new_expires, code))
            
            conn.commit()
            
            return {
                'success': True,
                'message': 'تم تجديد الاشتراك بنجاح / Subscription renewed successfully',
                'new_expires_at': new_expires.isoformat()
            }
        finally:
            conn.close()
