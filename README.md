# gitee2rundeck-adapter
This adapter run rundeck's job on gitee webhook event


## 实现方式
收到gitee发过来的POST请求。 根据 `git_ssh_url` 与 `refs` 匹配到 `rundeck`的`job_id`。 然后调用`rundeck`的 `web api`接口。 

程序使用了`tornado`
