from pro_codeanalysis.javarule.Definition import *


class Regular:
    """
    在匹配固定字符时如果是长串可以用（）包裹，需要多次匹配在其后加*
    例如：(spell)*匹配0次或多次spell单词

    ^	        匹配字符串的开头
    $	        匹配字符串的末尾。
    .	        匹配任意字符，除了换行符，当re.DOTALL标记被指定时，则可以匹配包括换行符的任意字符。
    [...]	    用来表示一组字符,单独列出：[amk] 匹配 'a'，'m'或'k'
    [^...]	    不在[]中的字符：[^abc] 匹配除了a,b,c之外的字符。
    re*	        匹配0个或多个的表达式。
    re+	        匹配1个或多个的表达式。
    re?	        匹配0个或1个由前面的正则表达式定义的片段，非贪婪方式
    re{ n}	    匹配n个前面表达式。例如，"o{2}"不能匹配"Bob"中的"o"，但是能匹配"food"中的两个o。
    re{ n,}	    精确匹配n个前面表达式。例如，"o{2,}"不能匹配"Bob"中的"o"，但能匹配"foooood"中的所有o。"o{1,}"等价于"o+"。"o{0,}"则等价于"o*"。
    re{ n, m}	匹配 n 到 m 次由前面的正则表达式定义的片段，贪婪方式
    a| b	    匹配a或b
    (re)	    G匹配括号内的表达式，也表示一个组
    (?imx)	    正则表达式包含三种可选标志：i, m, 或 x 。只影响括号中的区域。
    (?-imx)	    正则表达式关闭 i, m, 或 x 可选标志。只影响括号中的区域。
    (?: re)	    类似 (...), 但是不表示一个组
    (?imx: re)	在括号中使用i, m, 或 x 可选标志
    (?-imx: re)	在括号中不使用i, m, 或 x 可选标志
    (?#...)	    注释.
    (?= re)	    前向肯定界定符。如果所含正则表达式，以 ... 表示，在当前位置成功匹配时成功，否则失败。但一旦所含表达式已经尝试，匹配引擎根本没有提高；模式的剩余部分还要尝试界定符的右边。
    (?! re)	    前向否定界定符。与肯定界定符相反；当所含表达式不能在字符串当前位置匹配时成功
    (?> re)	    匹配的独立模式，省去回溯。
    \w	        匹配字母数字
    \W	        匹配非字母数字
    \s	        匹配任意空白字符，等价于 [\t\n\r\f].
    \S	        匹配任意非空字符
    \d	        匹配任意数字，等价于 [0-9].
    \D	        匹配任意非数字
    \A	        匹配字符串开始
    \Z	        匹配字符串结束，如果是存在换行，只匹配到换行前的结束字符串。c
    \z	        匹配字符串结束
    \G	        匹配最后匹配完成的位置。
    \b	        匹配一个单词边界，也就是指单词和空格间的位置。例如， 'er\b' 可以匹配"never" 中的 'er'，但不能匹配 "verb" 中的 'er'。
    \B	        匹配非单词边界。'er\B' 能匹配 "verb" 中的 'er'，但不能匹配 "never" 中的 'er'。
    \n, \t, 等.	匹配一个换行符。匹配一个制表符。等
    \1...\9	    匹配第n个分组的子表达式。
    \10	        匹配第n个分组的子表达式，如果它经匹配。否则指的是八进制字符码的表达式。
    """

    @staticmethod
    def r_package():
        """
        匹配包路径
        :return:
        """
        return '(\\w+\\.)+\\w+'

    @staticmethod
    def r_head_package():
        """
        匹配java头 包路径
        :return:
        """
        return '^(package)\\s+' + Regular.r_package() + '\\s*;?'

    @staticmethod
    def r_import():
        """
        匹配import包路径
        :return:
        """
        return '^(import)\\s+' + Regular.r_package() + '\\s*;?'

    @staticmethod
    def r_permission():
        """
        匹配权限申明
        :return: 正则
        """
        rule = '('
        for permission in Definition.permission:
            rule += (permission + '|')
        if rule.endswith('|'):
            rule = rule[0:(len(rule) - 1)]
        rule += ')*'
        return rule

    @staticmethod
    def r_modifier():
        """
        匹配修饰符
        :return: 正则
        """
        rule = '('
        for modifier in Definition.modifier:
            rule += (modifier + '|')
        if rule.endswith('|'):
            rule = rule[0:(len(rule) - 1)]
        rule += ')*'
        return rule

    @staticmethod
    def r_date_type():
        """
        匹配基本数据类型
        :return: 正则
        """
        rule = '('
        for date_type in Definition.date_type:
            rule += (date_type + '|')
        if rule.endswith('|'):
            rule = rule[0:(len(rule) - 1)]
        rule += ')'
        return rule

    @staticmethod
    def r_class_type():
        """
        匹配class类型
        :return: 正则
        """
        rule = '('
        for class_type in Definition.class_type:
            rule += (class_type + '|')
        if rule.endswith('|'):
            rule = rule[0:(len(rule) - 1)]
        rule += ')'
        return rule

    @staticmethod
    def r_name():
        """
        匹配定义类名
        :return: [^\s<>{}]*
        """
        return '\\w+'

    @staticmethod
    def r_t():
        """
        匹配范型
        :return:
        """
        return '(<[\\w\\s\\?<>]+>)'

    @staticmethod
    def r_class():
        return '^' + Regular.r_permission() + '\\s*' + Regular.r_modifier() + '\\s*' \
               + Regular.r_class_type() + '{1}\\s*' + Regular.r_name() + Regular.r_t() + '?\\s*(extends)?\\s*' \
               + Regular.r_name() + Regular.r_t() + '*\\s*(implements)?\\s*[^{}]*{*'

    @staticmethod
    def r_method():
        return Regular.r_permission() + '\\s*(' + Regular.r_modifier() + '\\s*){0,4}' \
               + Regular.r_t() + '*\\s*\\w+' + Regular.r_t() + '?\\s+[\\w]+\\(.*\\)\\s*\\{'

    @staticmethod
    def r_method_initialize():
        return '^' + Regular.r_permission().replace("*", "") + '\\s+' + Regular.r_name() + '\\s*\\(.*\\)\\s*\\{'

    @staticmethod
    def r_method_initialize_static():
        return '^(static)\\s*\\{'

    @staticmethod
    def r_method_params():
        return '(' + Regular.r_at() + '\\s+)*' + '(final\\s+)?\\w+' + Regular.r_t() + '?\\s+\\w+'

    @staticmethod
    def r_method_name():
        return '\\w+\\('

    @staticmethod
    def r_method_return():
        return '\\s*\\w+' + Regular.r_t() + '?\\s+\\w+\\('

    @staticmethod
    def r_at():
        return '(@\\w+)'

    @staticmethod
    def r_implements():
        return '(implements)\\s+([\\w<>.,]+\\s+)+'

    @staticmethod
    def r_extends():
        return '(extends)\\s+' + Regular.r_name() + Regular.r_t() + '?'
