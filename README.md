# recommender-system


本项目实现常见的推荐系统算法，如itembased,userbased,slope one,svd,svd++。通过从mysql中读取存在的movielens数据集
(http://www.grouplens.org/)
中的９：１划分的训练集和测试集合。并通过web端的操作，实现在web展示不同算法对于不同用户的电影推荐结果，以及不同算法的误差ＭＡＥ。

## web界面
![image](https://github.com/hongyesuifeng/recommender-system/blob/master/django_learn/image-folder/web%E7%95%8C%E9%9D%A2%EF%BC%91.jpg)

## web界面的含义
界面从上往下主要分为三个部分：
- 算法初始化部分 </br>
该部分最上面有个标题：算法初始化，标题下面有五个按钮，每个按钮代表着这种算法的初始化，在web界面点击之后，会调用相关的python程序，该程序会拉取数据库的训练集数据训练该模型。
- 预测用户评分 -</br>
该部分主要存在两栏，上面一栏左侧写着预测用户下面括号是输入范围，右边是一个输入框用于输入预测的用户。输入值１～９４３表示预测哪个用户，输入需要预测的用户后点击右侧的预测按钮，通过之前初始化的算法，对于该用户的预测结果将显示在下面的结果展示中。
- 计算该算法的ＭＡＥ值 - </br>
该部分用于计算初始化算法的在测试集上的ＭＡＥ值，点击ＭＡＥ按钮，在测试集上的ＭＡＥ值将显示在右侧。
