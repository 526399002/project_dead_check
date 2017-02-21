# project_dead_check
##一、功能介绍：##

**以读取配置文件的方式，按设定好的任务计划进行自定义监控：**
* 监控进程是否假死：
    根据日志文件大小一段时间内是否变更，及文件ctime是否变更做判断依据
    
* 增量监控日志的异常信息：
    针对大日志文件做到减少监控资源
   
   
**目录结构：**
* conf：核心配置文件，main.py读取配置文件中的信息完成操作
* var：各项目的变量函数及公共变量
* m_error：自定义异常信息
* base：管理项目的任务调度执行，使用的是APScheudler
* middle：中间函数，现只有命令行参数解析
* func：项目的功能实现
* log：存放日志文件的目录
* requirement.txt：依赖的Python库信息
* sendmail.py：邮件发送文件
* main.py：项目启动文件
 
 
##二、安装及使用：##
**环境准备：**

依赖的python版本:
* python 3.X
    
安装依赖Python库:
* pip install -r requirement.txt
    
    
**配置邮件发送方：**
```
$ vim conf/mail.conf
{
  email {
    smtp = smtp.163.com      // smtp服务器的URL地址
    port = 25                // smtp服务器的端口
    src = "test@163.com"     // 邮箱账号，也是发送邮件的用户
    password = "XXXXXXXX"    // 邮箱密码
    send_id = "系统管理员"    // 邮件中显示的发件人名称
    }
}
```

**配置进程假死监控：**
```
$ vim conf/settings.conf
thread {
  file1 {                     // 线程编号, 可随意定义
    project = "a.log"         // 项目名称
    counts_send = 1           // 连续错误时，邮件发送上限
    log_path = "/data/a.log"  // 进程输出的日志路径
    recipients = "test@qq.com" // 收件人列表, 以逗号隔开
    scheduler = {              ## 线程执行间隔
      trigger = interval
      seconds = 1200           // 按秒 
      }
  }
}
```

**配置日志异常信息监控：**
```
thread {
  file1 {                     // 线程编号, 可随意定义
    project = "a.log"         // 项目名称
    counts_send = 1           // 连续错误时，邮件发送上限
    behind = 2                // 输出错误信息后 N 行
    log_path = "/data/a.log"  // 进程输出的日志路径
    recipients = "test@qq.com" // 收件人列表, 以逗号隔开
    patterns = "error"         // 异常信息的匹配正则
    auto_cut = "True"          // 日志是否自动切割
    scheduler = {              ## 线程执行间隔
      trigger = interval
      seconds = 1200           // 按秒 
      }
  }
}
```

**启动监控:**
* -l：仅启动日志异常监控
* -d：仅启动进程假死监控
```
nohup python main.py -l -d &
```
