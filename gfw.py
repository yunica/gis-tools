import json
import click
import utils
import pandas as pd


# from scripts.utils import save_json

@click.group(chain=True)
def cli():
    click.echo(click.style('Scripts for GFW!', fg='green'))
    click.echo(click.style('======================', fg='green'))
    pass

    # process data


def process_json2geojson(i, k, data_out, data_err):
    ii = {"type": "Feature", 'id': k, "properties": {}, "geometry": {"type": "Point", "coordinates": []}}
    ii['properties'] = i
    if i['interpolated_location'] and i['interpolated_location']['lon']:
        cord = i['interpolated_location']
        ii['geometry']['coordinates'] = [cord['lon'], cord['lat']]
        data_out.append(ii)
    else:
        data_err.append(ii)


def process_json2geojson_next_prev(i, k, data_out, data_err, data_out_next, data_out_prev):
    ii = {"type": "Feature", 'id': k, "properties": {}, "geometry": {"type": "Point", "coordinates": []}}
    # del i['interpolated_location']
    ii['properties'] = i
    cord_prev = i['prev_message']
    cord_next = i['next_message']
    cord = i['interpolated_location']
    if cord and cord['lon']:
        ii['geometry']['coordinates'] = [cord['lon'], cord['lat']]
        data_out.append(ii)
    else:
        data_err.append(ii)

    if cord_prev and cord_prev['lon']:
        ii['geometry']['coordinates'] = [cord_prev['lon'], cord_prev['lat']]
        data_out_prev.append(ii)

    if cord_next and cord_next['lon']:
        ii['geometry']['coordinates'] = [cord_next['lon'], cord_next['lat']]
        data_out_next.append(ii)


def process_count(i, data_out, data_err, data_out_names, data_err_name):
    scene_id = str(i['scene_id']).strip()

    if scene_id in data_out_names and i['interpolated_location']:
        for j in data_out:
            if scene_id == str(j['scene_id']).strip():
                j['count'] += 1
    elif not (scene_id in data_out_names) and i['interpolated_location']:
        data_out_names.append(scene_id)
        ii = {"scene_id": scene_id, "count": 1}
        data_out.append(ii)
    elif (scene_id in data_err_name) and not i['interpolated_location']:
        for j in data_err:
            if scene_id == str(j['scene_id']).strip():
                j['count'] += 1
    else:
        data_err_name.append(scene_id)
        ii = {"scene_id": scene_id, "count": 1}
        data_err.append(ii)


@cli.command('json2geojson')
@click.option("--file", "-f", "in_file", required=True,
              help="Path to json file to be processed.", )
def run_json2geojson(in_file):
    with open(in_file, 'r') as json_file:
        json_data = json.load(json_file)
        data_out = {"type": "FeatureCollection", "features": []}
        data_err = []

        with click.progressbar(json_data, label='Process data') as bar:
            for k, i in enumerate(bar):
                process_json2geojson(i, k, data_out['features'], data_err)

        with click.progressbar(label='save data', length=1) as bar:
            for i in bar:
                new_name = in_file.replace('.json', '_data.geojson')
                utils.save_json(new_name, data_out)

        with click.progressbar(data_err, label='save errors', length=1) as bar:
            for i in bar:
                new_name = in_file.replace('.json', '_errors.json')
                utils.save_json(new_name, data_err)
                bar.update(1)


@cli.command('json2geojson_next_prev')
@click.option("--file", "-f", "in_file", required=True,
              help="Path to json file to be processed.", )
def run_json2geojson_next_prev(in_file):
    with open(in_file, 'r') as json_file:
        json_data = json.load(json_file)
        data_out = {"type": "FeatureCollection", "features": []}
        data_err = []
        data_out_next = {"type": "FeatureCollection", "features": []}
        data_out_prev = {"type": "FeatureCollection", "features": []}

        with click.progressbar(json_data, label='Process data',
                               length=len(json_data)) as bar:
            for k, i in enumerate(bar):
                process_json2geojson_next_prev(i, k, data_out['features'], data_err, data_out_next['features'],
                                               data_out_prev['features'])

        with click.progressbar(data_out, label='save data', length=1) as bar:
            for i in bar:
                new_name = in_file.replace('.json', '_data.geojson')
                utils.save_json(new_name, data_out)
                bar.update(1)

        with click.progressbar(data_out_next, label='save next', length=1) as bar:
            for i in bar:
                new_name = in_file.replace('.json', '_data_next.geojson')
                utils.save_json(new_name, data_out_next)
                bar.update(1)

        with click.progressbar(data_out_prev, label='save prev', length=1) as bar:
            for i in bar:
                new_name = in_file.replace('.json', '_data_prev.geojson')
                utils.save_json(new_name, data_out_prev)
                bar.update(1)

        with click.progressbar(data_err, label='save errors', length=1) as bar:
            for i in bar:
                new_name = in_file.replace('.json', '_errors.json')
                utils.save_json(new_name, data_err)
                bar.update(1)


@cli.command('count_escene')
@click.option("--file", "-f", "in_file", required=True,
              help="Path to json file to be processed.", )
