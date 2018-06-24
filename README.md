# gitee2rundeck-adapter
This adapter run rundeck's job on gitee webhook event

## Requirements:
* python >= 3.4
* tornado 5.0.2
* Rundeck 2.10.8

## 实现方式
收到gitee发过来的POST请求。 根据 `git_ssh_url` 与 `refs` 匹配到 `rundeck`的`job_id`。 然后调用`rundeck`的 `web api`接口。 

程序使用了`tornado`


## 开机启动

```
cat > /usr/lib/systemd/system/gitee2rundeck-adapter.service <<EOF
[Unit]
Description=gitee2rundeck-adapter
After=network.target

[Service]
ExecStart=/opt/server/gitee2rundeck-adapter/py3/bin/python /opt/server/gitee2rundeck-adapter/server.py
#ExecStop=
User=nobody
Group=nobody

[Install]
WantedBy=multi-user.target

EOF

systemctl enable gitee2rundeck-adapter

```


## todo
[] 使用独立配置文件

[] 完善文档
