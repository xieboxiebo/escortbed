import time

from es_data.es_conf import es_con


def actions_func(text, phone):
    actions = {
        'context': phone + '------>' + text,
        'createTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        'phone': phone
        }
    return actions


dics = {"v2_user_agreement": "协议版本：【V3.0】；发布/生效日期：【2020年10月27日】\n欢迎您注册护理床账号并使用护理床的服"
                          "务！\n本《护理床平台用户服务协议》（以下简称“本服务协议”）是您与护理床之间就注册护理床用户"
                          "账号及使用护理床的各项服务等相关事宜所订立的协议。",
        "v2_user_guide": "1、注册，填写注册信息。\n2、缴纳押金。\n3.开始使用护理床。 【V3.0】",
        "v2_about_us": "护理床公司成立于2020，旨在帮助人们更快捷的照顾病人。 【V3.0】"}

for key, value in dics.items():
    time.sleep(1)
    result = es_con.index(index=key, body=actions_func(value, "7654321333"))
    # print(key, value)
    print(result, end='\n')