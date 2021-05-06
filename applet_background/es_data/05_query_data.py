from es_data.es_conf import es_con



def query_index(index):
    '''
    查询所有

    data_agg = es_con.search(
        index=index,
        size=1000,
        body={
            "query": {
                "match_all": {}
            },
        }
    )
    '''
    data_agg = es_con.search(
        index=index,
        size=1000,
        body={
            "query": {
                "match_all": {}
            },
        }
    )
    print(data_agg, '666666666')

    for data in data_agg.get('hits').get('hits'):
        list_data = data.get('_source')
        if '' in list(list_data.values()):
            print(list_data)
            id_ = data.get('_id')
            # es_con.delete(index='base_data', id=id_)
        else:
            pass
        # print(list_data)

for index in ["v2_customer_service", "v2_user_agreement", "v2_user_guide", "v2_about_us"]:
    print(index.center(60, "-"))
    query_index(index)
    print(index.center(60, "-"))