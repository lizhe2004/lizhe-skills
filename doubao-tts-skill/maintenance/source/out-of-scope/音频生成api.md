基于 HTTP 协议的非流式音频生成接口。支持通过参考音频、参考图片或自然语言描述生成定制化音频，涵盖音效、音色等多种创作维度，单次最长可生成 **120** 秒音频，适用于有声书、影视配音、游戏音效等场景。


 
&nbsp;

<span id="Kc3z0KET"></span>
## 音频创作

**基本介绍**

豆包音频生成模型 1.0 (Seed\-Audio 1.0) 是业内首个可通过单条 Prompt 直接生成影视级音频的模型，支持文本、音频等多模态输入，显著降低声音创作门槛，兼顾高表现力与全要素覆盖。

**核心优势**


* **0 样本多模态生成:**  基于文本、图片、参考音频等数据，通过自然语言指导音频生成，大幅降低音色打造与效果调优的门槛

* **影视级多轨混音**

   * 单条指令即可定义多角色台词、语气与情绪节奏，自动完成时序编排与转场衔接

   * 笑声、叹息、停顿、方言口音等副语言细节可直接写入 Prompt 精准还原

   * 背景音乐、环境音效与人声一体化生成，无需额外混音软件，输出即成品

* **长时音色一致性:**  通过音色复刻方式，在长音频中保持音色统一，解决有声书、播客、长剧集等长程生成场景下音色不稳定的问题


&nbsp;

**应用场景**


* **音视频创作 / 编辑:**  面向短视频、广告、电商配音，可短时间内打造海量音色，让用户低门槛、便捷地创建适配自己视频的声音，并对合成效果 (风格、情感、局部修改) 灵活可控，实现语音、背景音乐与音效的一站式生成。

* **有声书:**  面向有声小说、多播、有声剧生产，可替代真人声优录音，大幅降低人工录制成本，快速产出高质量有声内容。

* **游戏配音:**  替代部分真人录音，以更强的可控性适配多角色、多情绪的游戏场景，并支持语音、背景音乐与音效的一站式生成。

* **AI 播客生产:**  快速生成多角色对谈音频，降低制作门槛，让播客内容实现规模化、批量化产出


&nbsp;

**能力预览**


