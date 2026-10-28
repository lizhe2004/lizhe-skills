> ## Documentation Index
> Fetch the complete documentation index at: https://docs.bailian.console.aliyun.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-Audio-TTS音色列表

> 查看 Qwen-Audio-TTS 各模型的系统音色，试听音色效果，并下载基础音色列表和试听音频。

<meta property="og:title" content="Qwen-Audio-TTS音色列表" />

<Note>
  - 所选音色（`voice`）必须属于当前模型（`model`）支持的音色列表，不能跨模型混用。音色不匹配时，服务会返回 `InvalidParameter` 错误，例如 `[cosyvoice:]Engine error [411]: TTS speak operation failed`。
  - 待合成文本（`text`）应使用所选音色支持的语言，否则可能出现发音错误或语音不自然。

  如需专属音色，请参见[声音复刻](/zh/model-studio/voice-cloning-user-guide)或[声音设计](/zh/model-studio/voice-design-user-guide)。
</Note>

## 系统音色 <span id="system-voices" />

对于支持方言指令的音色，可通过指令控制字段 `instruction` 指定方言，例如 `请讲上海话。`。

### qwen-audio-3.1-tts-plus <span id="qwen-tts31-plus-voices" />

<Tabs>
  <Tab title="旗舰音色">
    <table style={{ display: "table", tableLayout: "fixed", width: "100%", overflowWrap: "anywhere" }}>
      <colgroup>
        <col style={{ width: "30%" }} />

        <col style={{ width: "10%" }} />

        <col style={{ width: "25%" }} />

        <col style={{ width: "35%" }} />
      </colgroup>

      <thead>
        <tr>
          <th style={{ verticalAlign: "top" }}><strong>名称</strong></th>
          <th style={{ verticalAlign: "top" }}><strong>性别</strong></th>
          <th style={{ verticalAlign: "top" }}><strong>特性支持</strong></th>
          <th style={{ verticalAlign: "top" }}><strong>试听</strong></th>
        </tr>
      </thead>

      <tbody>
        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安灵心\_v3.1

            **voice 参数**: <code>longanlingxin\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            **试听 1**

            ```text
            你好呀，我是龙安灵心。在这个快节奏的世界里，我想做你耳畔最温柔的守候。无论是深夜的失眠还是清晨的微光，只要你需要，我都会在这里，用声音拥抱你的每一个情绪瞬间。
            ```

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
              <source src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9279.wav" type="audio/wav" />
            </audio>

            **试听 2**

            ```text
            今天过得怎么样？有没有遇到什么开心的小事，或者让你眉头紧锁的烦恼？别担心，慢慢说给我听。我会安静地陪伴着你，帮你梳理思绪，让心情像雨后的天空一样，重新变得清澈明亮。
            ```

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
              <source src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9278.wav" type="audio/wav" />
            </audio>

            **试听 3**

            ```text
            月亮已经爬上了树梢，星星在眨着眼睛。闭上眼睛，想象自己躺在柔软的云朵上，随着微风轻轻飘荡。所有的疲惫都随风散去，现在，请安心入睡，愿你在甜美的梦乡中，遇见最美的风景。
            ```

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
              <source src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f927f.wav" type="audio/wav" />
            </audio>
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 许南川

            **voice 参数**: <code>xunanchuan\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            **试听 1**

            ```text
            遇见你之前，我的世界是黑白单调的；遇见你之后，色彩斑斓如雨后彩虹。我想牵着你的手，走过春夏秋冬，看遍世间繁华。无论风雨如何变幻，只要你在身边，便是人间最美风景。
            ```

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
              <source src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f927e.wav" type="audio/wav" />
            </audio>

            **试听 2**

            ```text
            我是许南川，一个喜欢用声音讲述故事的人。我的声音或许不够华丽，但足够真诚。希望能通过这磁性的语调，带你走进不同的世界，感受文字背后的温度与力量，期待与你相遇。
            ```

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
              <source src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f927d.wav" type="audio/wav" />
            </audio>

            **试听 3**

            ```text
            在这个喧嚣的时代，保持清醒是一种奢侈。我喜欢在安静的午后，泡一杯茶，读一本好书。那种心灵的宁静，比任何物质的享受都来得珍贵。你呢？是否也渴望这样片刻的安宁？
            ```

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
              <source src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f927c.wav" type="audio/wav" />
            </audio>
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安欢\_v3.1

            **voice 参数**: <code>longanhuan\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            **试听 1**

            ```text
            嗨，大家好！我是龙安欢。我喜欢笑，喜欢热闹，更喜欢看到大家快乐的样子。有什么烦心事尽管找我，保证让你笑着走出阴霾。让我们一起快乐起来吧！
            ```

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
              <source src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9273.wav" type="audio/wav" />
            </audio>

            **试听 2**

            ```text
            买衣服不要只看款式，更要看面料和剪裁。这件大衣版型正，羊毛含量高，穿在身上既保暖又有型。性价比超高，闭眼入都不会错。信我的准没错，赶紧入手一件过冬吧！
            ```

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
              <source src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9272.wav" type="audio/wav" />
            </audio>

            **试听 3**

            ```text
            天哪，今天的天气简直太糟糕了！出门忘带伞，结果淋成落汤鸡。不过没关系，回家喝杯热姜茶，洗个热水澡，又是一条好汉！你们今天过得怎么样？有没有什么趣事跟我分享呀？
            ```

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
              <source src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9271.wav" type="audio/wav" />
            </audio>
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安风悦\_v3.1

            **voice 参数**: <code>longanfengyue\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            **试听 1**

            ```text
            明天白天多云转晴，气温适宜，最高二十度，最低十五度。风力不大，非常适合户外活动。不过早晚温差较大，建议大家适当增减衣物，预防感冒。出行前记得查看实时路况哦。
            ```

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
              <source src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9270.wav" type="audio/wav" />
            </audio>

            **试听 2**

            ```text
            最近我在看一部老电影，里面的配乐特别经典，听得我忍不住单曲循环。你平时喜欢听什么类型的音乐？是轻快的流行乐，还是安静的纯音乐？推荐几首给我呗，我想换换口味。
            ```

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
              <source src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9277.wav" type="audio/wav" />
            </audio>

            **试听 3**

            ```text
            外婆坐在藤椅上，手里织着那条没完工的围巾，针脚细密而整齐。夕阳透过窗棂洒在她银白的发丝上，泛着柔和的光晕。她抬起头，笑着对我说：‘天凉了，快戴上吧。’那一刻，时光仿佛静止。
            ```

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
              <source src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9276.wav" type="audio/wav" />
            </audio>
          </td>
        </tr>
      </tbody>
    </table>
  </Tab>
