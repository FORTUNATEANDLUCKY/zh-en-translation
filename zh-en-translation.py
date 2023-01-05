import requests
import js2py
import tkinter
import threading
import time

# 定义主要变量
url = "https://fanyi.baidu.com/v2transapi"
sentence = ''
# 定义默认翻译语言
lang_from = ''
lang_to = ''


def language():  # 判断输入值的语言
    global lang_from, lang_to
    for letter in sentence:
        if ord('A') <= ord(letter) <= ord('z'):
            lang_from = 'en'
            lang_to = 'zh'
            break
        lang_from = 'zh'
        lang_to = 'en'


def get_sign():  # 调用js函数生成sign值

    js = r'''function n(t, e) {
            for (var n = 0; n < e.length - 2; n += 3) {
                var r = e.charAt(n + 2);
                r = "a" <= r ? r.charCodeAt(0) - 87 : Number(r),
                r = "+" === e.charAt(n + 1) ? t >>> r : t << r,
                t = "+" === e.charAt(n) ? t + r & 4294967295 : t ^ r
            }
            return t
        }
function sign(t) {
            var r = "320305.131321201"
            var o, i = t.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
            if (null === i) {
                var a = t.length;
                a > 30 && (t = "".concat(t.substr(0, 10)).concat(t.substr
                (Math.floor(a / 2) - 5, 10)).concat(t.substr(-10, 10)))
            } else {
                for (var s = t.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), c = 0, u = s.length, l = []; c < u; c++)
                    "" !== s[c] && l.push.apply(l, function(t) {
                        if (Array.isArray(t))
                            return e(t)
                    }(o = s[c].split("")) || function(t) {
                        if ("undefined" != typeof Symbol && null != t[Symbol.iterator] || null != t["@@iterator"])
                            return Array.from(t)
                    }(o) || function(t, n) {
                        if (t) {
                            if ("string" == typeof t)
                                return e(t, n);
                            var r = Object.prototype.toString.call(t).slice(8, -1);
                            return "Object" === r && t.constructor && (r = t.constructor.name),
                            "Map" === r || "Set" === r ? Array.from(t) : "Arguments" 
                            === r || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? e(t, n) : void 0
                        }
                    }(o) || function() {
                        throw new TypeError("Invalid attempt to spread non-iterable instance.\
                        nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
                    }()),
                    c !== u - 1 && l.push(i[c]);
                var p = l.length;
                p > 30 && (t = l.slice(0, 10).join("") + l.slice(Math.floor(p / 2) - 5, 
                Math.floor(p / 2) + 5).join("") + l.slice(-10).join(""))
            }
            for (var d = "".concat(String.fromCharCode(103)).concat(String.fromCharCode(116)).concat
            (String.fromCharCode(107)), h = (null !== r ? r : (r = window[d] || "") || "").split("."), 
            f = Number(h[0]) || 0, m = Number(h[1]) || 0, g = [], y = 0, v = 0; v < t.length; v++) {
                var _ = t.charCodeAt(v);
                _ < 128 ? g[y++] = _ : (_ < 2048 ? g[y++] = _ >> 6 | 192 : (55296 == (64512 & _) && v + 1 < 
                t.length && 56320 == (64512 & t.charCodeAt(v + 1)) ? (_ = 65536 + ((1023 & _) << 10) + 
                (1023 & t.charCodeAt(++v)),
                g[y++] = _ >> 18 | 240,
                g[y++] = _ >> 12 & 63 | 128) : g[y++] = _ >> 12 | 224,
                g[y++] = _ >> 6 & 63 | 128),
                g[y++] = 63 & _ | 128)
            }
            for (var b = f, w = "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat
            (String.fromCharCode(97)) + "".concat(String.fromCharCode(94)).concat(String.fromCharCode(43)).concat
            (String.fromCharCode(54)), k = "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat
            (String.fromCharCode(51)) + "".concat(String.fromCharCode(94)).concat(String.fromCharCode(43)).concat
            (String.fromCharCode(98)) + "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat
            (String.fromCharCode(102)), x = 0; x < g.length; x++)
                b = n(b += g[x], w);
            return b = n(b, k),
            (b ^= m) < 0 && (b = 2147483648 + (2147483647 & b)),
            "".concat((b %= 1e6).toString(), ".").concat(b ^ f)
        }'''

    js_to_py = js2py.EvalJs()
    js_to_py.execute(js)
    sign = js_to_py.sign(sentence)
    return sign


