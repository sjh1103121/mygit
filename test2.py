from datetime import datetime
from kafka import KafkaProducer
import json
import time
import random
# Kafka 配置
bootstrap_servers = ['172.18.23.101:21005', '172.18.23.102:21005', '172.18.23.103:21005']
topic = 'test_topic'

# 创建 Kafka Producer（不设置 key.serializer，因为不传 key）
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
)

messages_to_send = 30  # 发送 30 条消息

try:
    for i in range(messages_to_send):
        message = {
            "a": f"user_{i}",
            "b": random.randint(100, 999),
            "event_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        #  关键：不传 key，也不传 partition → Kafka 会轮询分配到各 partition
        future = producer.send(topic, value=message)

        # 可选：打印发送信息（避免刷屏可注释掉）
        record_metadata = future.get(timeout=5)
        print(f" [{i+1}/{messages_to_send}] 发送到 partition={record_metadata.partition}, offset={record_metadata.offset}")

        # 可选：加一点间隔，便于观察
        time.sleep(0.01)

except Exception as e:
    print(f" 发送失败: {e}")

finally:
    producer.flush()
    producer.close()
    print(" 所有消息已发送完毕！")
