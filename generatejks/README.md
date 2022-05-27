## 使用须知

该项目仅适用于生成jks的单功能。通过命令行调用批量生成新的jks以及获取jks的相关签名信息，
需要本地装有jdk8u191以下的版本才可获得到md5，新版本keytool命令仅可获得sha1以及sha256


文件目录注释
｜- creatjks
    | - jks                 （自动生成存放所有jks相关文件）
        | - 序号             （以序号表示）
            | - jksinfo.txt （jks相关信息）
            | - xx.jks      （jks文件）
    | - com.xxx.xxx         （自动生成存放单个对应包名的jks相关文件）
        | - jksinfo.txt     （jks相关信息）
        | - xx.jks          （jks文件）
    | - multishell.py       （批量生成脚本执行程序）
    | - config.py           （相关配置封装，配置详情请查看对应注释）
    | - singleshell.py      （单个生成脚本执行程序）
    | - utils.py            （核心代码封装）
    | - randompackage.py    （随机生成包名封装）