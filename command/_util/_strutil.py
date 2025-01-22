import re
def split_first_letter(s):
    # 使用正则表达式找到第一个字母的位置
    match = re.search(r'[a-zA-Z]', s)
    if match:
        index = match.start()
        # 分割字符串
        before = s[:index]
        letter = s[index]
        after = s[index + 1:]
        return before, letter, after
    else:
        # 如果没有字母，返回整个字符串和两个空字符串
        return s, '', ''