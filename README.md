# pyjy

Pyjy is a Python implementation of the classic 2D RPG game "JinYongQunXiaZhuan" (金庸群侠传), a renowned Chinese game.

The goal of this project is to integrate Large Language Models (LLMs) into the game, allowing the non-player characters (NPCs) to think and act autonomously.

As most developers interested in this project are likely Chinese, the following README content is in Chinese.

---

本项目是《金庸群侠传》的一个 Python 开源实现。项目中需要使用《金庸群侠传》的原版素材，请开发者们自行提供。

本项目遵从 MIT 开源协议，开源协议仅覆盖本项目的原创代码部分。任何涉及《金庸群侠传》的版权归属于原开发公司智冠科技。

本项目的基础游戏部分深受另一个同类型开源项目 kys-cpp 影响，其中大部分实现也是参考该项目：https://github.com/scarsty/kys-cpp.git

本项目的目标是将金庸先生的武侠世界连接到当前蓬勃发展的生成式人工智能（GenAI）上，通过大语言模型（LLM）来驱动游戏中的 NPC。

## 项目运行

目前项目刚开始，启动也比较简单：

1. 克隆或下载本项目代码。
2. 找到《金庸群侠传》的原版软件，将 `resource`, `music`, `save` 这几个个目录拷贝到本项目的 `original_resource` 目录中。拷贝完成后的目录结构如下：
   ```
   pyjy
   |-----original_resource
          |-----music
          |-----resource
          |-----save
   ```
3. 进入 `pyjy` 目录，运行 `python ./main.py`

4. 开始游戏

目前只实现了84个子场景，在场景中通过方向键移动。
然后`z`键切换到上一个场景，`x`键切换到下一个场景

