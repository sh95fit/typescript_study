import boto3
from boto3.dynamodb.conditions import Key
import os
from dotenv import load_dotenv
from datetime import datetime
import pytz
import json
from decimal import Decimal

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("AWS_REGION")
tables_str = os.getenv("DYNAMODB_TABLES")
table_list = [table.strip() for table in tables_str.split(',')]

dynamodb = boto3.resource("dynamodb",
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=region_name)

kst = pytz.timezone('Asia/Seoul')

# naive datetime (시간대 정보 없는)
start_naive = datetime(2025, 6, 16, 0, 0, 0)
end_naive = datetime(2025, 6, 16, 23, 59, 59)

# 현지 시간으로 변환 (localized)
start_kst = kst.localize(start_naive)
end_kst = kst.localize(end_naive)

# UTC로 변환
start_utc = start_kst.astimezone(pytz.utc)
end_utc = end_kst.astimezone(pytz.utc)

# 유닉스 타임스탬프로 변환
start_date = int(start_kst.timestamp()*1000)
end_date = int(end_kst.timestamp()*1000)

print(start_date, end_date)
print(table_list[7])

# 테이블 목록 확인
# for table in dynamodb.tables.all():
#     print(table.name)
   
   
# 메세지 생성 테이블 조회 
# table = dynamodb.Table(table_list[3])
# res = table.query(
#     IndexName='SendDateCreatedAtIndex',
#     KeyConditionExpression=Key('sendDate').eq('2025/6/9')&Key('createdAt').between(start_date, end_date)
# )

# 발송된 메시지 테이블 조회 
table = dynamodb.Table(table_list[7])
res = table.query(
    IndexName='SendStatusIndex',
    KeyConditionExpression = Key('sendStatus').eq('sent') & Key('createdAt').between(start_date, end_date)
)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            else:
                return float(obj)
        return super(DecimalEncoder, self).default(obj)

items = res.get('Items', [])

if not items:
    print("조회된 데이터가 없습니다.")
else:
    # 1) 각 아이템을 보기 좋게 출력
    for i, item in enumerate(items, 1):
        print(f"=== Item {i} ===")
        for key, value in item.items():
            print(f"{key}: {value}")
        print()

    # 2) 또는 JSON 포맷으로 한 번에 예쁘게 출력하기 (필요 시)
    print(json.dumps(items, indent=4, ensure_ascii=False, cls=DecimalEncoder))
