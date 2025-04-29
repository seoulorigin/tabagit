import requests
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


# 공공데이터 API 정보
API_KEY = "MK4/TKoYQDeUyiqfOsHsd5+JsbFMsveVxsy5XfVXeth+vaSozHr/iPRO3vux61l/66nvxvSieCjLjJkwA2LNJQ=="
BASE_URL = "https://api.odcloud.kr/api/15060181/v1/uddi:f6ad9422-d80a-4984-b4b3-dde66d3f59f6"


# 데이터 요청
params = {
    "serviceKey": API_KEY,
    "page": 1,
    "perPage": 100
}


response = requests.get(BASE_URL, params=params)
response.raise_for_status()  # 요청 실패하면 예외 발생
response_data = response.json()


data_list = response_data['data'] #전체 JSON 중 'data'만 가져오기
first_station_info = response_data['data'][0] #리스트 안 첫번째 승차역 정보만 가져오기
print(first_station_info)


# 월별 데이터 추출
if 'data' in response_data and len(response_data['data']) > 0:
    row = response_data['data'][0]
    monthly_usage = {key: int(value) for key, value in row.items() if '년' in key and '월' in key}

    # 월별 데이터 정렬
    months, counts = zip(*sorted(monthly_usage.items()))

    # 그래프 그리기
    plt.figure(figsize=(12, 6))
    plt.bar(months, counts, color='salmon')
    plt.title("월별 이용자 수")
    plt.xlabel("월")
    plt.ylabel("이용자 수")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("데이터가 없습니다:", response_data)

