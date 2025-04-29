from fastapi import FastAPI, Response, Query
import httpx
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib


# 한글 깨짐 방지 설정 (Windows 기준)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False


app = FastAPI()


# 공공데이터 API 정보
API_KEY = "MK4/TKoYQDeUyiqfOsHsd5+JsbFMsveVxsy5XfVXeth+vaSozHr/iPRO3vux61l/66nvxvSieCjLjJkwA2LNJQ=="
BASE_URL = "https://api.odcloud.kr/api/15060181/v1/uddi:f6ad9422-d80a-4984-b4b3-dde66d3f59f6"


# 샘플 확인용
@app.get("/srt-passenger-sample")
async def sample():
    params = {
        "serviceKey": API_KEY,
        "page": 1,
        "perPage": 1
    }
    async with httpx.AsyncClient() as client:
        res = await client.get(BASE_URL, params=params)
        return res.json()


# 그래프 출력: 역 이름 선택 가능
@app.get("/srt-passenger-graph")
async def srt_passenger_graph(station: str = Query(..., description="승차역 이름 예: 수서")):
    params = {
        "serviceKey": API_KEY,
        "page": 1,
        "perPage": 100
    }


    async with httpx.AsyncClient() as client:
        res = await client.get(BASE_URL, params=params)
        res.raise_for_status()
        json_data = res.json()


    data = json_data.get("data", [])
    if not data:
        return {"error": "API로부터 받은 데이터가 없습니다."}


    # 해당 역 찾기
    row = next((item for item in data if item.get("승차역") == station), None)
    if not row:
        return {"error": f"'{station}'에 해당하는 역 데이터를 찾을 수 없습니다."}


    # 월별 데이터 추출
    monthly_data = {k: v for k, v in row.items() if "년" in k}
    sorted_items = sorted(monthly_data.items(), key=lambda x: x[0])
    labels = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]


    # 그래프 그리기
    plt.figure(figsize=(14, 6))
    plt.plot(labels, values, marker='o')
    plt.title(f"{station} 월별 승차 인원 추이")
    plt.xlabel("연월")
    plt.ylabel("승차 인원 수")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()


    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)


    return Response(content=buffer.getvalue(), media_type="image/png")
