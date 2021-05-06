import base64
import hmac
import time

from applet_background.link_config import redis_con


def redis_set_func(key_data, dict_data):
    """
    插入数据到redis
    :param key_data:  哈希的key
    :param dict_data: 字典格式，哈希的字段和值
    :return: 插入后的状态
    """
    # 插入数据到redis
    return_status = redis_con.hmset(key_data, dict_data)
    return return_status


def redis_get_func(hs_key):
    """
    读取redis数据，获取哈希的数据
    :param hs_key: 哈希的key
    :return:
    """
    return_data = redis_con.hgetall(hs_key)

    return return_data


def redis_delete_func(hs_key, *args):
    """

    :param hs_key: 哈希的key
    :param args: 配置参数
    :return: 返回状态
    """
    return_status = redis_con.hdel(hs_key, *args)
    return return_status


def str_to_token(key, expire=60 * 60 * 24 * 15):
    '''
    :param key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
    :param expire: int(最大有效时间，单位为s) 默认时间60天
    :return: token
    '''
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


def token_to_str(key, token):
    '''
    :param key: 服务器给的固定key
    :param token: 前端传过来的token
    :return: true,false
    '''
    # token是前端传过来的token字符串
    try:
        token_str = base64.urlsafe_b64decode(token).decode('utf-8')
        token_list = token_str.split(':')
        if len(token_list) != 2:
            return False
        ts_str = token_list[0]
        if float(ts_str) < time.time():  # 对比时间
            return False
        known_sha1_tsstr = token_list[1]
        sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
        calc_sha1_tsstr = sha1.hexdigest()
        if calc_sha1_tsstr != known_sha1_tsstr:
            return False
        return True
    except KeyError:
        return False
