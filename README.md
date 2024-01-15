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

本项目的本地知识库部分使用 LLM 模型 [THUDM/ChatGLM3-6B](https://huggingface.co/THUDM/chatglm3-6b) 与 Embedding 模型 [BAAI/bge-large-zh](https://huggingface.co/BAAI/bge-large-zh)。

下载模型需要先[安装 Git LFS](https://docs.github.com/zh/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)，然后在 composite_demo/Langchain_Chatchat 下运行

```shell
$ mkdir models
$ cd models
$ git lfs install
$ git clone https://huggingface.co/THUDM/chatglm3-6b
$ git clone https://huggingface.co/BAAI/bge-large-zh
```

### 3.修改配置文件
在 composite_demo/config.py 中填入可用的 BING_SUBSCRIPTION_KEY 和 OPENAI_API_KEY。

### 4.依据本地文档构建向量库
本地知识库需要依据文档构建本地向量库，这可能会花费几十分钟时间

```shell
# 在 composite_demo/Langchain_Chatchat 下运行
$ python init_database.py --recreate-vs
```

可用以下方法检验向量库是否完全构建：

```shell
# 在 composite_demo/Langchain_Chatchat 目录下运行
$ python startup.py -a
```

成功启动后在浏览器内打开 localhost:8501， 点击左边的“知识库管理”，若右边的表中所有文件的“向量库”部分均为 √，则向量库完全构建。否则，只需在右边的表中点击“向量库”部分为 × 的文件，点击下方的“添加至向量库”，等待添加完毕即可。

### 5.启动项目

按照以下命令依次启动各个子项目

```shell
# 启动 NeteaseCloudMusicApi, 在 NeteaseCloudMusicApi 目录下运行
$ node app.js

# 启动本地知识库, 在 composite_demo/Langchain_Chatchat 目录下运行
$ python startup.py -a

# 启动聊天界面, 在 composite_demo 目录下运行
$ streamlit run main.py
```

一定要等待 Langchain_Chatchat 完全启动后再启动聊天界面。

正常启动后，可在最后一个命令的输出中找到端口，并在浏览器内打开。一般情况下为 localhost:8502。