def translate():  # 定义翻译函数
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Acs-Token": "1672560348803_1672624931422_r5Il+d7eV22e4yrm2mJOCrZDFsvkGlrcsByz+"
                     "U0uEAzOZfH1SDneOw6EY9oxm5tcmKiRXbhubz7cj3NGxacQFeG4lRr12bl1nAmWNeWMFBUU40vNkhkIaYR/"
                     "iQbyl5B2laMRIGLTll4MXxqV3t/UlRIILKqDQolPpnOPlXKN1ANCuDkYNbn+AlTbSGew9+"
                     "H8e0VTk7wz2QhHvh5C27eA9kgzJGkWK0Y9msNdFGZMUy/K++6B+swYyizzvb1S/q5UhBmsH8e96+"
                     "bqo5nO0b6AAGDnSSBkQrVkaBjDZ2k9AOZGOf0Y+"
                     "NIReFXQbR4b7HfnAMMhsqxh4OiVDSs4TymwyHgOqnsONcoGdHUSBTL0v"
                     "JeFj0kPY4SX1AQIHgtgSh8536FoSWVikG72pb1TqWT7UjycyI9awm1V81KUFQPFIMo=",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "BIDUPSID=133F104840A7E29EB31DB59D5EE30A2F; PSTM=1666268514; APPGUIDE_10_0_2=1; "
                  "REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; "
                  "SOUND_PREFER_SWITCH=1; MCITY=-151%3A; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; "
                  "BAIDUID=287A3375722938B1F18F75AAA481BDF9:FG=1; __"
                  "yjs_duid=1_f6f3706a36025c3fb586f467922aedc81672452826910; "
                  "BAIDUID_BFESS=287A3375722938B1F18F75AAA481BDF9:FG=1; BA_HECTOR=ak8g852la4a10h2l8l0ga75t1hr343l1j; "
                  "ZFY=vQYFdLR:A7FYttE1z7a7Sy7O:B49Nzhn6YOzrUQ:BgyTes:C; BDRCVFR[Zh1eoDf3ZW3]=mk3SLVN4HKm; "
                  "delPer=0; PSINO=2; H_PS_PSSID=26350; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1672144007,1672367119,"
                  "1672462040,1672624536; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1672624536; "
                  "ab_sr=1.0.1_MWQyNDJjNmU0MDNkZDhjZDcxZGZhMDU5YThiZTRmMjQ4ZTY2YjgwMDRiNjYzNjJhZjUyMzlhZWI3OGY4ZGVhOTY"
                  "wNmQ1MWJlYzI4YTdhYjY5YTFjMDlkNDZiZmNmMmI5MDY3MzBhOWUwNDRmNWY5NzBmYmM3YzRmODc5ZGMwOTYxZTRlNTVm"
                  "ZjMxMzAwNDgwMTJkYzM3MWRhMWQ5ODYyMA==",
        "Origin": "https://fanyi.baidu.com",
        "Referer": "https://fanyi.baidu.com/?aldtype=16047",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
        "X-Requested-With": "XMLHttpRequest",
    }  # UA伪装
    params = {
        "from": "zh",
        "to": "en"
    }  # 字符串参数
    words = {
        "from": lang_from,
        "to": lang_to,
        "query": sentence,
        "transtype": "translang",
        "simple_means_flag": "3",
        "sign": get_sign(),
        "token": "4ce92f33f79a0c8916e1fbd8101af07c",
        "domain": "common"
    }  # 表单数据
    re = requests.post(url=url, data=words, params=params, headers=headers)
    pt = re.json()  # 返回json数据
    dic = eval(str(pt))  # 转化为字典
    results = dic["trans_result"]["data"][0:]
    result_end = ''
    for result in results:  # 对字典中的结果进行处理
        results_line = result["result"]
        result_line = ''
        for result_of_line in results_line:
            result_line += result_of_line[1] + ' '
        result_end += result_line+'\n'

    return result_end


def main():  # 主函数
    root = tkinter.Tk()
    root.title('翻译')
    root.geometry('550x600')
    # 输入标签提示
    label_input = tkinter.Label(root, text='请输入单词或短句（按钮或回车执行）：', font=('微软雅黑', 16))
    label_input.place(x=2, y=5)
    # 输入文本框
    text_input = tkinter.Text(root, font=('微软雅黑', 15), bd=2)
    text_input.place(x=20, y=50, height=200, width=500)
    # 输出结果提示
    label_output = tkinter.Label(root, text='翻译结果：', font=('微软雅黑', 16))
    label_output.place(x=2, y=260)
    # 输出文本框
    text_output = tkinter.Text(root, font=('微软雅黑', 15), bd=2)
    text_output.place(x=20, y=300, height=270, width=500)

    def show():  # 任务等待时展示提示
        text_output.delete(0.0, 'end')
        text_output.insert(1.1, '正在翻译，请稍后...')
        return

    def set_in():  # 向结果文本框输入结果
        global sentence, url  # 声明全局变量
        sentence = text_input.get(0.0, 'end')
        language()  # 判断翻译语言

        if sentence != '\n':
            try:  # 程序异常机制
                result = translate()
                text_output.delete(0.0, 'end')
                text_output.insert(1.1, result)
            except IndexError:  # 请求页面尚未完全加载应对机制
                text_output.delete(0.0, 'end')
                text_output.insert(1.1, '请求超时，请重试！')
            except KeyError:  # 输入太多空格并且无其它内容时应对机制
                text_output.delete(0.0, 'end')
                text_output.insert(1.1, '输入值有误！！！')
            except requests.exceptions.ConnectionError:  # 无网络时应对机制
                text_output.delete(0.0, 'end')
                text_output.insert(1.1, '请连接网络后运行！')
        else:  # 无输入时应对机制
            time.sleep(1)
            text_output.delete(0.0, 'end')
            text_output.insert(1.1, '输入值有误！！！')

    def get():  # 多线程并行执行实现等待程序运行
        threading.Thread(target=show).start()
        threading.Thread(target=set_in).start()
    # 翻译执行按钮
    button_start = tkinter.Button(root, text='开始翻译', font=('微软雅黑', 14), bd=3, command=get)
    button_start.place(x=400, y=3)
    button_start.bind_all('<Return>', lambda event=None: button_start.invoke())
    root.mainloop()  # 展示窗口


if __name__ == '__main__':
    main()
