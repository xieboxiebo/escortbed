from es_data.es_conf import es_con

actions = [
    {
    'problem': '退款申请后什么时候到账？',
    'createTime': '2020-10-27 13:35:34',
    'answerContent': '如您已线上提交退款申请，请您耐心等待，无需再次来电。款项预估将于7个工作日内原路退回。',
    'answerType': 1,
    'answerNumber': 1,
    "phone": '123456789'
    },
    {
    'problem': '订单如何取消？',
    'createTime': '2020-10-27 13:36:34',
    'answerContent': '1、取消订单操作：\n登录小程序，点击页面右下方【我的】-【我的订单】，点击需要取消的订单，进入【订单详情】页面后点击左下角【申请退款】按钮，选择退款原因后完成提交。',
    'answerType': 2,
    'answerNumber': 2,
    "phone": '123456789'
    },
    {
    'problem': '如何开具电子发票？',
    'createTime': '2020-10-27 13:38:34',
    'answerContent': '在【已完成】中，点击订单结算页【发票】，选择发票类型为【电子普通发票】。',
    'answerType': 3,
    'answerNumber': 3,
    "phone": '123123456'
    },
    {
    'problem': '如何查看订单编号？',
    'createTime': '2020-10-27 13:40:34',
    'answerContent': '1、打开小程序，点击“我的订单”\n2、或者点击查看全部订单\n3、点击要查看订单编号的物品\n4、下拉即可看到订单编号。',
    'answerType': 4,
    'answerNumber': 4,
    "phone": '123123456'
    },
    {
    'problem': '如何退押金？',
    'createTime': '2020-10-27 13:41:34',
    'answerContent': '1、点击【押金】页面。\n2、点击【退还押金】',
    'answerType': 5,
    'answerNumber': 5,
    "phone": '7897897890'
    },
    {
    'problem': '已关锁未结束计费？',
    'createTime': '2020-10-27 13:42:34',
    'answerContent': '因信号可能稍有延迟，麻烦您稍等片刻。若关锁一段时间后仍未结束计费，请点击【强制结束计费】，并拍照上传设备编号。',
    'answerType': 6,
    'answerNumber': 6,
    "phone": '7897897890'
    },
    {
    'problem': '如何退还金额？',
    'createTime': '2020-10-27 13:43:34',
    'answerContent': '点击【金额】——一【退还余额】，一般会安排原路退回，即银行卡支付退回银行卡，微信支付退回支付银行卡或微信零钱，余额退回余额；',
    'answerType': 7,
    'answerNumber': 7,
    "phone": '7654321333'
    },
    {
    'problem': '忘记关锁，怎么办？',
    'createTime': '2020-10-27 13:46:34',
    'answerContent': '护理床忘记关锁很容易造成护理床丢失或被破坏，同时也会影响您的个人信用，请后续用车不要忘记哦~如您目前已发生该问题，请您及时申报忘记关锁，我们将安排工作人员寻找护理床并处理您的订单。',
    'answerType': 8,
    'answerNumber': 8,
    "phone": '7654321333'
    },
]

for action in actions:
    result = es_con.index(index="v2_customer_service", body=action)
    print(result, end='\n')