|**类型** |**标题** |**Prompt & 参考音频** |**demo** |
|---|---|---|---|
|**文生音频** |悬疑刑侦片 |```Plain Text```<br>```先是一声手机震动的声音，环境中持续的鸟鸣声。音乐以马林巴为主奏乐器，加入合成器lead、电贝斯、打击乐，整体情绪紧张悬疑。男子1（中青年男性，台湾口音，嗓音低沉，浑厚）用严肃语气说道：“钟sir，你是什么时候被收买的？” 男子2（中年男性，台湾口音，嗓音沙哑，成熟）平静无奈的语气说：“既然你都知道了，我也没有什么好隐瞒的。阿标手上有些证据，搭配上李勋的人证，足够让青龙帮垮台。”男子1继续追问，语气中带着怀疑困惑：“你现在说这些，是要我继续相信你？”男子2以一种告诫的口吻说：“信不信都无所谓。我打来只是想提醒你，阿标已经失去耐心，最好待在男公馆别乱跑。在那里，青龙帮的人，不敢轻举妄动。”男子1简短地问道：“为什么？”男子2解释道：“据说跟青龙帮的帮规有关，细节我也不清楚。只知道男公馆对他们来说，是个不能动手的地方。”男子1的语气变得更加尖锐和不解，他说：“我就当你被阿标收买了，那你打这通电话的意图是什么？不是应该希望李峋落入他们手里吗？”男子2的声音听起来充满了无力感和宿命感，他缓缓说道：“有些事，不是我能选择的。宇川，这是我唯一能做的。保护好李峋，也保重自己。”然后出现一阵轻微的汽车行驶声，接着是一声轻微的汽车刹车声，随后是两声高跟鞋走路脚步声。```<br> |&nbsp;<br><br><audio src="https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_8a1e5377841d270ad2ca7d4b7cf5407b.wav" title="audio_Film__087_sft_1780966364038 (2).wav" controls></audio><br><br><br> |
||灵山宣战 |```Plain Text```<br>```音乐以合成器pad铺底，同时有合成打击乐、弦乐组、管乐组合奏，整体情绪紧张悬疑，先是一声沉闷的类似钟声“咚”的特效音，并伴随着一阵长时间的低频氛围音效，然后是一声尖锐的风声呼啸而过的特效音，紧接着是一声沉重的石门机关开启声，随后又是一声快速闪过的风声特效音，再出现连续两声的类似于“咻”的法术闪过特效音，之后是一声较长的类似于“唰”的转场特效音，再出现一声类似于“咻”的法术闪过特效音，最后是一声类似于“呼”的风声转场特效音。六耳猕猴（青年男性，嗓音偏尖细，沙哑，张扬，奇幻电影）声音有混响感，用一种非常得意和满足的语气说道：“爽！这斗战胜佛的位置，坐着就是舒服，嘿嘿嘿。”对话中夹杂着一声类似于“唰”的法术闪过特效音，然后是一声轻微的走路脚步声，接着是一声跳跃落地的声音，紧跟着是两声布鞋在地面摩擦的脚步声，如来佛祖（中年男性，嗓音浑厚，沉稳，有力，威严，庄重）声音整体带有明显回响，语速平缓，语气庄重地说道：“斗战胜佛入我沙门一年，斩妖除魔，功德无量，今日，特赐汝九转金莲一株，以示嘉奖。”对话中夹杂着一声类似于“唰”的法术闪过特效音，然后是一阵多人布鞋走路脚步声，六耳猕猴先是发出一阵用力的呼喝声，接着语气变得恭敬而正式，回应道：“弟子，谢佛祖恩典。”对话后先是一声沉闷的雷声，然后是一阵多人慌乱的跑步脚步声，接着是一声类似于“哗”的法术爆炸特效音，再出现一声金属嗡鸣声，众人发出惊慌失措的呼喊声。男子1（中年男性，嗓音低沉，气质成熟）用惊慌的语气问道：“发生什么事了？”对话中夹杂着一声多人摔倒在地的声音，然后是一声沉闷的爆炸声，接着是一阵持续的电流声，六耳猕猴疑惑的“嗯？”了一声。然后出现一声类似于“呼”的风声转场特效音，男子2（中年男性，嗓音低沉，气质沉稳）用困惑且警惕的语气问道：“怎么回事儿？”对话中夹杂着一声沉闷的爆炸声，然后是一阵多人痛苦的尖叫声，接着是一声重物落地的撞击声，再出现一声爆炸声，男子3（中老年男性，声音低沉，沙哑，威严感）用惊慌但霸气的语气问道：“敌袭！何方妖孽敢擅闯灵山！”对话中夹杂着一声多人摔倒在地的声音，然后是一声沉闷的爆炸声，接着是一阵持续的电流声，观音菩萨（中青年女性，嗓音柔和，温柔，知性）轻声的“啊”了一声。然后出现一声类似于“呼”的风声转场特效音，紧接着是一声巨大的石门被撞开的破碎声，男子4（中年男性，嗓音沙哑，成熟）用震惊地语气说道：“这是？”其中夹杂着多人的惊呼声。如来佛祖用震惊的语气说：“这股气息…”音乐以弦乐组合奏为主，加入中国大鼓，整体情绪紧张激烈对话中夹杂着一声沉闷的爆炸声，然后是一阵多人痛苦的尖叫声和惊呼声，接着是一声重物落地的撞击声，再出现一声爆炸声，须菩提（老年男性，嗓音低沉，沙哑，苍老，气质沉稳）声音带有回响，充满了压抑已久的愤怒，说道：“当初，汝等言他是妖猴，吾忍了，后来，汝等压他五百年，吾忍了，如今，汝等是非不分真假不明，害我徒儿枉死，让这只六耳冒名顶替，这口气，吾若是再忍，枉为师表，吾徒悟空何在？今日，为师来为他，”接着音量提高，一字一句地说道：“找回公道！”对话中夹杂着一声沉闷的爆炸声，然后是一阵多人痛苦的尖叫声，接着是一声重物落地的撞击声，再出现一声爆炸声，然后出现一声类似于“呼”的风声转场特效音，紧接着是一阵急促的跑步声，最后出现一声类似于“呼”的风声转场特效音。六耳猕猴显示一阵害怕地惊呼，然后用惊讶和不解的语气问道：“佛祖，这，这是谁？”如来佛祖的声音充满了力量和威严，一字一顿地说道：“斜月三星洞，”接着音量提高，大喊道：“须菩提！”```<br> |&nbsp;<br><br><audio src="https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_a17d2501ab957e0dc959b8b2d963abb5.wav" title="灵山宣战.wav" controls></audio><br><br><br> |
||电商直播带货 |```Plain Text```<br>```背景音乐极其微弱，以东北风格为主，女声演唱，整体音乐氛围热闹积极。带货主播1（青年女声，声音明亮，带有东北口音，热情）状态积极、仔细且设身处地的为直播间观众介绍道："金黄色的，这一定是很好的这个品质榴莲，那我进来瞅一眼吧。"期间穿插着带货主播2（青年女声，声线温柔甜美）认同的"对"的声音。带货主播1继续热情高亢的介绍道："A加级别的树熟的当地国的这一个，金枕头榴莲肉儿。"这是带货主播2也补充说道："金枕"带货主播1接着说道："而且是带核榴莲肉朋友们，不是属于把那个里面的那个核给您抠出去的。其实人为干预越少，您可能吃着更安心一点儿点儿，并且呢它放得住，保质期是18个月呢。"还有碰触塑料包装袋发出的声音。同时带货主播1继续推销道："啊，所以就是看您家里冰箱冷冻层的地方了。要是真有地方，我建议大家能买两包儿，不买一包儿。"带货主播1接着说："因为买两包儿我们还有一个10块钱的小优惠，还有一个10块钱的小优惠。你看噼里啪啦已经在把1打在公屏上。"说到这时语气搞怪地说道："熟练地让人心疼。"期间不停地穿插着带货主播2的赞同附和声："对""嗯"。带货主播2（青年女声，声线温柔甜美）笑着赞同道："哎呦，是"带货主播1继续强调道："熟练地让人心疼。"```<br> |&nbsp;<br><br><audio src="https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_2d7dfcf84faef3169fba67a57a340354.wav" title="电商直播带货.wav" controls></audio><br><br><br> |
|**参考音频生成** |爷爷宠溺独白 |参考音频<br><br><audio src="https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_b347f80c4e1ea466d946a102e4f4160a.wav" title="参考音频_爷爷宠溺独白.wav" controls></audio><br><br><br>Prompt<br><br>```Plain Text```<br>```爷爷（70岁以上，沙哑沧桑的音色，温和慈祥，气息不稳，饰演者为@音频1 ）整体节奏缓慢有适当的停顿，声音偶发颤抖，语气充满了慈爱和宠溺，带着笑意说道："好嘞，那爷爷就来偏爱小丸子吧！就算世界上所有人全都不偏爱小丸子，可爷爷我仍然会最最最最偏爱丸子你呀！5月真好啊！马上就是丸子的生日啦！嗯，那今天爷爷什么都买给你！"```<br> |&nbsp;<br><br><audio src="https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_0355a8467b98691eaebe62f3fcebd28c.wav" title="爷爷宠溺独白.wav" controls></audio><br> |
||技术讲解 |参考音频<br><br><audio src="https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_5a03502aa67c3fc560294bd79c18bdc5.wav" title="参考音频_技术讲解.wav" controls></audio><br><br><br>Prompt<br><br>```Plain Text```<br>```中年男性（35-40岁，嗓音低沉，略微沙哑，轻微气泡音，有口音，说话期间会不时的吸、咽口水，饰演者为@音频1 ）```<br>```语速稍微偏快，语气沉稳而肯定的说道："Java它…Java这块就不…不需要…因为Java本身有一个释放机制、垃圾回收机制，它都不需要你自己处理了，它自动回收机制。但是C++这块代码这是个难点，像你说这些内存的…把那对象进行存储，还有释放。呃……这块需要你在代码里面要体现出来，所以说这个是个难点啊。呃…是个难点，容易犯错的地方。很多人…做C++这么多年，很多人…做过C++多少年的甚至10年的人，他这块…一个指针、一个是内存这块，他都代码经常犯错。这种…就是我了解的，就是一些那个…我们这些同行里头，他们经常都犯错。所以说，所以我认为C++这块吧…它的器械电子、精工行业、工业方面制造比…应用比较广一些。呃…是…我…觉得它技术含量…还是比…尽管它更新没有比较慢些，它技术含量比Java…还是大多了，对。"语言组织得不好，说起话来有些吞吞吐吐，偶尔还有一些无法分辨的说话内容。 ```<br> |&nbsp;<br><br><audio src="https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_55af3217ab2d2a5f71f2666d7b37a1ce.wav" title="技术讲解.wav" controls></audio><br> |
| 时间控制| 示例| 广告播音员 是二十五岁左右年轻女子，声音优雅甜美，普通话，吐字清晰<br>音频以而长线条合成器开始，电子鼓组进入，合成器铃类乐器点缀，整体舒缓优雅的音乐氛围。<br>广告播音员语速慢、平缓、柔和且富有吸引力地说道：[2.7s:5.7s]“美丽的旅程，值得一个璀璨的开始。”<br>广告播音员继续以专业、舒缓、有说服力的语调介绍产品，且音量有增大，语速稍有加快道：[6.6s:18.9s]“Pocara面霜，专为年轻肌肤定制的第一瓶高端养护。<br>深海精粹与智能水润科技交融，瞬间渗透，24小时超强锁水，让肌肤如晨露般透亮饱满。”<br>句首伴随着一声水声流过的特效音，然后出现两声短暂、轻微的撞击水声音效，紧接着出现一阵类似于[19.7s:20.6s]“咕噜咕噜”的气泡声。<br>广告播音员用清晰柔美但坚定的声音念出品牌名称和广告语：[22.1s:24.3s]“Pocara，开启你的高光时刻。”<br>结尾响起一段空灵的风铃质感的合成器音效。|

 






