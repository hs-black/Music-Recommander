# 基于LLM的音乐推荐系统 (Music Recommender)

## 介绍

TODO

## 快速上手

### 1.环境配置

先创建一个 python 版本为 3.10 的 conda 环境
```shell
$ conda create -n music_recommender python=3.10
$ conda activate music_recommender
```

接着安装项目及依赖
```shell
# 克隆项目
$ git clone --recursive https://github.com/hs-black/Music-Recommander.git
$ cd Music-Recommander

# 安装 ChatGLM 库的依赖
$ pip install -r requirements.txt

# 安装 Langchain-Chatchat 库的依赖
$ cd composite_demo/Langchain_Chatchat
$ pip install -r requirements.txt

# 安装 NeteaseCloudMusicApi 库的依赖
$ cd ../../NeteaseCloudMusicApi
$ npm install
```

### 2.模型下载
本项目的本地数据库部分使用 LLM 模型 [THUDM/ChatGLM3-6B](https://huggingface.co/THUDM/chatglm3-6b) 与 Embedding 模型 [BAAI/bge-large-zh](https://huggingface.co/BAAI/bge-large-zh)。

下载模型需要先[安装 Git LFS](https://docs.github.com/zh/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)，然后在 composite_demo/Langchain_Chatchat 下运行

```shell
$ mkdir models
$ cd models
$ git lfs install
$ git clone https://huggingface.co/THUDM/chatglm3-6b
$ git clone https://huggingface.co/BAAI/bge-large-zh
```

### 3.启动项目

按照以下命令依次启动各个子项目

```shell
# 启动 NeteaseCloudMusicApi, 在 NeteaseCloudMusicApi 目录下运行
$ node app.js

# 启动本地数据库, 在 composite_demo/Langchain_Chatchat 目录下运行
$ python startup.py -a

# 启动聊天界面, 在 composite_demo 目录下运行
$ streamlit run main.py
```

一定要等待 Langchain_Chatchat 完全启动后再启动聊天界面。

正常启动后，可在最后一个命令的输出中找到端口，并在浏览器内打开。一般情况下为 localhost:8502。