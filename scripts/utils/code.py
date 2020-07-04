import json


def save_json(name, data):
    with open('./{}'.format(name), 'w') as f:
        json.dump(data, f, ensure_ascii=False )
        f.close()


def order_dict(dict=[], field='count', order=-1):
    order_l = sorted(dict, key=lambda i: order * i[field])
    return order_l