<span data-label="purple">POST</span> `https://openspeech.bytedance.com/api/v3/tts/create`


请求头


**X\-Api\-Key** `string` <span data-api-tag="require|aUddUK">必选</span>

API Key 可从 [控制台>API Key管理](https://console.volcengine.com/speech/new/setting/apikeys?projectName=default.) 获取

[新版控制台](https://console.volcengine.com/speech/new?_vtm_=a106466.b106468.0_0.0_0.0.844_7636990835414320667)使用 `X-Api-Key` 单头鉴权，[旧版控制台](https://console.volcengine.com/speech/app)使用 `X-Api-App-Id` + `X-Api-Access-Key` 双头鉴权，参考示例详见：[旧版控制台鉴权参考示例](https://docs.volcengine.com/docs/6561/2534847?lang=zh)

<div data-tips="true" data-tips-type="warning" data-tips-is-title="true">注意</div>


<div data-tips="true" data-tips-type="warning">旧版控制台后续会下线，建议尽快切换到<a href="https://console.volcengine.com/speech/new?_vtm_=a106466.b106468.0_0.0_0.0.844_7636990835414320667">新版控制台</a>获取 API Key</div>




**X\-Api\-Request\-Id** `string`

客户端请求追踪ID，用于跨系统关联。建议传入内部业务系统的 `TraceID`，或使用`UUID`生成




请求体


**model** `string` <span data-api-tag="require|WLnuqK">必选</span>

模型版本标识，当前支持模型如下：


* **`seed-audio-1.0`**

   * 支持语种： `中文` `英文` `日语` `韩语` `墨西哥-西班牙语` `西班牙语` `德语` `法语` `巴西-葡萄牙语` `泰语` `越南语` `马来语` `菲律宾语` `意大利语` `俄语` `荷兰语` `波兰语` `土耳其语`

   * 支持时间轴控制，可通过`text_prompt`自然语言描述控制音频总时长及人声说话的具体时间段



**text_prompt** `string` <span data-api-tag="require|BfIXiZ">必选</span>

用于合成音频的提示词或者待合成的文本内容，最大支持3000字符。当前支持以下生成模式：


* **纯文本生成**：直接传入提示词，系统按 `text_prompt` 中的描述生成音频

* **参考音频生成**：通过 `@音频N` 引用 `references` 中对应位置的参考音频，编号从 1 开始，按上传顺序依次为`@音频1`、 `@音频2`......

* **参考图片生成**：使用图片参考时，本字段可只传入待合成的文本内容


<div data-tips="true" data-tips-type="tip" data-tips-is-title="true">说明</div>


<div data-tips="true" data-tips-type="tip">当前支持的语种请参考<code>model</code>的参数描述</div>




**references** `object list`

参考资源列表，根据传入内容自动匹配生成模式：


* **纯文本生成**：不传参考资源，按 `text_prompt` 中的提示词生成音频

* **参考音频生成**：传入音频参考，按参考音频和 `text_prompt` 中的提示词生成音频，同时支持通过音色ID指定音色

* **参考图片生成**：传入图片参考，按 `text_prompt` 中的文本内容生成音频


支持**纯文本**、**文本 + 图片**、**文本 + 音频**的组合生成音频

<div data-tips="true" data-tips-type="tip" data-tips-is-title="true">说明</div>



* <div data-tips="true" data-tips-type="tip">参考音频的上传顺序须与<code>text_prompt</code>中<code>@音频N</code>的编号顺序严格对应，即上传的第一条音频对应<code>@音频1</code>，以此类推</div>


* <div data-tips="true" data-tips-type="tip">最多支持上传3条参考音频，单条时长 ≦ 30秒，单条大小 ≦ 10 MB。支持格式：<code>wav</code>/<code>mp3</code>/<code>pcm</code>/<code>ogg_opus</code></div>


* <div data-tips="true" data-tips-type="tip">最多支持上传1张参考图片，图片大小 ≦ 10MB。支持格式<code>jpeg</code>/<code>png</code>/<code>webp</code></div>




**speaker** `string`

音色 ID，支持使用["豆包语音合成模型2.0"的音色](https://docs.volcengine.com/docs/6561/1257544?lang=zh)或声音复刻音色

<div data-tips="true" data-tips-type="warning" data-tips-is-title="true">注意</div>


<div data-tips="true" data-tips-type="warning"><code>speaker</code>、 <code>audio_data</code>、<code>audio_url</code> 参数互斥，仅需传入其中一个参数</div>




**audio_data** `string`

参考音频 Base64 编码

<div data-tips="true" data-tips-type="warning" data-tips-is-title="true">注意</div>


<div data-tips="true" data-tips-type="warning"><code>speaker</code>、 <code>audio_data</code>、<code>audio_url</code> 参数互斥，仅需传入其中一个参数</div>




**audio_url** `string`

参考音频 URL，支持引用远端音频

<div data-tips="true" data-tips-type="warning" data-tips-is-title="true">注意</div>


<div data-tips="true" data-tips-type="warning"><code>speaker</code>、 <code>audio_data</code>、<code>audio_url</code> 参数互斥，仅需传入其中一个参数</div>




**image_data** `string`

参考图片 Base64 编码

<div data-tips="true" data-tips-type="warning" data-tips-is-title="true">注意</div>



* <div data-tips="true" data-tips-type="warning">该参数与<code>image_url</code>互斥，仅需传入其中一个参数</div>


* <div data-tips="true" data-tips-type="warning">图片参考不能与音频参考混用，即<code>image_data</code> 参数不能与<code>audio_data</code> 、<code>audio_url</code> 或 <code>speaker</code>同时传入</div>




**image_url** `string`

参考图片URL

<div data-tips="true" data-tips-type="warning" data-tips-is-title="true">注意</div>



* <div data-tips="true" data-tips-type="warning">该参数与<code>image_data</code>互斥，仅需传入其中一个参数</div>


* <div data-tips="true" data-tips-type="warning">图片参考不能与音频参考混用，即<code>image_url</code> 参数不能与<code>audio_data</code> 、<code>audio_url</code> 或 <code>speaker</code>同时传入</div>





**audio_config** `object`

输出音频配置


**format** `string`

指定输出音频的格式，默认为`wav`

可选值：`wav`/`mp3`/`pcm`/`ogg_opus`



**sample_rate** `int`

指定输出音频的采样率，单位为Hz，不同音频格式支持的采样率不同，详细如下：


* `wav`/`pcm`默认值为`40000`，取值范围为[`8000`,`16000`,`24000`,`32000`,`40000`,`44100`,`48000`]

* `mp3`默认值为`44100`，取值范围为[`8000`,`16000`,`24000`,`32000`,`44100`,`48000`]

* `ogg_opus`仅支持`48000`



**speech_rate** `int`

指定语速，默认值为`0`，取值范围：[`-50`,`100`]，取值越大，语速越快

`-50`代表0.5倍速，`100`代表2.0倍速，默认不调整语速



**loudness_rate** `int`

指定音量，默认值为`0`，取值范围：[`-50`,`100`]，取值越大，音量越大

`-50`代表0.5倍音量，`100`代表2.0倍音量，默认不调整音量



**pitch_rate** `int`

指定音调，默认值为`0`，默认不调整音调，取值范围：[`-12`,`12`]，取值越大，音调越高



**enable_subtitle** `bool`

启用字幕服务，默认值为`false`，开启后，将返回字级别的时间戳

可选值：`true`, `false`




**watermark** `object`

水印配置，不传时默认不添加水印


**aigc_watermark** `bool`

显式水印开关，默认值为 `False`，开启后可在合成结尾增加音频节奏标识

可选值：`true`, `false`



**aigc_metadata** `object`

隐式水印，开启后可在合成音频 header 加入元数据，不开启时默认不添加水印


**enable** `bool`

启用隐式水印，默认值为 `False`

可选值：`true`, `false`



**content_producer** `string`

指定合成服务提供者的名称或编码



**produce_id** `string`

指定内容制作编号



**content_propagator** `string`

指定内容传播服务提供者的名称或编码



**propagate_id** `string`

指定内容传播编号






响应头


**X\-Tt\-Logid** `string`

服务端返回的 `Logid`，用于在咨询或者反馈时定位问题




响应体


**code** `int`

错误状态码，如需了解更多状态码的具体含义，可查阅[错误码查询文档](https://docs.volcengine.com/docs/6561/2534853?lang=zh#2u2ql30k)



**message** `string`

错误状态详情，如需了解更多状态详情的具体含义，可查阅[错误码查询文档](https://docs.volcengine.com/docs/6561/2534853?lang=zh#2u2ql30k)



**audio** `string`

合成后的音频数据，以 Base64 编码返回



**duration** `float`

处理后音频时长（秒），变速/后处理时可能与 `original_duration` 不同，计费以 `original_duration` 为准



**original_duration** `float`

模型输出的原始音频时长（秒），该值为计费依据，上限为120秒



**url** `string`

带过期时间的音频地址，有效期2小时



**subtitle** `object`

音频字幕信息，仅当`enable_subtitle`设置为`true` 时才会返回字幕信息


**text** `string`

音频对应的字幕文本



**sentences** `object list`

子句字幕信息


**start_time** `int`

该句起始时间，距音频开始的毫秒偏移值



**end_time** `int`

该句结束时间，距音频开始的毫秒偏移值



**text** `string`

该句的完整文本



**words** `object list`

词粒度


**start_time** `int`

该 token 起始时间，距音频开始的毫秒偏移值



**end_time** `int`

该 token 结束时间，距音频开始的毫秒偏移值



**text** `string` \*\*\*\*

该 token 的文本内容








