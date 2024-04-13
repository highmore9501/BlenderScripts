## readyPlayerMe-->hubs

### 集成 readyPlayerMe 页面

这是 readyPlayerMe 集成指南的地址：
https://docs.readyplayer.me/ready-player-me/integration-guides/overview
用户在集成好的 readyPlayerMe 页面上捏好人以后，最终导出会得到一个 avatar 的 url，我们把它下载下来。就得到了下个步骤必须的材料。

### 导入动画数据

用`copyAnimationsToReadyPlayerModel.py`将一个已带有行走，跑步，站立等动画的模型里带的动画，复制到另一个由 readyPlayer 生成的模型上。

#### 需要：

- 电脑安装 blender
- 本 py 脚本文件
- 一个带有动画模型的 blender 文件
- 一个由 readyPlayer 生成的 glb 模型文件

#### 使用方法：

运行指令：
`blender -b <带动画模型的blender文件路径> -P <py脚本路径> -- <readyPlayer的glb模型文件路径>`

#### 运行结果：

会在原 readyPlayer 模型的同一目录下生成一个新的 glb 文件，该文件名与原文件名相同，只是在后面加上了 `_animated` 的后缀。

### 将模型转为用户资产

原 hubs 是让用户点击创建 avatar，然后上传模型，转化为用户资产的，具体的实现是在 `src/react-components/avatar-editor.js`里。

原来的逻辑有点小复杂：

- 用户通过 `selectListingGrid` 选择模型文件上传，先更新了 `this.inputFiles["glb"]`,`this.state.avatar.files.glb`
- 用户点击 `保存`按钮，会执行 `uploadAvatar`方法，它会执行以下步骤：

  1. 加载读取模型文件，并且把文件分割成 `gltf` 和 `bin` 两个部分，然后保存到 `this.inputFiles.gltf`和 `this.inputFIles.bin`里面。（为什么会分成两个部分，是因为根据 glb 文件的结构，它本身就分两个部分：`gltf` 部分保存的是模型的数据层级结构，`bin` 保存的是各种 raw 数据，比如各种材质贴图，动画数据。所以 `gltf` 部分数据量不大，`bin` 才是模型的主体）

  2. 调用`this.preview.snapshot `，生成一张模型的预览图片，保存到`this.inputFiles.thumbnail`里。

  3. 调用`src/utils/media-utils.js`里的`upload`方法，将 `this.inputFIles` 下的各种文件上传，实际上也就是上传 `gltf,bin,thumbnail` 这三个文件。每上传成功一个文件会得到一个 respone，里面有 `file_id,meta.access_token,meta.promotion_token` 三个字段。
  4. 给 `this.state.avatar.files` 下面的 `gltf,bin,thumbnail`，都添加 `file_id,meta.access_token,meta.promotion_token` 三个值。
  5. 调用 `createOrUpdateAvatar`，把 `this.state.avatar` 里的数据上传，上传结束后，模型正式成为用户可用资产。

上面的内容可以查看 `src/react-components/avatar-editor.js`里的中文注释。

现在的逻辑最好是可以直接模拟用户操作，完成选择模型并点击上传的动作。因为要把原流程剥离出来重写是非常麻烦的。
