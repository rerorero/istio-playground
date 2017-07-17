#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

class FilebaseKubectl:

    def __init__(self, module):
        self.module = module

    def current_resource(self):
        result = self.get()
        if result['out'] is not None:
            return result
        elif result['err'].find('NotFound') >= 0:
            result['rc'] = 0
            result['err'] = None
            return result
        else:
            return result

    def get(self):
        result = self.kubectl_action('get')
        if result['rc'] == 0:
            result['out'] = json.dumps(result['out'])
            return result
        else:
            result['out'] = None
            return result
    
    def kubectl_action(self, action):
        cmd = 'kubectl %s -f "%s"' % (action, self.module.params.get('filepath'))
        rc, out, err = self.module.run_command(cmd, use_unsafe_shell=True)
        return dict(rc=rc, out=out, err=err, changed=0)

    def execute_premise_exists(self, action, expect_exists, ignore):
        cur_result = self.current_resource()
        if cur_result['rc'] != 0:
            return cur_result

        if (not expect_exists) and (cur_result['out'] is None):
            res = self.kubectl_action(action)
            res['changed'] = 1
            return res
        if expect_exists and (cur_result['out'] is not None):
            res = self.kubectl_action(action)
            res['changed'] = 1
            return res
        else:
            if ignore:
                return cur_result
            else:
                cur_result['rc'] = 1
                if expect_exists:
                    cur_result['err'] = 'Not found'
                else:
                    cur_result['err'] = 'Already exists'
                return cur_result

    def execute(self):
        action = self.module.params.get('action')
        if action == 'get':
            return self.get()
        else:
            if action == 'create':
                return self.execute_premise_exists(action, False, False)
            if action == 'present':
                return self.execute_premise_exists('create', False, True)
            elif action == 'delete':
                return self.execute_premise_exists(action, True, False)
            if action == 'absent':
                return self.execute_premise_exists('delete', True, True)
            elif action == 'apply':
                return self.execute_premise_exists(action, True, False)

    def get_output(self, result):
        if result['rc']:
            self.module.fail_json(msg=result['err'], rc=result['rc'], err=result['err'])
        else:
            self.module.exit_json(**result)

def main():
    module = AnsibleModule(
        argument_spec = dict(
            action = dict(required=True, choices=["create", "present", "delete", "absent", "apply", "get"]),
            filepath = dict(required=True)
        )
    )

    kube = FilebaseKubectl(module)
    result = kube.execute()
    kube.get_output(result)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
