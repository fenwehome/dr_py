#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : vod.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/9/6
import functools
import json

from flask import Blueprint, abort, request, render_template, send_from_directory, render_template_string, jsonify, \
    make_response, redirect, \
    current_app
from time import time
from utils.web import getParmas, get_interval
from utils.cfg import cfg
from utils.env import get_env
from js.rules import getRuleLists, getJxs
from base.R import R
from utils.log import logger
from utils import parser
from controllers.cms import CMS
from base.database import db
from models.ruleclass import RuleClass
from models.playparse import PlayParse
from js.rules import getRules
from controllers.service import storage_service, rules_service
from concurrent.futures import ThreadPoolExecutor, as_completed, thread  # 引入线程池
from quickjs import Function, Context
import ujson

# web = Blueprint("web", __name__, template_folder='templates/cmsV10/mxpro/html/index/')
web = Blueprint("web", __name__)


@web.route('/cms/<path:filename>')
def custom_static_js(filename):
    # 自定义静态目录 {{ url_for('custom_static',filename='help.txt')}}
    # print(filename)
    return send_from_directory('templates/cms', filename)

@web.route('/<web_name>/<theme>')
def web_index(web_name, theme):
    ctx = {'web_name': web_name, 'key': '关键词', 'description': '描述'}
    lsg = storage_service()
    js0_password = lsg.getItem('JS0_PASSWORD')
    ctx['pwd'] = js0_password
    ctx['path'] = request.path
    ctx['url'] = request.url
    try:
        return render_template(f'cms/{theme}/homeContent.html', ctx=ctx)
    except Exception as e:
        return render_template('404.html', ctx=ctx, error=f'发生错误的原因可能是下面路径未找到:{e}')