def run_count(in_file):
    with open(in_file, 'r') as json_file:
        json_data = json.load(json_file)
        data_out = []
        data_err = []
        data_out_names = []
        data_err_name = []
        with click.progressbar(json_data, label='Process data',
                               length=len(json_data)) as bar:
            for k, i in enumerate(bar):
                process_count(i, data_out, data_err, data_out_names, data_err_name)

        with click.progressbar(data_out, label='save count', length=1) as bar:
            for i in bar:
                new_name = in_file.replace('.json', '_data_count.json')
                utils.save_json(new_name, data_out)
                bar.update(1)
        with click.progressbar(data_err, label='save count', length=1) as bar:
            for i in bar:
                new_name = in_file.replace('.json', '_data_count_err.json')
                utils.save_json(new_name, data_err)
                bar.update(1)


# @click.command()
# def run_agrupador(in_file):
#     with open(in_file, 'r') as json_file:
#         json_data = json.load(json_file)
#         data_out = []
#         with click.progressbar(json_data, label='Process data',
#                                length=len(json_data)) as bar:
#             x_temp = {'count': 0, 'scenes': []}
#             for i in bar:
#                 x_temp['scenes'].append(i)
#                 x_temp['count'] += i['count']
#
#                 if x_temp['count'] > 1499:
#                     data_out.append(x_temp)
#                     x_temp = {'count': 0, 'scenes': []}
#
#             print('save json')
#             save_json(data_out, 'gfw_data_agrupated')
#             print(len(data_out))

def process_filter_8(i, data_out):
    scene_id = str(i['scene_id']).strip()
    if i['count'] >= 2000:
        data_out[0]['count'] += i['count']
        data_out[0]['escenes_count'] += 1
        data_out[0]['scenes'].append(scene_id)
    elif 2000 > i['count'] and i['count'] >= 1000:
        data_out[1]['count'] += i['count']
        data_out[1]['escenes_count'] += 1
        data_out[1]['scenes'].append(scene_id)
    elif 1000 > i['count'] and i['count'] >= 900:
        data_out[2]['count'] += i['count']
        data_out[2]['escenes_count'] += 1
        data_out[2]['scenes'].append(scene_id)
    elif 900 > i['count'] and i['count'] >= 800:
        data_out[3]['count'] += i['count']
        data_out[3]['escenes_count'] += 1
        data_out[3]['scenes'].append(scene_id)
    elif 800 > i['count'] and i['count'] >= 700:
        data_out[4]['count'] += i['count']
        data_out[4]['escenes_count'] += 1
        data_out[4]['scenes'].append(scene_id)
    elif 700 > i['count'] and i['count'] >= 600:
        data_out[5]['count'] += i['count']
        data_out[5]['escenes_count'] += 1
        data_out[5]['scenes'].append(scene_id)
    elif 600 > i['count'] and i['count'] >= 500:
        data_out[6]['count'] += i['count']
        data_out[6]['escenes_count'] += 1
        data_out[6]['scenes'].append(scene_id)
    elif 500 > i['count']:
        data_out[7]['count'] += i['count']
        data_out[7]['escenes_count'] += 1
        data_out[7]['scenes'].append(scene_id)


@cli.command('group_8')
@click.option("--file", "-f", "in_file", required=True,
              help="Path to json file to be processed.", )
