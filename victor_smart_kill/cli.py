# -*- coding: utf-8 -*-

"""Console script for victor_smart_kill."""
import os
import sys
import json
import time
import datetime
import click
import requests
import getpass
import victor_smart_kill as vsk

@click.group()
@click.option('-c', '--config', 'config_fname', default=os.path.expanduser("~/.victorsmartkill/config.json"), help='Config file to use')
@click.option('-t', '--token', 'token_fname', default=os.path.expanduser("~/.victorsmartkill/token.json"), help='JSON file to store token in')
@click.pass_context
def cli(ctx, config_fname, token_fname):
    ctx.obj = {"config_fname": config_fname, "token_fname": token_fname}

@cli.command()
@click.pass_obj
def login(ctx):

    vsk.get_token(ctx['config_fname'], ctx['token_fname'])

@cli.command()
@click.pass_obj
def update_config(ctx):
    vsk.update_config(ctx['config_fname'], ctx['token_fname'])

@cli.command()
@click.argument('within', required=False, default=24)
@click.argument('name', required=False, default=None)
@click.pass_obj
def status(ctx, within, name):

    results = vsk.status(ctx['config_fname'], ctx['token_fname'], within, name)

    for trap in results:
        s = "id={0} name='{1}' kills_present={2} last_kill={3} last_report={4}"
        print(s.format(trap['id'], trap['name'], trap['kills_present'], trap['last_kill'], trap['last_report']))

@cli.command()
@click.argument('within', required=False, default=24)
@click.argument('name', required=False, default=None)
@click.pass_obj
def check(ctx, within, name):

    results = vsk.status(ctx['config_fname'], ctx['token_fname'], within, name)
    date_fmt = '%Y-%m-%dT%H:%M:%S.%fZ'

    for trap in results:
        s = "id={0} name='{1}' kills_present={2} last_kill={3} last_report={4}"

        last_report = trap['last_report']
        kills_present = trap['kills_present']
        if kills_present is None:
            kills_present = 0

        last_report_obj = datetime.datetime.strptime(last_report, date_fmt)
        threshold_time = datetime.datetime.now() - datetime.timedelta(hours=within)

        if kills_present > 0 or last_report_obj < threshold_time:
            print(s.format(trap['id'], trap['name'], trap['kills_present'], trap['last_kill'], trap['last_report']))
