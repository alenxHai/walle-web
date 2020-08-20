# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2019 walle-web.io
    :created time: 2018-12-23 20:17:14
    :author: wushuiyong@walle-web.io
"""
import json

import requests
from . import Notice
from walle.model.project import ProjectModel


class Dingding(Notice):

    def deploy_task(self, project_info, notice_info):
        if notice_info['repo_mode'] == ProjectModel.repo_mode_tag:
            version = notice_info['tag']
        else:
            version = '{branch}/{commit}'.format(branch=notice_info['branch'], commit=notice_info['commit'])
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "上线单通知",
                "text": """#### ![screenshot](http://walle-web.io/dingding.jpg) {username} {title}  \n
                > **项目**：{project_name} \n
                > **任务**：{task_name} \n
                > **版本**：{version} \n """.format(
                    username=notice_info['username'], itle=notice_info['title'],
                    project_name=notice_info['project_name'], task_name=notice_info['task_name'], version=version
                )
            }
        }
        '''
        上线单新建, 上线完成, 上线失败

        @param hook:
        @param notice_info:
            'title',
            'username',
            'project_name',
            'task_name',
            'branch',
            'commit',
            'is_branch',
        @return:
        '''
        headers = {'Content-Type': 'application/json;charset=UTF-8'}
        for hook in project_info['notice_hook'].split(';'):
            response = requests.post(hook, data=json.dumps(data).encode('utf-8'), headers=headers)
            # @todo增加可能错误到console中显示

        return True
