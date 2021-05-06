

# 联系客服索引创建
from es_data.es_conf import es_con

mappings = {
    "mappings": {
        "properties": {
            # 问题
            "problem": {
                "type": "keyword"
            },
            # 创建时间
            "createTime": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
            },
            # 答案
            "answerContent": {
                "type": "text"
            },
            # 答案类型
            "answerType": {
                "type": "integer"
            },
            # 答案次数
            "answerNumber": {
                "type": "integer"
            },
            # role
            "phone": {
                "type": "text"
            }
        }
    }
}

result = es_con.indices.create(index='v2_customer_service', body=mappings)
# print(result)

li = ["v2_user_agreement", "v2_user_guide", "v2_about_us"]
# create index
for i in li:
    mappings = {
        "mappings": {
            "properties": {
                # 内容
                "context": {
                    "type": "keyword"
                },
                # 创建时间
                "createTime": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                },
                # 角色
                "phone": {
                    "type": "text"
                }
            }
        }
    }

    es_con.indices.create(index=i, body=mappings)
