from applet_background.link_config import es_con, con_mysql


def per_index_es_all_data(index, phone):
    """
    获取当前索引下的所有数据，并按时间逆序排列
    :param index:
    :param phone:
    :return:
    """
    datas = es_con.search(
        index=index,
        size=1000,
        body={
            "query": {
                "match": {
                    "phone": phone
                }
            },
            "size": 10000,
            "sort": {
                "createTime": {
                    "order": "desc"
                }
            }
        }
    )

    return datas.get("hits").get("hits")


def customer_service_es_data_get(index, phone):
    """
        联系客服——数据获取
    :param index:
    :param phone:
    :return:
    """
    init_datas = per_index_es_all_data(index, phone)
    customer_datas = list()
    problems = list()

    for data in init_datas:
        customer_data = dict()
        tmp = data.get("_source")
        customer_data["problem"] = tmp.get("problem")
        customer_data["answerContent"] = tmp.get("answerContent")
        customer_datas.append(customer_data)
        problems.append(tmp.get("problem"))

    return customer_datas, problems


def customer_service_es_data_insert(text, time_, answer, phone):
    """
    联系客服——数据插入
    :param text:
    :param time_:
    :param answer:
    :param phone:
    :return:
    """
    actions = {
            'problem': text,
            'createTime': time_,
            'answerContent': answer,
            'answerType': 1,
            'answerNumber': 1,
            'phone': phone
        }
    es_con.index(index="v2_customer_service", body=actions)
    return True


def customer_service_es_data_delete(text):
    query = {
        'query':
            {'match':
                 {
                     'problem': text
                 }
             }
    }  # 删除某个客服服务问题的所有文档

    es_con.delete_by_query(index='v2_customer_service', body=query)
    return True


def agree_guide_about_es_data_get(index, phone):
    """
    用户协议 用户指南 关于我们 数据获取
    :param index:
    :param phone:
    :return:
    """
    agree_guide_about_init = per_index_es_all_data(index, phone)
    agree_guide_about_datas = list()
    agree_guide_about_contexts = list()
    for data in agree_guide_about_init:
        agree_guide_about_data = dict()
        tmp = data.get("_source")
        agree_guide_about_data["context"] = tmp.get("context")
        agree_guide_about_data["createTime"] = tmp.get("createTime")
        agree_guide_about_datas.append(agree_guide_about_data)
        agree_guide_about_contexts.append(tmp.get("context"))
    return agree_guide_about_datas[0], agree_guide_about_contexts


def agree_guide_about_es_data_insert(index, text, time_, phone):
    """
    用户协议 用户引导 关于我们数据插入
    :param index:
    :param text:
    :param time_:
    :param phone:
    :return:
    """
    actions = {
        'context': text,
        'createTime': time_,
        'phone': phone
    }
    es_con.index(index=index, body=actions)
    return True


# 数据库函数封装
def sql_func(sql, *args):
    conn = con_mysql.connection()
    cursor = conn.cursor()
    if args:
        cursor.execute(sql, args)
    else:
        cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return data


def check_user_auth_level(user_phone):
    '''
    登录用户权限检查
    :param user_phone:  用户手机号
    :return: 用户等级，代理商等信息
    '''
    sql = "select level, agentId, agentName from manager_list where phoneNumber = " + user_phone
    level = sql_func(sql)
    # print('level', level)
    return level


def feedback_data(agent_name=None, user_phone=None, is_handle=None, page_size=10, page_number=1):
    """
    系统设置——用户反馈
    :param user_phone:
    :param agent_name:
    :param is_handle:
    :param page_size:
    :param page_number:
    :return:
    """

    search_dic = dict()
    if agent_name or user_phone or is_handle:
        if is_handle:
            is_handle = '0' if is_handle == "未处理" else '1'
        search_dic = {"device_compose.`agentName`": agent_name,
                      "feedback.`phoneNumber`": user_phone,
                      "feedback.`isHandle`": is_handle}

    feed_back_data_sql = """select feedback.`deviceId`, feedback.`nickName`, feedback.`phoneNumber`, 
    feedback.`feedbackContent`, feedback.`picLink`, feedback.`raiseTime`, feedback.`isHandle`, 
    device_compose.`agentName`
    from feedback left join device_compose 
    on device_compose.`deviceId`=feedback.`deviceId`
    """

    search_str = ""
    for key, value in search_dic.items():
        if not value:
            pass
        elif value == user_phone:
            search_str += key + " like " + "'" + value + "%'" + " and "
        else:
            search_str += key + " = " + "'" + value + "'" + " and "

    if search_str:
        search_str = search_str.rstrip(" and ")
        sql = feed_back_data_sql + " where " + search_str + " limit " + str(int(page_size) * (int(page_number) - 1)) + \
            ", " + str(int(page_size) * int(page_number))
    else:
        sql = feed_back_data_sql + " limit " + str(int(page_size) * (int(page_number) - 1)) + \
            "," + str(int(page_size) * int(page_number))

    datas = sql_func(sql)
    feed_back_lists = list()
    for data in datas:
        feed_back_dict = {"deviceId": data[0],
                          "nickName": data[1],
                          "phoneNumber": data[2],
                          "feedbackContent": data[3],
                          "picLink": data[4],
                          # "raiseTime": data[5].strftime('%Y-%m-%d %H:%M:%S'),
                          "raiseTime": data[5],
                          "isHandle": "未处理" if data[6] == "0" else "已处理"}
        feed_back_lists.append(feed_back_dict)

    return feed_back_lists


def coupon_datas_get(agent_id=None):
    """
    优惠券数据获取
    :param agent_id:
    :return:
    """
    sql = """SELECT coupon_message.`couponName`, coupon_message.`couponValue`, coupon_message.`count` ,
    coupon_message.`couponEnd`, hos_list.`hosName`, coupon_message.`hosId` 
    FROM coupon_message JOIN hos_list ON hos_list.`agentId` = coupon_message.`agentId` """

    search_sql = ""

    if not agent_id:
        search_sql = sql
    else:
        search_sql = sql + "where coupon_message.`agentId` = " + agent_id
    datas = sql_func(search_sql)
    coupons_lists = list()
    if len(datas) == 0:
        return coupons_lists
    else:
        for data in datas:
            coupon_dic = {
                'couponName': data[0],
                'couponValue': data[1],
                'countNum': data[2],
                'endTime': data[3].split(' ')[0],
                'hosName': data[4],
                'hosId': data[5]
            }
            coupons_lists.append(coupon_dic)
        return coupons_lists


def coupon_info_del(coupon_name):
    pass


if __name__ == '__main__':
    print(coupon_datas_get("103"))


