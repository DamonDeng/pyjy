# pyjy

Pyjy is a python implementation of a Chinese Game named "JinYongQunXiaZhuan", which is a classic 2D RPG game.

The plan of this project is integrating LLM model into the projec to drive the NPC to think and do by themseves.

As most of the developers who may have interest in this project are Chinese, the following readme content is in Chinese.

本项目是《金庸群侠传》的一个Python开源实现，项目中需要使用《金庸群侠传》的原版素材，请开发者们自行提供。

本项目遵从MIT开源协议，开源协议只覆盖本项目的原创代码部分，任何涉及《金庸群侠传》的版权归属于原开发公司智冠科技。

本项目的基础游戏部分深受另一个同类型开源项目kys-cpp影响，其中大部分实现也是参考该项目：https://github.com/scarsty/kys-cpp.git

本项目的目标是将金庸先生的武侠世界连接到当前蓬勃发展的生成式样人工智能（GenAI）上，通过大语言模型（LLM）来驱动游戏中的NPC

# 项目运行

目前项目刚开始，启动也比较简单

1. 克隆或者下载本项目代码，
2. 找到《金庸群侠传》的原版软件，将resource和save两个目录拷贝到本项目的original_resource目录中。
    拷贝完以后的目录结构如下：
    pyjy
    |-----original_resource
             |
             |-----resource
             |-----save
3. 进入pyjy目录，
运行 `python ./main.py`