</Tabs>

### qwen-audio-3.1-tts-flash <span id="qwen-tts31-voices" />

<Note>
  多语种与方言音色、精品英文音色支持北京和新加坡地域，其他类型音色仅支持北京地域。
</Note>

<Tabs>
  <Tab title="多语种与方言音色">
    <span id="qwen-tts31-multilingual" />

    以下四个音色均支持下列全部方言和语言。

    - 方言：上海话、广东话、东北话、重庆话、陕西话、云南话、宁波话、甘肃话。
    - 语言：日语、韩语、法语、德语、葡萄牙语、意大利语、越南语、印尼语。

    <table style={{ display: "table", tableLayout: "fixed", width: "100%", overflowWrap: "anywhere" }}>
      <colgroup>
        <col style={{ width: "30%" }} />

        <col style={{ width: "10%" }} />

        <col style={{ width: "25%" }} />

        <col style={{ width: "35%" }} />
      </colgroup>

      <thead>
        <tr>
          <th style={{ verticalAlign: "top" }}>
            **音色信息**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **性别**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **特性支持**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **试听**
          </th>
        </tr>
      </thead>

      <tbody>
        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安欢\_v3.1

            **voice 参数**: <code>longanhuan\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            重庆话

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9ced.wav" />

            宁波话

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cec.wav" />

            韩语

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9ce3.wav" />

            印尼语

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9ce2.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安灵心\_v3.1

            **voice 参数**: <code>longanlingxin\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            云南话

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9ce1.wav" />

            陕西话

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9ce0.wav" />

            上海话

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9ce7.wav" />

            法语

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9ce6.wav" />

            意大利语

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9ce5.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安风悦\_v3.1

            **voice 参数**: <code>longanfengyue\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            东北话

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9ce4.wav" />

            越南语

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cfb.wav" />

            日语

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cfa.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 许南川

            **voice 参数**: <code>xunanchuan\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            甘肃话

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cf9.wav" />

            东北话

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cf8.wav" />

            法语

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cff.wav" />

            葡萄牙语

            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cfe.wav" />
          </td>
        </tr>
      </tbody>
    </table>
  </Tab>

  <Tab title="精品中文音色">
    <span id="qwen-tts31-chinese" />

    以下音色仅支持中文普通话。

    <table style={{ display: "table", tableLayout: "fixed", width: "100%", overflowWrap: "anywhere" }}>
      <colgroup>
        <col style={{ width: "23%" }} />

        <col style={{ width: "7%" }} />

        <col style={{ width: "12%" }} />

        <col style={{ width: "13%" }} />

        <col style={{ width: "20%" }} />

        <col style={{ width: "25%" }} />
      </colgroup>

      <thead>
        <tr>
          <th style={{ verticalAlign: "top" }}>
            **音色信息**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **性别**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **声线特质**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **适用场景**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **特性支持**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **试听**
          </th>
        </tr>
      </thead>

      <tbody>
        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 于小云

            **voice 参数**: <code>yuxiaoyun\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            元气、亲切、自然
          </td>

          <td style={{ verticalAlign: "top" }}>
            广告营销、广播、客服助手、旁白
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cfd.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 乔小娇

            **voice 参数**: <code>qiaoxiaojiao\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            俏丽、可爱
          </td>

          <td style={{ verticalAlign: "top" }}>
            广告营销、客服助手、有声书
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cfc.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 夏小晨

            **voice 参数**: <code>xiaxiaochen\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            元气、明亮
          </td>

          <td style={{ verticalAlign: "top" }}>
            广告营销、有声书
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cf2.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 安明远

            **voice 参数**: <code>anmingyuan\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            清亮、自然
          </td>

          <td style={{ verticalAlign: "top" }}>
            广告营销、有声书、旁白
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cf1.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 温怀清

            **voice 参数**: <code>wenhuaiqing\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            清亮、柔和
          </td>

          <td style={{ verticalAlign: "top" }}>
            儿童故事、客服助手、广告营销、新闻播报
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cf0.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 安小岚

            **voice 参数**: <code>anxiaolan\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            清甜、纯净
          </td>

          <td style={{ verticalAlign: "top" }}>
            有声书、客服助手、旁白、新闻播报、广告营销
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cf7.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 谢舒柔

            **voice 参数**: <code>xieshurou\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            柔和、自然、知性
          </td>

          <td style={{ verticalAlign: "top" }}>
            有声书、客服助手、旁白
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9cf5.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 白清岚

            **voice 参数**: <code>baiqinglan\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            明亮、清纯
          </td>

          <td style={{ verticalAlign: "top" }}>
            语音助手、客服助手
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c0b.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 许玉远

            **voice 参数**: <code>xuyuyuan\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            知性、成熟、质感
          </td>

          <td style={{ verticalAlign: "top" }}>
            广告营销、新闻播报、旁白、客服助手、有声书
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c0a.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 安若柔

            **voice 参数**: <code>anruorou\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            气声、知性
          </td>

          <td style={{ verticalAlign: "top" }}>
            旁白、语音助手
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c09.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 闻怀之

            **voice 参数**: <code>wenhuaizhi\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            稳重、成熟
          </td>

          <td style={{ verticalAlign: "top" }}>
            有声书、新闻播报、广告营销、客服助手、旁白
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c08.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 萧行之

            **voice 参数**: <code>xiaoxingzhi\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            端庄、贵气
          </td>

          <td style={{ verticalAlign: "top" }}>
            新闻播报、有声书、旁白、客服助手
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c0f.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 顾云舒

            **voice 参数**: <code>guyunshu\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            成熟、稳重
          </td>

          <td style={{ verticalAlign: "top" }}>
            音乐电台、客服助手、有声书、旁白
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c0e.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 霍拙石

            **voice 参数**: <code>huozhuoshi\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            清亮
          </td>

          <td style={{ verticalAlign: "top" }}>
            有声书、广告营销、旁白
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c0d.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 叶清禾

            **voice 参数**: <code>yeqinghe\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            亲切、温柔
          </td>

          <td style={{ verticalAlign: "top" }}>
            有声书、广告营销、旁白、客服助手
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c0c.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 云欢欢

            **voice 参数**: <code>yunhuanhuan\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            高亢、热情
          </td>

          <td style={{ verticalAlign: "top" }}>
            有声书、旁白、客服助手
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c03.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 徐小俏

            **voice 参数**: <code>xuxiaoqiao\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            自然、俏皮
          </td>

          <td style={{ verticalAlign: "top" }}>
            有声书、旁白、客服助手
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c02.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 白安然

            **voice 参数**: <code>baianran\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            低沉、浑厚、气声
          </td>

          <td style={{ verticalAlign: "top" }}>
            配音讲解、有声书、旁白
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c01.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 许言初

            **voice 参数**: <code>xuyanchu\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            沉稳、磁性
          </td>

          <td style={{ verticalAlign: "top" }}>
            新闻播报、有声书
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c00.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 叶知晴

            **voice 参数**: <code>yezhiqing\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            轻快、自然
          </td>

          <td style={{ verticalAlign: "top" }}>
            儿童故事、客服助手、语音助手
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c05.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 安迪

            **voice 参数**: <code>andi\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            ABC口音
          </td>

          <td style={{ verticalAlign: "top" }}>
            语音助手
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c1b.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 安语晴

            **voice 参数**: <code>anyuqing\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            甜妹
          </td>

          <td style={{ verticalAlign: "top" }}>
            语音助手、旁白、新闻播报
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c1a.wav" />
          </td>
        </tr>
      </tbody>
    </table>
  </Tab>

  <Tab title="精品英文音色">
    <span id="qwen-tts31-english" />

    以下音色仅支持英文。

    <table style={{ display: "table", tableLayout: "fixed", width: "100%", overflowWrap: "anywhere" }}>
      <colgroup>
        <col style={{ width: "27%" }} />

        <col style={{ width: "8%" }} />

        <col style={{ width: "12%" }} />

        <col style={{ width: "23%" }} />

        <col style={{ width: "30%" }} />
      </colgroup>

      <thead>
        <tr>
          <th style={{ verticalAlign: "top" }}>
            **音色信息**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **性别**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **口音**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **特性支持**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **试听**
          </th>
        </tr>
      </thead>

      <tbody>
        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Emily

            **voice 参数**: <code>Emily\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            英式女声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c19.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Luna

            **voice 参数**: <code>Luna\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            英式女声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c18.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Eric

            **voice 参数**: <code>Eric\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            英式男声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c1f.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Luca

            **voice 参数**: <code>Luca\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            英式男声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c1e.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Abby

            **voice 参数**: <code>Abby\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            美式女声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c1d.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Annie

            **voice 参数**: <code>Annie\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            美式女声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c1c.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Ava

            **voice 参数**: <code>Ava\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            美式女声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c13.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Beth

            **voice 参数**: <code>Beth\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            美式女声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c12.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Betty

            **voice 参数**: <code>Betty\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            美式女声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c11.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Cally

            **voice 参数**: <code>Cally\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            美式女声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c10.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Cindy

            **voice 参数**: <code>Cindy\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            美式女声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c17.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Donna

            **voice 参数**: <code>Donna\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            美式女声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c16.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Andy

            **voice 参数**: <code>Andy\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            美式男声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c15.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: Brian

            **voice 参数**: <code>Brian\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            美式男声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c14.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: David

            **voice 参数**: <code>David\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            美式男声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c2b.wav" />
          </td>
        </tr>
      </tbody>
    </table>
  </Tab>

  <Tab title="其他系统音色">
    <span id="qwen-tts31-additional" />

    <table style={{ display: "table", tableLayout: "fixed", width: "100%", overflowWrap: "anywhere" }}>
      <colgroup>
        <col style={{ width: "23%" }} />

        <col style={{ width: "7%" }} />

        <col style={{ width: "12%" }} />

        <col style={{ width: "13%" }} />

        <col style={{ width: "20%" }} />

        <col style={{ width: "25%" }} />
      </colgroup>

      <thead>
        <tr>
          <th style={{ verticalAlign: "top" }}>
            **音色信息**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **性别**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **声线特质**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **适用场景**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **特性支持**
          </th>

          <th style={{ verticalAlign: "top" }}>
            **试听**
          </th>
        </tr>
      </thead>

      <tbody>
        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安元妃\_v3.1

            **voice 参数**: <code>longanyuanfei\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            高傲妃子音
          </td>

          <td style={{ verticalAlign: "top" }}>
            社交陪伴
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c2a.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙杰力豆\_v3.1

            **voice 参数**: <code>longjielidou\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            天真男童音
          </td>

          <td style={{ verticalAlign: "top" }}>
            儿童陪伴
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c29.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安灵希\_v3.1

            **voice 参数**: <code>longanlingxi\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            可爱甜美音
          </td>

          <td style={{ verticalAlign: "top" }}>
            社交陪伴（精品中文）
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c2f.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙火火\_v3.1

            **voice 参数**: <code>longhuohuo\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            顽皮少年音
          </td>

          <td style={{ verticalAlign: "top" }}>
            角色音
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c28.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙应桃\_v3.1

            **voice 参数**: <code>longyingtao\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            温柔淡定女
          </td>

          <td style={{ verticalAlign: "top" }}>
            客服
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c2e.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安雅\_v3.1

            **voice 参数**: <code>longanya\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            高雅气质女
          </td>

          <td style={{ verticalAlign: "top" }}>
            社交陪伴
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c2d.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙婉\_v3.1

            **voice 参数**: <code>longwan\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            细腻柔声女
          </td>

          <td style={{ verticalAlign: "top" }}>
            社交陪伴
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c2c.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙星\_v3.1

            **voice 参数**: <code>longxing\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            温婉邻家女
          </td>

          <td style={{ verticalAlign: "top" }}>
            社交陪伴
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c23.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙华\_v3.1

            **voice 参数**: <code>longhua\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            元气甜美女
          </td>

          <td style={{ verticalAlign: "top" }}>
            社交陪伴
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c22.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙寒\_v3.1

            **voice 参数**: <code>longhan\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            温暖痴情男
          </td>

          <td style={{ verticalAlign: "top" }}>
            社交陪伴
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c21.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安智\_v3.1

            **voice 参数**: <code>longanzhi\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            睿智轻熟男
          </td>

          <td style={{ verticalAlign: "top" }}>
            社交陪伴
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c20.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙哲\_v3.1

            **voice 参数**: <code>longzhe\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            呆板大暖男
          </td>

          <td style={{ verticalAlign: "top" }}>
            社交陪伴
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c27.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安洋\_v3.1

            **voice 参数**: <code>longanyang\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            阳光大男孩
          </td>

          <td style={{ verticalAlign: "top" }}>
            社交陪伴（标杆音色）
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c26.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 李白\_v3.1

            **voice 参数**: <code>libai\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            古代诗仙男
          </td>

          <td style={{ verticalAlign: "top" }}>
            诗词朗诵
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c25.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙铃\_v3.1

            **voice 参数**: <code>longling\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            稚气呆板女
          </td>

          <td style={{ verticalAlign: "top" }}>
            童声
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c24.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙牛牛\_v3.1

            **voice 参数**: <code>longniuniu\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            阳光男童声
          </td>

          <td style={{ verticalAlign: "top" }}>
            消费电子-儿童有声书
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c3b.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙闪闪\_v3.1

            **voice 参数**: <code>longshanshan\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            戏剧化童声
          </td>

          <td style={{ verticalAlign: "top" }}>
            消费电子-儿童有声书
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c3a.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙泡泡\_v3.1

            **voice 参数**: <code>longpaopao\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            飞天泡泡音
          </td>

          <td style={{ verticalAlign: "top" }}>
            消费电子-儿童陪伴
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c39.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: loongstella\_v3.1

            **voice 参数**: <code>loongstella\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            飒爽利落女
          </td>

          <td style={{ verticalAlign: "top" }}>
            新闻播报
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c38.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙媛\_v3.1

            **voice 参数**: <code>longyuan\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            温暖治愈女
          </td>

          <td style={{ verticalAlign: "top" }}>
            有声书
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c3f.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙妙\_v3.1

            **voice 参数**: <code>longmiao\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            抑扬顿挫女
          </td>

          <td style={{ verticalAlign: "top" }}>
            有声书
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c3e.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙三叔\_v3.1

            **voice 参数**: <code>longsanshu\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            沉稳质感男
          </td>

          <td style={{ verticalAlign: "top" }}>
            有声书
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c3d.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安莉\_v3.1

            **voice 参数**: <code>longanli\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            利落从容女
          </td>

          <td style={{ verticalAlign: "top" }}>
            语音助手
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c3c.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安温\_v3.1

            **voice 参数**: <code>longanwen\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            优雅知性女
          </td>

          <td style={{ verticalAlign: "top" }}>
            语音助手
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c33.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安朗\_v3.1

            **voice 参数**: <code>longanlang\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            清爽利落男
          </td>

          <td style={{ verticalAlign: "top" }}>
            语音助手
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c32.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙小夏\_v3.1

            **voice 参数**: <code>longxiaoxia\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            女
          </td>

          <td style={{ verticalAlign: "top" }}>
            沉稳权威女
          </td>

          <td style={{ verticalAlign: "top" }}>
            语音助手
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c31.wav" />
          </td>
        </tr>

        <tr>
          <td style={{ verticalAlign: "top" }}>
            **名称**: 龙安冲\_v3.1

            **voice 参数**: <code>longanchong\_v3.1</code>
          </td>

          <td style={{ verticalAlign: "top" }}>
            男
          </td>

          <td style={{ verticalAlign: "top" }}>
            激情推销男
          </td>

          <td style={{ verticalAlign: "top" }}>
            直播带货
          </td>

          <td style={{ verticalAlign: "top" }}>
            SSML: 支持

            指令控制: 支持

            时间戳: 支持
          </td>

          <td style={{ verticalAlign: "top" }}>
            <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }} src="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/audios/6a4b3c2d1e0f9c30.wav" />
          </td>
        </tr>
      </tbody>
    </table>
  </Tab>
