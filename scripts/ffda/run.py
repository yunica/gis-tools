import json
import click
from ..utils import code as utils


@click.group(chain=True)
def cli():
    click.echo(click.style('Scripts for FFDA!', fg='green'))
    click.echo(click.style('======================', fg='green'))
    pass

    # process data


@cli.command('field_separate')
@click.option("--file", "-in", "in_file", required=True,
              help="Path to geojson.", )
@click.option("--field", "-f", "field", default='label', show_default=True,
              help="Field name of separate.", )
@click.option("--arr_fields", "-af", "arr_fields", required=True,
              help="new field name of separate for fields, separate for ',' ", )
def field_separate(in_file, field, arr_fields):
    """
    Convert gfw json 2 geojson
    """
    with open(in_file, 'r') as json_file:
        json_data = json.load(json_file)
        features = []
        salida_test = []

        with click.progressbar(json_data['features'], label='Process data') as bar:
            arr_fields = [i for i in arr_fields.split(',') if i]
            for k, geo in enumerate(bar):
                # properties = i['properties']
                otest = {'id': k, 'o': geo['properties'][field], 'new': []}
                geo['id'] = k
                for indx, field_t in enumerate(arr_fields):
                    geo['properties'][f'{field_t.strip()}'] = geo['properties'][field][indx]
                    otest['new'].append(geo['properties'][field][indx])
                del (geo['properties'][field])
                features.append(geo)
                salida_test.append(otest)

        with click.progressbar(label='save data', length=1) as bar:
            for i in bar:
                json_data['features'] = features
                new_name = in_file.replace('.geojson', '_separate.geojson')
                utils.save_json(new_name, json_data)
                bar.update(1)

        # errors = [i['id'] for i in salida_test if not i['o'] == i['new']]
        # if errors:
        #     click.echo(click.style('======= ERROR =======', fg='red'))
        #     for i in errors:
        #         print(i, end=' - ')


@cli.command('field_agrupate')
@click.option("--file", "-in", "in_file", required=True,
              help="Path to geojson.", )
@click.option("--field", "-f", "field", default='label', show_default=True,
              help="Field name of separate.", )
@click.option("--arr_fields", "-af", "arr_fields", required=True,
              help="new field name of separate for fields, separate for ',' ", )
def field_agrupate(in_file, field, arr_fields):
    """
    Convert gfw json 2 geojson
    """
    with open(in_file, 'r') as json_file:
        json_data = json.load(json_file)
        features = []

        with click.progressbar(json_data['features'], label='Process data') as bar:
            arr_fields = [i for i in arr_fields.split(',') if i]
            for geo in bar:
                new_field = []
                for field_t in arr_fields:
                    new_field.append(geo['properties'][f'{field_t.strip()}'])
                    del (geo['properties'][field_t])
                geo['properties'][field] = new_field
                features.append(geo)

        with click.progressbar(label='save data', length=1) as bar:
            for i in bar:
                json_data['features'] = features
                new_name = in_file.replace('.geojson', '_agrupate.geojson')
                utils.save_json(new_name, json_data)
                bar.update(1)


@cli.command('field_validate')
@click.option("--file", "-in", "in_file", required=True,
              help="Path to geojson.", )
@click.option("--arr_fields", "-af", "arr_fields", required=True,
              help="fields for validate, separate for ','  except: background ", )
@click.option("--back", "-b", "background", default='background', show_default=True,
              help="field for background", )
def field_validate(in_file, arr_fields, background, ):
    """
    validate geojson if  tag labels aren't conflict
    """
    with open(in_file, 'r') as json_file:
        json_data = json.load(json_file)
        features_error = []

        with click.progressbar(json_data['features'], label='Process data') as bar:
            arr_fields = [i for i in arr_fields.split(',') if i]
            max_sum = len(arr_fields)
            for geo in bar:
                suma = 0
                for field_t in arr_fields:
                    suma += int(geo['properties'][f'{field_t.strip()}'])

                if int(geo['properties'][f'{background.strip()}']):
                    if suma:
                        features_error.append(geo)
                else:
                    if not suma:
                        features_error.append(geo)

        errors = [f'{i["id"]} ({i["properties"]["tile"]})' for i in features_error]
        if errors:
            click.echo(click.style('======= ERROR =======', fg='red'))
            for i in errors:
                print(i, end=' -- ')


if __name__ == '__main__':
    cli()
