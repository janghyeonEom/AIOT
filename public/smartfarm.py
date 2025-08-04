import time
import random
import datetime
from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class SensorData:
    """센서 데이터 클래스"""
    timestamp: str
    temperature: float
    humidity: float
    fan_status: bool
    pump_status: bool

class SmartFarmController:
    """스마트 팜 제어 시스템"""
    
    def __init__(self):
        # 제어 설정값
        self.temp_threshold = 30.0  # 온도 임계값 (℃)
        self.humidity_threshold = 40.0  # 습도 임계값 (%)
        
        # 장비 상태
        self.fan_running = False
        self.pump_running = False
        
        # 센서 데이터 로그
        self.data_log: List[SensorData] = []
        
        # 시뮬레이션용 환경 변수
        self.current_temp = 25.0
        self.current_humidity = 45.0
        
        print("🌱 스마트 팜 제어 시스템이 시작되었습니다!")
        print(f"📊 온도 임계값: {self.temp_threshold}℃")
        print(f"💧 습도 임계값: {self.humidity_threshold}%")
        print("-" * 50)
    
    def read_sensors(self) -> tuple:
        """
        센서에서 온도와 습도를 읽어옵니다.
        실제 환경에서는 DHT22, SHT30 등의 센서를 사용합니다.
        """
        # 시뮬레이션: 실제 환경에서는 센서에서 값을 읽어옵니다
        # 온도는 20-40도, 습도는 30-70% 범위에서 변동
        temp_variation = random.uniform(-2, 3)
        humidity_variation = random.uniform(-5, 8)
        
        # 장비 동작에 따른 환경 변화 시뮬레이션
        if self.fan_running:
            temp_variation -= 2  # 환풍기 동작시 온도 하강
        if self.pump_running:
            humidity_variation += 5  # 펌프 동작시 습도 상승
        
        self.current_temp += temp_variation * 0.1
        self.current_humidity += humidity_variation * 0.1
        
        # 현실적인 범위로 제한
        self.current_temp = max(15, min(45, self.current_temp))
        self.current_humidity = max(20, min(90, self.current_humidity))
        
        return round(self.current_temp, 1), round(self.current_humidity, 1)
    
    def control_fan(self, turn_on: bool):
        """환풍기 제어"""
        if turn_on and not self.fan_running:
            self.fan_running = True
            print("🌪️  환풍기 ON - 온도 낮추는 중...")
        elif not turn_on and self.fan_running:
            self.fan_running = False
            print("⏹️  환풍기 OFF")
    
    def control_pump(self, turn_on: bool):
        """물 펌프 제어"""
        if turn_on and not self.pump_running:
            self.pump_running = True
            print("💦 물 펌프 ON - 습도 높이는 중...")
        elif not turn_on and self.pump_running:
            self.pump_running = False
            print("⏹️  물 펌프 OFF")
    
    def make_control_decisions(self, temperature: float, humidity: float):
        """온도습도에 따른 제어 결정"""
        
        # 온도 제어 로직
        if temperature > self.temp_threshold:
            self.control_fan(True)
        elif temperature < self.temp_threshold - 2:  # 히스테리시스 적용
            self.control_fan(False)
        
        # 습도 제어 로직
        if humidity < self.humidity_threshold:
            self.control_pump(True)
        elif humidity > self.humidity_threshold + 10:  # 히스테리시스 적용
            self.control_pump(False)
    
    def log_data(self, temperature: float, humidity: float):
        """데이터 로깅"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = SensorData(
            timestamp=timestamp,
            temperature=temperature,
            humidity=humidity,
            fan_status=self.fan_running,
            pump_status=self.pump_running
        )
        self.data_log.append(data)
        
        # 최근 100개 데이터만 유지
        if len(self.data_log) > 100:
            self.data_log.pop(0)
    
    def display_status(self, temperature: float, humidity: float):
        """현재 상태 출력"""
        print(f"\n📊 [{datetime.datetime.now().strftime('%H:%M:%S')}] 현재 상태")
        print(f"🌡️  온도: {temperature}℃ {'⚠️ ' if temperature > self.temp_threshold else '✅'}")
        print(f"💧 습도: {humidity}% {'⚠️ ' if humidity < self.humidity_threshold else '✅'}")
        print(f"🌪️  환풍기: {'🟢 ON' if self.fan_running else '🔴 OFF'}")
        print(f"💦 펌프: {'🟢 ON' if self.pump_running else '🔴 OFF'}")
        print("-" * 40)
    
    def get_statistics(self) -> Dict:
        """통계 정보 반환"""
        if not self.data_log:
            return {}
        
        temps = [data.temperature for data in self.data_log]
        humids = [data.humidity for data in self.data_log]
        
        return {
            "avg_temp": round(sum(temps) / len(temps), 1),
            "max_temp": max(temps),
            "min_temp": min(temps),
            "avg_humidity": round(sum(humids) / len(humids), 1),
            "max_humidity": max(humids),
            "min_humidity": min(humids),
            "fan_runtime": sum(1 for data in self.data_log if data.fan_status),
            "pump_runtime": sum(1 for data in self.data_log if data.pump_status),
            "total_records": len(self.data_log)
        }
    
    def save_log_to_file(self, filename: str = "farm_log.json"):
        """로그를 파일로 저장"""
        try:
            data_dict = [
                {
                    "timestamp": data.timestamp,
                    "temperature": data.temperature,
                    "humidity": data.humidity,
                    "fan_status": data.fan_status,
                    "pump_status": data.pump_status
                }
                for data in self.data_log
            ]
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=2)
            print(f"📝 로그가 {filename}에 저장되었습니다.")
        except Exception as e:
            print(f"❌ 로그 저장 실패: {e}")
    
    def run_monitoring_cycle(self, duration_minutes: int = 5):
        """모니터링 사이클 실행"""
        print(f"🔄 {duration_minutes}분간 모니터링을 시작합니다...")
        print("Ctrl+C를 눌러 중단할 수 있습니다.\n")
        
        cycle_count = 0
        
        try:
            while cycle_count < duration_minutes * 12:  # 5초마다 체크
                # 센서 데이터 읽기
                temperature, humidity = self.read_sensors()
                
                # 제어 결정
                self.make_control_decisions(temperature, humidity)
                
                # 데이터 로깅
                self.log_data(temperature, humidity)
                
                # 상태 출력 (10회마다 = 50초마다)
                if cycle_count % 10 == 0:
                    self.display_status(temperature, humidity)
                
                cycle_count += 1
                time.sleep(5)  # 5초 대기
                
        except KeyboardInterrupt:
            print("\n\n⏹️  모니터링이 중단되었습니다.")
        
        # 최종 통계 출력
        stats = self.get_statistics()
        if stats:
            print("\n📈 운영 통계:")
            print(f"   평균 온도: {stats['avg_temp']}℃ (최고: {stats['max_temp']}℃, 최저: {stats['min_temp']}℃)")
            print(f"   평균 습도: {stats['avg_humidity']}% (최고: {stats['max_humidity']}%, 최저: {stats['min_humidity']}%)")
            print(f"   환풍기 동작: {stats['fan_runtime']}/{stats['total_records']}회")
            print(f"   펌프 동작: {stats['pump_runtime']}/{stats['total_records']}회")
        
        # 로그 저장
        self.save_log_to_file()

def main():
    """메인 함수"""
    print("🌱 스마트 팜 온도습도 제어 시스템")
    print("=" * 50)
    
    # 스마트 팜 컨트롤러 생성
    farm = SmartFarmController()
    
    while True:
        print("\n메뉴를 선택하세요:")
        print("1. 실시간 모니터링 시작 (5분)")
        print("2. 단일 측정 및 제어")
        print("3. 설정 변경")
        print("4. 통계 보기")
        print("5. 종료")
        
        try:
            choice = input("\n선택 (1-5): ").strip()
            
            if choice == '1':
                duration = input("모니터링 시간을 입력하세요 (분, 기본값 5): ").strip()
                duration = int(duration) if duration.isdigit() else 5
                farm.run_monitoring_cycle(duration)
                
            elif choice == '2':
                temp, humidity = farm.read_sensors()
                farm.make_control_decisions(temp, humidity)
                farm.log_data(temp, humidity)
                farm.display_status(temp, humidity)
                
            elif choice == '3':
                print(f"\n현재 설정:")
                print(f"온도 임계값: {farm.temp_threshold}℃")
                print(f"습도 임계값: {farm.humidity_threshold}%")
                
                try:
                    new_temp = input("새 온도 임계값 (엔터로 유지): ").strip()
                    new_humidity = input("새 습도 임계값 (엔터로 유지): ").strip()
                    
                    if new_temp:
                        farm.temp_threshold = float(new_temp)
                    if new_humidity:
                        farm.humidity_threshold = float(new_humidity)
                    
                    print("✅ 설정이 업데이트되었습니다.")
                except ValueError:
                    print("❌ 잘못된 값입니다.")
                
            elif choice == '4':
                stats = farm.get_statistics()
                if stats:
                    print("\n📈 현재 통계:")
                    print(f"   총 기록: {stats['total_records']}개")
                    print(f"   평균 온도: {stats['avg_temp']}℃")
                    print(f"   평균 습도: {stats['avg_humidity']}%")
                    print(f"   환풍기 동작률: {stats['fan_runtime']/stats['total_records']*100:.1f}%")
                    print(f"   펌프 동작률: {stats['pump_runtime']/stats['total_records']*100:.1f}%")
                else:
                    print("📊 아직 데이터가 없습니다.")
                
            elif choice == '5':
                print("👋 스마트 팜 시스템을 종료합니다.")
                break
                
            else:
                print("❌ 잘못된 선택입니다.")
                
        except KeyboardInterrupt:
            print("\n👋 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()