def run_group_8(in_file):
    with open(in_file, 'r') as json_file:
        json_data = json.load(json_file)
        # data count
        data_out_count = []
        data_err = []
        data_out_names = []
        data_err_name = []
        with click.progressbar(json_data, label='Process data count ',
                               length=len(json_data)) as bar:
            for k, i in enumerate(bar):
                process_count(i, data_out_count, data_err, data_out_names, data_err_name)

        # process data count

        data_out = [{'name': '2000>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                    {'name': '2000>1000>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                    {'name': '1000>900>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                    {'name': '900>800>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                    {'name': '800>700>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                    {'name': '700>600>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                    {'name': '600>500>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                    {'name': '500>', 'count': 0, 'escenes_count': 0, 'scenes': []}]
        with click.progressbar(data_out_count, label='Process data filter',
                               length=len(data_out_count)) as bar:
            for i in bar:
                process_filter_8(i, data_out)

        with click.progressbar(data_out, label='save group', length=1) as bar:
            for i in bar:
                new_name = in_file.replace('.json', '_data_group_8.json')
                new_data = utils.order_dict(data_out)
                utils.save_json(new_name, new_data)
                bar.update(1)


@cli.command('group_8_split')
@click.option("--file", "-f", "in_file", required=True,
              help="Path to json file to be processed.", )
def run_goup_8_split(in_file):
    with open(in_file, 'r') as json_file:
        json_data = json.load(json_file)

        # data count
        data_out_count = []
        data_err = []
        data_out_names = []
        data_err_name = []
        with click.progressbar(json_data, label='Process data count ',
                               length=len(json_data)) as bar:
            for k, i in enumerate(bar):
                process_count(i, data_out_count, data_err, data_out_names, data_err_name)

        data_out_mask = [{'name': '2000>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                         {'name': '2000>1000>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                         {'name': '1000>900>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                         {'name': '900>800>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                         {'name': '800>700>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                         {'name': '700>600>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                         {'name': '600>500>=', 'count': 0, 'escenes_count': 0, 'scenes': []},
                         {'name': '500>', 'count': 0, 'escenes_count': 0, 'scenes': []}]
        with click.progressbar(data_out_count, label='Process data mark',
                               length=len(data_out_count)) as bar:
            for i in bar:
                process_filter_8(i, data_out_mask)

        data_out = [
            {'name': '2000>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '2000>1000>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '1000>900>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '900>800>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '800>700>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '700>600>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '600>500>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '500>', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}}]
        data_err = [{'name': '2000>=', 'count': 0, 'scenes': []},
                    {'name': '2000>1000>=', 'count': 0, 'scenes': []},
                    {'name': '1000>900>=', 'count': 0, 'scenes': []},
                    {'name': '900>800>=', 'count': 0, 'scenes': []},
                    {'name': '800>700>=', 'count': 0, 'scenes': []},
                    {'name': '700>600>=', 'count': 0, 'scenes': []},
                    {'name': '600>500>=', 'count': 0, 'scenes': []},
                    {'name': '500>', 'count': 0, 'scenes': []}]
        data_err_gen = []
        data_out_next = [
            {'name': '2000>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '2000>1000>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '1000>900>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '900>800>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '800>700>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '700>600>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '600>500>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '500>', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}}]
        data_out_prev = [
            {'name': '2000>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '2000>1000>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '1000>900>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '900>800>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '800>700>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '700>600>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '600>500>=', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}},
            {'name': '500>', 'count': 0, 'scenes': {"type": "FeatureCollection", "features": []}}]

        with click.progressbar(json_data, label='Process data filtered', length=len(json_data)) as bar:
            for k, i in enumerate(bar):
                geojson = {"type": "Feature", 'id': k, "properties": {},
                           "geometry": {"type": "Point", "coordinates": []}}
                geojson['properties'] = i
                cord_prev = i['prev_message']
                cord_next = i['next_message']
                cord = i['interpolated_location']
                index = None
                for j, l in enumerate(data_out_mask):
                    if str(i['scene_id']).strip() in l['scenes']:
                        index = j
                        break

                if index or (index is 0):
                    if cord and cord['lon']:
                        geojson['geometry']['coordinates'] = [cord['lon'], cord['lat']]
                        data_out[index]['count'] += 1
                        data_out[index]['scenes']['features'].append(geojson)
                    else:
                        data_err[index]['count'] += 1
                        data_err[index]['scenes'].append(geojson)
                    if cord_prev and cord_prev['lon']:
                        geojson['geometry']['coordinates'] = [cord_prev['lon'], cord_prev['lat']]
                        data_out_prev[index]['count'] += 1
                        data_out_prev[index]['scenes']['features'].append(geojson)

                    if cord_next and cord_next['lon']:
                        geojson['geometry']['coordinates'] = [cord_next['lon'], cord_next['lat']]
                        data_out_next[index]['count'] += 1
                        data_out_next[index]['scenes']['features'].append(geojson)
                else:
                    data_err_gen.append(geojson)

        with click.progressbar(data_out_mask, label='save split mask', length=1) as bar:
            for i in bar:
                new_name = in_file.replace('.json', '_data_group_8.json')
                new_data = utils.order_dict(data_out_mask)
                utils.save_json(new_name, new_data)
                bar.update(1)

        with click.progressbar(data_out, label='save data_out', length=len(data_out)) as bar:
            for i in bar:
                count = i['count']
                name = i['name']
                new_name = in_file.replace('.json', f'_data_split_{name}-c{count}.geojson')
                utils.save_json(new_name, i['scenes'])

        with click.progressbar(data_out_next, label='save data_out_next', length=len(data_out_next)) as bar:
            for i in bar:
                count = i['count']
                name = i['name']
                new_name = in_file.replace('.json', f'_data_split_next_{name}-c{count}.geojson')
                utils.save_json(new_name, i['scenes'])

        with click.progressbar(data_out_prev, label='save data_out_prev', length=len(data_out_prev)) as bar:
            for i in bar:
                count = i['count']
                name = i['name']
                new_name = in_file.replace('.json', f'_data_split_prev_{name}-c{count}.geojson')
                utils.save_json(new_name, i['scenes'])

        with click.progressbar(data_err, label='save data_err', length=len(data_err)) as bar:
            for i in bar:
                count = i['count']
                name = i['name']
                new_name = in_file.replace('.json', f'_data_split_err_{name}-c{count}.json')
                utils.save_json(new_name, i['scenes'])

        with click.progressbar(data_err_gen, label='save error generic', length=1) as bar:
            for i in bar:
                new_name = in_file.replace('.json', '_data_count_err_split.json')
                utils.save_json(new_name, data_err_gen)
                bar.update(1)


if __name__ == '__main__':
    cli()
