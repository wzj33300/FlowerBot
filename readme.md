## Flower Bot

魔改自原仓库。

Flower Bot 是一个实现 [Codeforces](https://codeforces.com) 单挑的 QQ Bot。使用框架为 [Mirai](https://github.com/mamoe/mirai) 和 [Alicebot](https://docs.alicebot.dev/)。

水平有限，写的比较垃圾，欢迎提出改进建议。

~~欢迎加 qq 群：213035996 使用~~

# 部署教程

1. 部署 Mirai

使用 [mcl-installer](https://github.com/iTXTech/mcl-installer) 一键安装。

需要的插件如下：
- chat-command
- mirai-api-http
- mirai-login-solver-sakura (验证码解决器)
- 签名插件

如果在服务器上配置，需要修改 `mcl` 或 `mcl.cmd`，在 `-jar mcl.jar` 前面加上 `-Dmirai.no-desktop=true`。

将 `./config/net.mamoe.mirai-api-http/setting.yml` 修改成：
```
adapters:
  - ws
enableVerify: true
verifyKey: 1234567890
adapterSettings:
  ws:
    host: localhost
    port: 8080
    reservedSyncId: -1
```
端口可以自由更改，在 bot 侧同步更改就行。

配置好签名服务后，登录账号，记得用命令给予权限，类似：

```
perm add g* net.mamoe.mirai.console.chat-command:*
```

2. 部署 FlowerBot

将项目 `clone` 下来，修改 `plugins/FlowerCore/configs.py`, `plugins/authconfigs.py`, `config.toml`，可能还需要修改多个文件的输出字符串中的身份内容（改成你自己的）。

要指定监听端口，请在 `config.toml` 中 `[adapter.mirai]` 后添加一行：
```
port = 指定的端口
```

python 安装依赖，包括：
- alicebot[mirai]
- pygame
- watchfiles (热加载)

在 `plugins\FlowerCore` 下面有一个 `storage` 文件夹，用于存放数据，结构如下（我不知道不建会不会有影响）：
```
storage
├── admin.json
├── blacklist.json
├── groupauth.json
├── memory.pkl
└── wordle.json
```

然后使用下面命令启动：
```
python main.py
```
如果没找到 `python` 可以尝试 `python3`。

全部搞好之后，将机器人拉进群里面，输入 `\ciallo`，机器人有回应即成功。