</Tabs>

### qwen-audio-3.0-tts-plus <span id="f399ce27bcc8" />

<table style={{ display: "table", tableLayout: "fixed", width: "100%", overflowWrap: "anywhere" }}>
  <colgroup>
    <col style={{ width: "15%" }} />

    <col style={{ width: "30%" }} />

    <col style={{ width: "20%" }} />

    <col style={{ width: "35%" }} />
  </colgroup>

  <thead>
    <tr>
      <th style={{ verticalAlign: "top" }}>
        **适用场景**
      </th>

      <th style={{ verticalAlign: "top" }}>
        **音色信息**
      </th>

      <th style={{ verticalAlign: "top" }}>
        **特性支持**
      </th>

      <th style={{ verticalAlign: "top" }}>
        **音频试听（右键保存音频）**
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td rowSpan={2} style={{ verticalAlign: "top" }}>
        社交陪伴（旗舰音色）
      </td>

      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：龙安灵心

        <strong>voice参数</strong>：longanlingxin

        <strong>特质</strong>：知心温暖音

        <strong>年龄</strong>：25岁

        <strong>性别</strong>：女

        <strong>语言</strong>：中文（普通话）、英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 支持

        指令控制: 支持

        时间戳: 支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/deqsie/01_longanlingxin.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>

    <tr>
      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：龙安鲁风

        <strong>voice参数</strong>：longanlufeng

        <strong>特质</strong>：明亮开朗音

        <strong>年龄</strong>：25岁

        <strong>性别</strong>：男

        <strong>语言</strong>：中文（普通话）、英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 支持

        指令控制: 支持

        时间戳: 支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/tpgsdv/02_longanlufeng.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>
  </tbody>
