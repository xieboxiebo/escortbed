from django.test import TestCase

# Create your tests here.
from applet_background.link_config import con_mysql

con_mysql_connect = con_mysql.connection()
cursor = con_mysql_connect.cursor()
cursor.execute("SELECT orderId, hosName, userName,phoneNumber,amountMoney,user_payment.`agentName`, raiseTime FROM"
               " user_payment , hos_list  WHERE user_payment.`deviceId` = hos_list.`deviceId`"
               " and user_payment.`type` = '押金' ORDER BY raiseTime DESC")
data = cursor.fetchall()
cursor.close()
con_mysql_connect.close()
return_list = list()
for data_ in data:
    return_list.append(
        {
            'orderId': data_[0],
            'hoaName': data_[1],
            'userName': data_[2],
            'phoneNumber': data_[3],
            'money': data_[4],
            'agentName': data_[5],
            'createTime': data_[6]
        }
    )
