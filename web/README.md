# libserver使用指南

## 对游戏逻辑编写者

libserver的设计逻辑是：

> libserver的调用者将自己编写__main__函数，然后通过调用libserver的 start_server 函数将程序控制权移交给libserver。随后libserver将接管程序，同时启动图形化服务器管理界面。在这个管理界面下，房主可以进行一些操作，比如设置规则与人数。当房主按下“开始游戏”按钮时，libserver将控制权让出，程序开始执行游戏逻辑。
>
> 控制权的转让是利用回调函数完成的，简而言之，在调用start_server时，调用者需要将游戏逻辑的启动函数作为参数传递给start_server，这样，libserver做完自己的工作后，就会去调用那个被作为参数传递的游戏逻辑启动函数。

举个例子：

libserver自带的game_logic_example函数可以作为游戏逻辑的启动函数，它的实现是这样的：

```
def game_logic_example(
    player_name,
    player_read_fn,
    player_write_fn,
    max_round,
    allow_zhai,
    allow_jump,
    player_socket
):
    print('game started')
    print('player name: ', player_name)
    print('player read fn: ', player_read_fn)
    print('player write fn: ', player_write_fn)
    print('max round: ', max_round)
    print('allow zhai: ', allow_zhai)
    print('allow jump: ', allow_jump)
    print('player socket: ', player_socket)
```

（如果自己实现游戏逻辑入口函数，参数要与这个example保持一致，防止出现稀奇古怪传参错误）

现在来使用libserver：

```
if __name__ == "__main__":
    start_server(libserver.game_logic_example, '127.0.0.1', 12347)
```

发现libserver启动了一个图形界面，当点击“开始游戏”时，libserver.game_logic_example被调用。

只需要把libserver.game_logic_example做修改，即可实现其他游戏逻辑。

参数含义：

```
player_name,			# N元一维列表，N为玩家个数，保存玩家名
player_read_fn,			# N元一维列表，N为玩家个数，保存读取函数
player_write_fn,		# N元一维列表，N为玩家个数，保存写入函数
max_round,			# 最大游玩局数
allow_zhai,			# 允许斋规则
allow_jump,			# 允许跳开规则
player_socket			# N元一维列表，N为玩家个数，保存对所有玩家的socket
```


对其中第二个、第三个参数加以解释：

如果想对玩家编号 i 发网络信息，这样：

`player_write_fn[i]("要发的信息")`

如果要等待并读取玩家编号 i 发来的信息，这样：

`消息 = player_read_fn[i]()`

其他参数意义比较明确，不需要专门解读。


## 对客户端编写者

先建立TCP连接，之后需要马上发一段字符串，代表自己的名字，随后服务器就会正式将此客户端加入玩家列表。随后正常通信。