</table>

### qwen-audio-3.0-tts-flash <span id="f399ce27bcc8flash" />

<table style={{ display: "table", tableLayout: "fixed", width: "100%", overflowWrap: "anywhere" }}>
  <colgroup>
    <col style={{ width: "15%" }} />

    <col style={{ width: "30%" }} />

    <col style={{ width: "20%" }} />

    <col style={{ width: "35%" }} />
  </colgroup>

  <thead>
    <tr>
      <th style={{ verticalAlign: "top" }}>
        **适用场景**
      </th>

      <th style={{ verticalAlign: "top" }}>
        **音色信息**
      </th>

      <th style={{ verticalAlign: "top" }}>
        **特性支持**
      </th>

      <th style={{ verticalAlign: "top" }}>
        **音频试听（右键保存音频）**
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td rowSpan={5} style={{ verticalAlign: "top" }}>
        社交陪伴（精品中文）
      </td>

      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：龙安风悦

        <strong>voice参数</strong>：longanfengyue

        <strong>特质</strong>：自然亲切音

        <strong>年龄</strong>：30岁

        <strong>性别</strong>：女

        <strong>语言</strong>：中文（普通话）、英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 支持

        指令控制: 支持

        时间戳: 支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/djxajf/03_longanfengyue.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>

    <tr>
      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：龙安元妃

        <strong>voice参数</strong>：longanyuanfei

        <strong>特质</strong>：高傲妃子音

        <strong>年龄</strong>：30岁

        <strong>性别</strong>：女

        <strong>语言</strong>：中文（普通话）、英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 支持

        指令控制: 支持

        时间戳: 支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/lnyaxv/04_longanyuanfei.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>

    <tr>
      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：龙安灵希

        <strong>voice参数</strong>：longanlingxi

        <strong>特质</strong>：可爱甜美音

        <strong>年龄</strong>：25岁

        <strong>性别</strong>：女

        <strong>语言</strong>：中文（普通话）、英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 支持

        指令控制: 支持

        时间戳: 支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/pfkypj/05_longanlingxi.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>

    <tr>
      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：龙安小昕

        <strong>voice参数</strong>：longanxiaoxin

        <strong>特质</strong>：亲切活泼音

        <strong>年龄</strong>：22岁

        <strong>性别</strong>：女

        <strong>语言</strong>：中文（普通话）、英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 支持

        指令控制: 支持

        时间戳: 支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/msjxqk/07_longanxiaoxin.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>

    <tr>
      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：龙安欢

        <strong>voice参数</strong>：longanhuan\_v3.6

        <strong>年龄</strong>：25岁

        <strong>性别</strong>：女

        <strong>语言</strong>：中文（普通话）、英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 支持

        指令控制: 支持

        时间戳: 支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/glwaer/09_longanhuan.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>

    <tr>
      <td rowSpan={2} style={{ verticalAlign: "top" }}>
        儿童陪伴/智能玩具（精品儿童）
      </td>

      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：龙杰力豆

        <strong>voice参数</strong>：longjielidou\_v3.6

        <strong>特质</strong>：天真男童

        <strong>年龄</strong>：5岁

        <strong>性别</strong>：男

        <strong>语言</strong>：中文（普通话）、英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 支持

        指令控制: 支持

        时间戳: 支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/wirytn/08_longjielidou.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>

    <tr>
      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：龙泡泡

        <strong>voice参数</strong>：longpaopao\_v3.6

        <strong>特质</strong>：软糯可爱音

        <strong>年龄</strong>：5岁

        <strong>性别</strong>：女

        <strong>语言</strong>：中文（普通话）、英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 支持

        指令控制: 支持

        时间戳: 支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/nrgkjo/13_longpaopao.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>

    <tr>
      <td rowSpan={2} style={{ verticalAlign: "top" }}>
        角色音/游戏（精品中文）
      </td>

      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：龙火火

        <strong>voice参数</strong>：longhuohuo\_v3.6

        <strong>特质</strong>：顽皮少年音

        <strong>年龄</strong>：8岁

        <strong>性别</strong>：男

        <strong>语言</strong>：中文（普通话）、英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 支持

        指令控制: 支持

        时间戳: 支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/efdgqh/11_longhuohuo.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>

    <tr>
      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：龙川叔

        <strong>voice参数</strong>：longchuanshu\_v3.6

        <strong>特质</strong>：川普大叔音

        <strong>年龄</strong>：40岁

        <strong>性别</strong>：男

        <strong>语言</strong>：中文（普通话）、英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 支持

        指令控制: 支持

        时间戳: 支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/makxfd/12_longchuanshu.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>

    <tr>
      <td rowSpan={3} style={{ verticalAlign: "top" }}>
        社交陪伴/语音助手（精品英文）
      </td>

      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：loongmary

        <strong>voice参数</strong>：loongmary

        <strong>特质</strong>：温暖英音

        <strong>年龄</strong>：20岁

        <strong>性别</strong>：女

        <strong>语言</strong>：英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 不支持

        指令控制: 不支持

        时间戳: 不支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/wpitzn/01_loongmary.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>

    <tr>
      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：loongeva

        <strong>voice参数</strong>：loongeva\_v3.6

        <strong>特质</strong>：高智美音

        <strong>年龄</strong>：28岁

        <strong>性别</strong>：女

        <strong>语言</strong>：英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 不支持

        指令控制: 不支持

        时间戳: 不支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/xajwqw/02_loongeva.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>

    <tr>
      <td style={{ verticalAlign: "top" }}>
        <strong>名称</strong>：loongJohn

        <strong>voice参数</strong>：loongjohn

        <strong>特质</strong>：沉稳亲切美音

        <strong>年龄</strong>：28岁

        <strong>性别</strong>：男

        <strong>语言</strong>：英文
      </td>

      <td style={{ verticalAlign: "top" }}>
        SSML: 不支持

        指令控制: 不支持

        时间戳: 不支持
      </td>

      <td style={{ verticalAlign: "top" }}>
        <audio controls style={{ width: "100%", maxWidth: "100%", minWidth: 0 }}>
          <source src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/pwxpto/03_loongjohn_1.wav" type="audio/x-wav" />
        </audio>
      </td>
    </tr>
  </tbody>
</table>

## 基础音色 <span id="ext-voices-title" />

<Note>
  建议优先使用系统音色，以获得更稳定的语音合成效果。如需定制音色，可通过[声音复刻](/zh/model-studio/voice-cloning-user-guide)或[声音设计](/zh/model-studio/voice-design-user-guide)创建专属音色。基础音色提供更多选择，使用前建议试听并评估其是否符合业务需求。
</Note>

除上述系统音色外，`qwen-audio-3.0-tts-plus`和`qwen-audio-3.0-tts-flash`各自还提供500余个通过声音复刻生成的基础音色，调用方式与系统音色一致。

<span id="base-voice-usage" />

基础音色命名格式为`qwen-audio-3.0-tts-{plus|flash}-{音色后缀}`，两个模型同一后缀对应同一套试听音频。

<span id="base-voice-downloads" />

- `qwen-audio-3.0-tts-plus`基础音色列表（Excel）：[qwen-audio-3.0-tts-plus基础音色.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260723/ydwqqz/qwen-audio-3.0-tts-plus%E5%9F%BA%E7%A1%80%E9%9F%B3%E8%89%B2.xlsx)
- `qwen-audio-3.0-tts-flash`基础音色列表（Excel）：[qwen-audio-3.0-tts-flash基础音色.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260723/thosjr/qwen-audio-3.0-tts-flash%E5%9F%BA%E7%A1%80%E9%9F%B3%E8%89%B2.xlsx)
- 基础音色试听音频包（plus和flash共用）：[基础音色试听音频包.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260720/tuuuqo/%E5%9F%BA%E7%A1%80%E9%9F%B3%E8%89%B2%E8%AF%95%E5%90%AC%E9%9F%B3%E9%A2%91%E5%8C%85.zip)

**试听步骤**

<span id="base-voice-preview" />

1. 下载Excel和试听音频包，将音频包解压到本地。
2. 在Excel中找到“预览音频文件名”列，获取音频文件名。
3. 在解压目录中找到对应文件，使用播放器打开试听。
